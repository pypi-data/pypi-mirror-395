from __future__ import annotations

from collections.abc import Callable
from types import MappingProxyType
from typing import Any, assert_never

import attrs

from rhodochrosite.cursor import Cursor
from rhodochrosite.exc import (
    InvalidTypeCode,
    NotAMarshalFile,
    StreamFormatError,
    StreamUnexpectedlyEndedError,
)
from rhodochrosite.ruby import (
    ENCODING_SYMBOL,
    TYPE_CODE_CACHE,
    CustomMarshal,
    ObjectMakerFunc,
    RubyClassReference,
    RubyMarshalValue,
    RubySpecialInstance,
    RubySymbol,
    RubyTypeCode,
    RubyUserObject,
    RubyUserSpecialSubtypeObject,
    UnknownCustomMarshal,
    make_generic_object,
)

# Unlike Python's ``marshal``, Ruby's ``marshal`` is surprisingly well documented.
# The format is available at https://devdocs.io/ruby~3.3/marshal_rdoc.

type CustomMakerFunc = Callable[[RubySymbol, bytes], CustomMarshal]

# Code style note:
# Functions prefixed with `_next` read a type code.
# Functions prefixed with `_read` do not read a type code.


class _SillyRubyDictKey(dict):
    """
    Workaround for silliness.

    For whatever reason, there are people who think putting a hash as the key of a hash is a
    perfectly acceptable thing to do. It is *not* a perfectly acceptable thing to do.
    """

    def _key(self) -> tuple[tuple[Any, Any], ...]:
        return tuple(map(tuple, self.items()))

    def __hash__(self) -> int:
        return hash(self._key())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _SillyRubyDictKey):
            return NotImplemented

        return other._key() == self._key()


