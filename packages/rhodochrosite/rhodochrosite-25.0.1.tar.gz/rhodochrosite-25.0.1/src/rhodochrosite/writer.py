import math
from collections.abc import Collection, Mapping, Sequence
from io import BytesIO
from typing import IO, assert_never

import attrs

from rhodochrosite.ruby import (
    ENCODING_SYMBOL,
    CustomMarshal,
    RubyClassReference,
    RubyMarshalValue,
    RubySpecialInstance,
    RubySymbol,
    RubyTypeCode,
    RubyUserObject,
    RubyUserSpecialSubtypeObject,
)

# Note on object links:
# As lists/dicts/mutable objects, etc, are unhashable in Python, no object links are emitted. This
# makes the outputted marshal file a bit longer. When an object is marshalled vs when it isn't also
# depends on implementation details of the Ruby Marshal module, whereas it is completely fine to
# just not emit object links.


@attrs.define(slots=True, kw_only=True)
class MarshalWriter:
    """
    A low-level writer for data in the Ruby marshal format.
    """

    #: The underlying buffer to write to.
    buffer: IO[bytes] = attrs.field(factory=BytesIO)

    #: A mapping of {seen symbols: position} used to emit symbol links.
    seen_symbols: dict[RubySymbol, int] = attrs.field(init=False, factory=dict)

    #: If true, the version header has been written.
    written_header: bool = attrs.field(init=False, default=False)

    def _write_header(self) -> None:
        if self.written_header:
            return

        self.buffer.write(b"\x04\x08")
        self.written_header = True

    def _write_raw_number(self, number: int) -> None:
        """
        Writes a raw fixed number to the stream.
        """

        # https://github.com/d9pouces/RubyMarshal/blob/81135afa0235ca3b6e895192da3978f49b9a9706/rubymarshal/writer.py#L249

        if number == 0:
            self.buffer.write(b"\x00")
            return

        if 0 < number < 123:
            self.buffer.write((number + 5).to_bytes(length=1, byteorder="little", signed=True))
            return

        if -124 < number < 0:
            self.buffer.write((number - 5).to_bytes(length=1, byteorder="little", signed=True))
            return

        size = math.ceil(number.bit_length() / 8.0)
        if size > 5:
            raise ValueError(f"{number} is too big for a fixnum")

        original_obj = number
        factor = 256**size

        if number < 0 and number == -factor:
            size -= 1
            number += factor / 256

        elif number < 0:
            number += factor

        sign = int(math.copysign(size, original_obj))
        self.buffer.write(sign.to_bytes(1, byteorder="little", signed=True))

        for _ in range(size):
            self.buffer.write((number % 256).to_bytes(byteorder="little", signed=False))
            number //= 256

    def _write_raw_string(self, s: str | bytes, /) -> None:
        """
        Writes a single raw bytestring to the stream.
        """

        if isinstance(s, str):
            s = s.encode("utf-8")

        self._write_raw_number(len(s))
        self.buffer.write(s)

    def _write_symbol_with_typecode(self, symbol: RubySymbol) -> None:
        """
        Writes a symbol with the appropriate typecode.
        """

        # we want round-tripping so we have to actually care about writing out symlinks
        try:
            previous_pos = self.seen_symbols[symbol]
        except KeyError:
            pass
        else:
            self.buffer.write(RubyTypeCode.SymbolLink)
            self._write_raw_number(previous_pos)
            return

        self.buffer.write(RubyTypeCode.Symbol)
        self._write_raw_string(symbol.value)
        self.seen_symbols[symbol] = len(self.seen_symbols)

    def _write_pairs(self, pairs: Collection[tuple[RubyMarshalValue, RubyMarshalValue]]) -> None:
        """
        Writes out a list of (key, value) pairs.
        """

        self._write_raw_number(len(pairs))
        for k, v in pairs:
            self.write_object(k)
            self.write_object(v)

    def _write_array_with_typecode(self, arr: Collection[RubyMarshalValue]) -> None:
        """
        Writes out an array of objects.
        """

        self.buffer.write(RubyTypeCode.Array)
        self._write_raw_number(len(arr))
        for item in arr:
            self.write_object(item)

    def _write_dict_with_typecode(self, dict: Mapping[RubyMarshalValue, RubyMarshalValue]) -> None:
        """
        Writes out a dict/Ruby hash of objects.
        """

        self.buffer.write(RubyTypeCode.Hash)
        self._write_pairs(dict.items())

    def _write_ruby_object(self, obb: RubyUserObject) -> None:
        """
        Writes a single Ruby object into the stream.
        """

        self.buffer.write(RubyTypeCode.Object)
        self._write_symbol_with_typecode(obb.ruby_class_name)
        pairs = obb.find_instance_variables()
        self._write_pairs(pairs)

    def write_object(self, object: RubyMarshalValue) -> None:
        """
        Writes a single object to the buffer.

        Ideally, this should only be called once at the top-level because ``Marshal.load`` on the
        Ruby side only supports loading a single value.
        """

        self._write_header()

        # Note: This is noqa'd because it means that any missing ``return`` will fall through to
        # the final assert_never() and cause a type-checker error.

        if object is True:
            self.buffer.write(RubyTypeCode.StaticTrue)
            return

        elif object is False:  # noqa: RET505
            self.buffer.write(RubyTypeCode.StaticFalse)
            return

        elif object is None:
            self.buffer.write(RubyTypeCode.StaticNone)
            return

        elif isinstance(object, int):
            # TODO: big numbers
            self.buffer.write(RubyTypeCode.Fixnum)
            self._write_raw_number(object)
            return

        elif isinstance(object, float):
            # XXX: Marshal.dump will strip trailing zeroes; I think this is identical to the ``g``
            #      format specifier...
            #      Needs further tests?

            self.buffer.write(RubyTypeCode.Float)
            self._write_raw_string(f"{object:g}")
            return

        elif isinstance(object, str):
            # encoded string with instance variables...
            self.buffer.write(RubyTypeCode.Instance)
            self.buffer.write(RubyTypeCode.String)
            self._write_raw_string(object)
            self._write_pairs([(ENCODING_SYMBOL, True)])
            return

        elif isinstance(object, bytes):
            # non-encoded string with no instance variables
            self.buffer.write(RubyTypeCode.String)
            self._write_raw_string(object)
            return

        elif isinstance(object, RubySpecialInstance):
            # apparently the Reborn OrderedHash class uses this????
            self.buffer.write(RubyTypeCode.Instance)

            # intercept strings so that they don't get wrapped in an instance
            if isinstance(object.base_object, str):
                pairs = dict(object.instance_variables)
                self.buffer.write(RubyTypeCode.String)
                self._write_raw_string(object.base_object)
                pairs[ENCODING_SYMBOL] = True
                pairs = list(pairs.items())
            else:
                pairs = object.instance_variables
                self.write_object(object.base_object)

            self._write_pairs(pairs)
            return

        elif isinstance(object, RubySymbol):
            self._write_symbol_with_typecode(object)
            return

        elif isinstance(object, Sequence):
            self._write_array_with_typecode(object)
            return

        elif isinstance(object, Mapping):
            self._write_dict_with_typecode(object)
            return

        # XXX: This has to be above it because it's a more specialised type!
        elif isinstance(object, RubyUserSpecialSubtypeObject):
            if object.instance_variables:
                self.buffer.write(RubyTypeCode.Instance)

            self.buffer.write(RubyTypeCode.SpecialSubtypeObject)
            self._write_symbol_with_typecode(object.name)

            # luckily for us the inner value is typecode prefixed

            if isinstance(object.wrapped_object, str):
                # we need to intercept strings as writing a regular str with this function will
                # force it to be wrapped in an Instance
                self.buffer.write(RubyTypeCode.String)
                self._write_raw_string(object.wrapped_object)
                object.instance_variables[ENCODING_SYMBOL] = True
            else:
                self.write_object(object.wrapped_object)

            if object.instance_variables:
                self._write_pairs(object.instance_variables.items())

            return

        elif isinstance(object, RubyUserObject):
            self._write_ruby_object(object)
            return

        elif isinstance(object, CustomMarshal):
            raw_bytes = object.get_raw_bytes()

            self.buffer.write(RubyTypeCode.UserDefined)
            self._write_symbol_with_typecode(object.ruby_class_name)
            self._write_raw_string(raw_bytes)
            return

        elif isinstance(object, RubyClassReference):  # pyright: ignore [reportUnnecessaryIsInstance]
            self.buffer.write(RubyTypeCode.Klass)
            # doesn't use a symbol, but *does* use object links for some bizarre reason??
            self._write_raw_string(object.value.value)
            return

        assert_never(object)


def write_object(data: RubyMarshalValue) -> bytes:
    """
    Marshals a single, top-level object.
    """

    buf = BytesIO()
    writer = MarshalWriter(buffer=buf)
    writer.write_object(data)
    return buf.getvalue()