@attrs.define(slots=True, kw_only=True)
class MarshalReader:
    """
    A low-level reader for data in the Ruby marshal format.
    """

    #: The stream of data to read.
    stream: Cursor = attrs.field()

    #: A list of previously encountered symbols in this stream.
    symbol_links: list[RubySymbol] = attrs.field(init=False, factory=list)

    #: If True, then strings will be unwrapped in the stream.
    unwrap_strings: bool = attrs.field(default=True)

    #: If True, then all strings will be decoded as UTF-8.
    #:
    #: This is mostly useful for older Ruby code that emitted raw bytestrings in the feed instead
    #: of encoding them as instance strings.
    decode_all_strings: bool = attrs.field(default=False)

    #: If True, then dict keys will be unwrapped into strings.
    unwrap_dict_keys: bool = attrs.field(default=False)

    #: A mapping of {ruby type name: (name, instance vars) -> RubyObject} to make user objects.
    object_factories: dict[RubySymbol, ObjectMakerFunc] = attrs.field(factory=dict)

    #: A mapping of {ruby type name: (name, bytestring) _> RubyObject} for objects with ``_load``.
    #:
    #: Examples include RGSS' Table class.
    custom_factories: dict[RubySymbol, CustomMakerFunc] = attrs.field(factory=dict)

    _object_refs: list[int] = attrs.field(factory=list, init=False)
    _inside_objlink_count: int = attrs.field(default=0, init=False)

    @classmethod
    def from_bytes(
        cls,
        data: bytes | bytearray,
        *,
        unwrap_strings: bool = True,
        decode_all_strings: bool = False,
        unwrap_dict_keys: bool = False,
    ) -> MarshalReader:
        """
        Creates a new :class:`.MarshalReader` from a series of bytes.
        """

        return MarshalReader(
            stream=Cursor(wrapped=bytes(data)),
            unwrap_strings=unwrap_strings,
            decode_all_strings=decode_all_strings,
            unwrap_dict_keys=unwrap_dict_keys,
        )

    def __attrs_post_init__(self) -> None:
        # e first two bytes of the stream contain the major and minor version, each as a single byte
        # encoding a digit. The version implemented in Ruby is 4.8 (stored as “x04x08”) and is
        # supported by ruby 1.8.0 and newer.

        magic_number = self.stream.read(2)
        if magic_number != b"\x04\x08":
            raise NotAMarshalFile(f"Invalid magic number {magic_number}")

    def _read(self, count: int, /, message: str = "End of file") -> bytes:
        # thanks???
        if count == 0:
            return b""

        if data := self.stream.read(count):
            if len(data) < count:
                raise StreamUnexpectedlyEndedError(f"Expected {count} bytes, got {len(data)}")

            return data

        raise StreamUnexpectedlyEndedError(message + f" whilst reading {count} bytes")

    def _push_objref(self) -> None:
        if self._inside_objlink_count >= 1:
            return

        self._object_refs.append(self.stream.cursor - 1)

    def _next_type_code(self) -> RubyTypeCode:
        """
        Reads the next type code from the stream.

        A type code is a single character identifying the next object in the stream.
        """

        return TYPE_CODE_CACHE[self._read(1, "EOF reached when reading next type code")]

    # stolen from rubymarshal directly
    def _read_fixnum(self) -> int:
        size_byte = self._read(1, "Missing the size byte for a fixnum")

        # hardcoded zero
        if size_byte == b"\x00":
            return 0

        length = int.from_bytes(size_byte, signed=True)

        if 5 < length < 128:
            return length - 5

        if -129 < length < -5:
            return length + 5

        result = 0
        factor = 1

        int_body = self._read(abs(length), f"Missing fixnum value of length {abs(length)}")

        for byte in int_body:
            result += byte * factor
            factor *= 256

        if length < 0:
            result = result - factor

        return result

    def _read_float(self) -> float:
        """
        Reads a single floating point number from the stream.
        """

        data = self._read_string().decode("ascii")
        return float(data)

    def _read_symbol(self) -> RubySymbol:
        size = self._read_fixnum()
        name = self._read(size, f"Missing symbol body of length {size}")

        symbol = RubySymbol(value=name.decode(encoding="utf-8"))

        if self._inside_objlink_count <= 0:
            self.symbol_links.append(symbol)

        return symbol

    def _read_symlink(self) -> RubySymbol:
        """
        Reads a reference to a previous symbol in the stream.
        """

        index = self._read_fixnum()
        try:
            return self.symbol_links[index]
        except IndexError:  # pragma: no cover
            # can't reasonably cover this, Marshal.dump should never do this...?
            raise StreamFormatError(f"Invalid symbol link {index}") from None

    def _read_string(self) -> bytes:
        """
        Reads a raw, un-encoded string from the stream.
        """

        length = self._read_fixnum()
        return self._read(length)

    def _read_array(self) -> list[RubyMarshalValue]:
        """
        Reads a Ruby array.
        """

        item_count = self._read_fixnum()
        return [self.next_object() for _ in range(item_count)]

    def _read_hash(self) -> dict[RubyMarshalValue, RubyMarshalValue]:
        """
        Reads a Ruby hash (dict).
        """

        item_count = self._read_fixnum()
        values = {}
        for _ in range(item_count):
            key = self.next_object()
            value = self.next_object()

            if isinstance(key, dict):
                # ? fuck you???
                key = MappingProxyType(_SillyRubyDictKey(key))

            values[key] = value

        if self.unwrap_dict_keys:
            for key in list(values.keys()):
                if isinstance(key, RubySymbol):
                    values[key.value] = values.pop(key)

        return values

    def _read_symbol_pairs(self) -> list[tuple[RubySymbol, RubyMarshalValue]]:
        """
        Reads a set of symbol pairs from the stream.
        """

        count = self._read_fixnum()
        pairs: list[tuple[RubySymbol, RubyMarshalValue]] = []

        for _ in range(count):
            name = self.next_object()

            if not isinstance(name, RubySymbol):  # pragma: no cover
                raise InvalidTypeCode(f"Expected a symbol when reading symbol, but got a '{name}'")

            value = self.next_object()

            pairs.append((name, value))

        return pairs

    def _unwrap_str(
        self, wrapped_str: bytes, ivars: list[tuple[RubySymbol, RubyMarshalValue]]
    ) -> bytes | str:
        """
        Unwraps a string from a ``bytes`` object if it is an encoded string.
        """

        if self.decode_all_strings:
            return wrapped_str.decode()

        for name, value in ivars:
            if name == ENCODING_SYMBOL:
                if value:
                    return wrapped_str.decode()

                # In practice, I don't think it's ever possible for strings with @E: false to be
                # emitted by Marshal.dump.
                return wrapped_str

        return wrapped_str

    def _read_instance(self) -> RubySpecialInstance | RubyUserSpecialSubtypeObject | str | bytes:
        """
        Reads a new "instance" from the stream.

        This will also unwrap str and bytes into their correct types.
        """

        next_code = self._next_type_code()
        completed_object = self._read_object_after_type_code(next_code)
        pairs = self._read_symbol_pairs()

        # extremely gross here... oh well

        if next_code == RubyTypeCode.SpecialSubtypeObject:
            assert isinstance(completed_object, RubyUserSpecialSubtypeObject)

            # copy over all pairs into the special subtype's storage instead
            for k, v in pairs:
                completed_object.instance_variables[k] = v

            if isinstance(completed_object.wrapped_object, bytes):
                completed_object.wrapped_object = self._unwrap_str(
                    completed_object.wrapped_object, pairs
                )

            return completed_object

        if self.unwrap_strings and next_code == RubyTypeCode.String and len(pairs) == 1:
            if self.decode_all_strings:
                # already decoded by the other function, just return it
                assert isinstance(completed_object, str), f"{completed_object} not a decoded str"
                return completed_object

            assert isinstance(completed_object, bytes), "string typecode was followed by non-str???"

            name, value = pairs[0]
            assert name == ENCODING_SYMBOL, "expected String to have a single symbol of 'E'"
            if value:
                return completed_object.decode()

            return completed_object

        return RubySpecialInstance(base_object=completed_object, instance_variables=pairs)

    def _read_ruby_object(self, name: RubySymbol) -> RubyUserObject:
        """
        Reads a new Ruby object from the stream.
        """

        assert not name.value.startswith("@"), (
            "found object name beginning with @; this is obviously incorrect"
        )

        pairs = self._read_symbol_pairs()
        maker = self.object_factories.get(name, make_generic_object)
        ivars = dict(pairs)
        return maker(name, ivars)

    def _next_symbol_or_symlink(self) -> RubySymbol:
        """
        Reads either a symbol or a symlink.
        """

        code = self._next_type_code()
        if code == RubyTypeCode.Symbol:
            return self._read_symbol()

        if code == RubyTypeCode.SymbolLink:
            return self._read_symlink()

        raise InvalidTypeCode(f"Expected to read a symbol or symbol link, got a {code} instead")

    def _read_object_after_type_code(self, code: RubyTypeCode) -> RubyMarshalValue:
        """
        Reads the next object from the stream using the provided type code.
        """

        match code:
            case RubyTypeCode.Instance:
                return self._read_instance()

            case RubyTypeCode.StaticTrue:
                return True

            case RubyTypeCode.StaticFalse:
                return False

            case RubyTypeCode.StaticNone:
                return None

            case RubyTypeCode.Fixnum:  # *not* the arbitrary big-integer type
                return self._read_fixnum()

            case RubyTypeCode.Float:
                self._push_objref()
                return self._read_float()

            case RubyTypeCode.Symbol:
                return self._read_symbol()

            case RubyTypeCode.SymbolLink:
                return self._read_symlink()

            case RubyTypeCode.String:
                # These are possible in the raw stream with e.g. ``Marshal.dump("abc".b)``.
                self._push_objref()
                s = self._read_string()
                if self.decode_all_strings:
                    return s.decode()

                return s

            case RubyTypeCode.Array:
                self._push_objref()
                return self._read_array()

            case RubyTypeCode.Hash:
                self._push_objref()
                return self._read_hash()

            case RubyTypeCode.Klass:
                self._push_objref()
                next = self._read_symbol()
                return RubyClassReference(value=next)

            case RubyTypeCode.Object:
                self._push_objref()
                klass_name = self._next_symbol_or_symlink()
                return self._read_ruby_object(klass_name)

            case RubyTypeCode.SpecialSubtypeObject:
                # for whatever reason CRuby doesn't push these as object references ?_?

                klass_name = self._next_symbol_or_symlink()
                real_value = self.next_object()
                assert isinstance(real_value, (str, bytes, list, dict)), (
                    "special object that wasn't a subtype of bytes, list, hash, but is actually "
                    f"{type(real_value)}"
                )

                # note: instance variables are handed by the ``I`` subtype, rather than this
                # block.
                return RubyUserSpecialSubtypeObject(
                    wrapped_object=real_value, name=klass_name, instance_variables={}
                )

            case RubyTypeCode.ObjectLink:
                link = self._read_fixnum()

                with self.stream.with_seeked_to(self._object_refs[link]):
                    self._inside_objlink_count += 1
                    try:
                        return self.next_object()
                    finally:
                        self._inside_objlink_count -= 1

            case RubyTypeCode.UserDefined:
                self._push_objref()
                klass_name = self._next_symbol_or_symlink()
                size = self._read_fixnum()

                factory = self.custom_factories.get(klass_name, UnknownCustomMarshal)
                return factory(klass_name, self._read(size))

        assert_never(code)

    def next_object(self) -> RubyMarshalValue:
        """
        Reads the next object from this stream.
        """

        return self._read_object_after_type_code(self._next_type_code())


def read_object(
    data: bytes | bytearray,
    *,
    unwrap_strings: bool = True,
    decode_all_strings: bool = False,
    unwrap_dict_keys: bool = False,
) -> RubyMarshalValue:
    """
    Reads a single ``RubyMarshalValue`` from the provided byte data source.
    """

    return MarshalReader.from_bytes(
        data,
        unwrap_strings=unwrap_strings,
        decode_all_strings=decode_all_strings,
        unwrap_dict_keys=unwrap_dict_keys,
    ).next_object()
