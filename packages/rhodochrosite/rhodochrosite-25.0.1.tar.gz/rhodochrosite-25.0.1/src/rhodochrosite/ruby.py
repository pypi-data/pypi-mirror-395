from __future__ import annotations

import abc
import enum
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import NotRequired, TypedDict, cast, final, override

import attrs

from rhodochrosite.exc import ObjectMissingKeyError

type RubyMarshalValue = (
    bool
    | None
    | int
    | str
    | bytes
    | float
    | RubySymbol
    | RubyClassReference
    | RubySpecialInstance
    | RubyUserObject
    | CustomMarshal
    | Sequence[RubyMarshalValue]
    | Mapping[RubyMarshalValue, RubyMarshalValue]
)


type ObjectMakerFunc = Callable[[RubySymbol, dict[RubySymbol, RubyMarshalValue]], RubyUserObject]
type RubyConverter = Callable[[RubyMarshalValue], RubyMarshalValue]


class RubyExtra(TypedDict):
    """
    Extra data for attrs fields defining how they are marshalled to Ruby fields.
    """

    skip: bool
    ivar_name: NotRequired[str]
    ruby_converter: NotRequired[RubyConverter]


def ruby_skip() -> dict[str, RubyExtra]:
    return {"ruby": {"skip": True}}


def ruby_name(name: str) -> dict[str, RubyExtra]:
    return {"ruby": {"skip": False, "ivar_name": name}}


def ruby_converter(converter: RubyConverter) -> dict[str, RubyExtra]:
    return {"ruby": {"skip": False, "ruby_converter": converter}}


class RubyTypeCode(bytes, enum.Enum):
    """
    An enumeration of the possible Ruby type codes.
    """

    StaticTrue = b"T"
    StaticFalse = b"F"
    StaticNone = b"0"
    Fixnum = b"i"
    Float = b"f"
    Symbol = b":"
    SymbolLink = b";"
    Klass = b"c"
    Object = b"o"
    String = b'"'
    Instance = b"I"
    Array = b"["
    Hash = b"{"
    ObjectLink = b"@"
    SpecialSubtypeObject = b"C"
    UserDefined = b"u"


# because Enum(b"?") is REALLY fucking slow???
def _make_type_code_cache() -> dict[bytes, RubyTypeCode]:
    cache: dict[bytes, RubyTypeCode] = {}
    for code in RubyTypeCode.__members__:
        i = RubyTypeCode[code]
        cache[i.value] = i

    return cache


TYPE_CODE_CACHE: dict[bytes, RubyTypeCode] = _make_type_code_cache()


@attrs.define(slots=True, frozen=True, repr=True, str=False, eq=True, hash=True)
@final
class RubySymbol:
    """
    A special type of immutable string.

    See https://ruby-doc.org/3.3.3/Symbol.html for more information.
    """

    __match_args__ = ("value",)

    #: The actual value of this symbol.
    #:
    #: Obstensibly, this can be any sequence of bytes; in practice, it's a unicode string.
    value: str = attrs.field()

    @override
    def __str__(self) -> str:
        return self.value

    @override
    def __repr__(self) -> str:
        return f"RubySymbol({self.value})"


def atom(s: str, /) -> RubySymbol:
    """
    Shorthand notation for making a :class:`.RubySymbol`.
    """

    return RubySymbol(s)


ENCODING_SYMBOL = atom("E")


@attrs.define(kw_only=True, slots=True, frozen=True)
class RubySpecialInstance:
    """
    An special instance with instance variables.

    This is separate from a :class:`.AnyRubyObject`, and is only used for certain special objects
    under unknown circumstances.
    """

    #: The base object for this instance.
    base_object: RubyMarshalValue = attrs.field()

    #: The additional instance variables for this instance.
    instance_variables: list[tuple[RubySymbol, RubyMarshalValue]] = attrs.field()


class AnyRubyObject(abc.ABC):
    """
    Marker class for any Ruby-side object instance.

    This can be either a :class:`.RubyNonSpecialObject`
    """

    @property
    @abc.abstractmethod
    def ruby_class_name(self) -> RubySymbol:
        """
        The Ruby-side class name for this ruby object.
        """


@attrs.define(kw_only=True, slots=True, frozen=True, eq=True, hash=True)
@final
class RubyClassReference(AnyRubyObject):
    """
    Wraps a symbol specifically for a Ruby-side class reference.
    """

    #: The name of this class.
    value: RubySymbol = attrs.field()

    @property
    @override
    def ruby_class_name(self) -> RubySymbol:
        """
        The Ruby-side class name for this ruby object.
        """

        return self.value


@attrs.define(kw_only=True, slots=True, frozen=True, eq=True, hash=True)
@final
class RubyModuleReference(AnyRubyObject):
    """
    Wraps a symbol specifically for a Ruby-side module reference.
    """

    #: The name of this class.
    value: RubySymbol = attrs.field()

    @property
    @override
    def ruby_class_name(self) -> RubySymbol:
        """
        The Ruby-side class name for this ruby object.
        """

        return self.value


class RubyUserObject(AnyRubyObject, abc.ABC):
    """
    Base class for any Ruby object that doesn't have a built-in type code.

    All objects inheriting this are serialisable into a Ruby object (with type code ``o``). This
    should be an ``attrs`` class to function properly; all attrs fields on the class will be
    automatically detected.
    """

    def find_instance_variables(self) -> list[tuple[RubySymbol, RubyMarshalValue]]:
        """
        Finds all of the instance variables on this object for re-serialisation.
        """

        fields: Iterable[attrs.Attribute[RubyMarshalValue]] = attrs.fields(type(self))
        ivars: list[tuple[RubySymbol, RubyMarshalValue]] = []

        for field in fields:
            extra = field.metadata
            name = field.name

            ruby_converter: RubyConverter = lambda it: it  # noqa: E731

            if "ruby" in extra:
                ruby = cast(RubyExtra, extra["ruby"])

                if ruby["skip"]:
                    continue

                name = ruby.get("ivar_name", name)
                ruby_converter = ruby.get("ruby_converter", ruby_converter)

            if not name.startswith("@"):
                name = "@" + name

            sym = RubySymbol(name)
            converted = ruby_converter(getattr(self, field.name))
            ivars.append((sym, converted))

        return ivars


def make_ruby_attrs_object_fn(
    klass: type[RubyUserObject], *, skip_extra: bool = False
) -> ObjectMakerFunc:
    """
    Makes a new :class:`.RubyUserObject` that uses ``attrs`` for its fields.
    """

    # TODO: do a cattrs and exec() this
    fields: Iterable[attrs.Attribute[RubyMarshalValue]] = attrs.fields(klass)

    def _make(klass_name: RubySymbol, ivars: dict[RubySymbol, RubyMarshalValue]) -> RubyUserObject:
        transformed_ivars = {s.value[1:]: v for (s, v) in ivars.items()}
        kwargs: dict[str, RubyMarshalValue] = {}

        for field in fields:
            if not field.init:
                continue

            extra = field.metadata
            name = field_name = field.name

            if "ruby" in extra:
                ruby = cast(RubyExtra, extra["ruby"])

                if ruby["skip"]:
                    continue

                name = ruby.get("ivar_name", name)

            try:
                kwargs[field_name] = transformed_ivars.pop(name)
            except KeyError as e:
                raise ObjectMissingKeyError(
                    f"Missing ivar {name} when reading {klass_name.value}"
                ) from e

        if transformed_ivars and not skip_extra:
            names = ", ".join(transformed_ivars.keys())
            raise ValueError(f"{klass.__name__} is missing attributes for {names}")

        return klass(**kwargs)

    return _make


@attrs.define(slots=True, kw_only=True)
class GenericRubyUserObject(RubyUserObject):
    """
    A generic implementation of :class:`.RubyNonSpecialObject`.

    This class is used when the Ruby deserialiser doesn't understand how to decode an object.
    """

    name: RubySymbol = attrs.field()
    instance_variables: dict[RubySymbol, RubyMarshalValue] = attrs.field()

    @override
    def find_instance_variables(self) -> list[tuple[RubySymbol, RubyMarshalValue]]:
        return list(self.instance_variables.items())

    @property
    @override
    def ruby_class_name(self) -> RubySymbol:
        return self.name

    def get_ivar(self, ivar: RubySymbol | str) -> RubyMarshalValue | None:
        if isinstance(ivar, str):
            ivar = RubySymbol(ivar)

        return self.instance_variables.get(ivar)


def make_generic_object(
    name: RubySymbol, instance_vars: dict[RubySymbol, RubyMarshalValue]
) -> GenericRubyUserObject:
    """
    Creates a new :class:`.GenericRubyObject`.
    """

    return GenericRubyUserObject(name=name, instance_variables=instance_vars)


class CustomMarshal(AnyRubyObject, abc.ABC):
    """
    An ABC for any type that has a custom marshal format.

    Examples include the RGSS::Table.
    """

    @abc.abstractmethod
    def get_raw_bytes(self) -> bytes:
        """
        Gets the raw encodeed bytes for this object.
        """


@attrs.define(kw_only=False, slots=True, frozen=True, eq=True, hash=True)
@final
class UnknownCustomMarshal(CustomMarshal, AnyRubyObject):
    """
    A ruby type that has an unknown deserialisation method.
    """

    #: The class name for this user-defined object.
    name: RubySymbol = attrs.field()

    #: The raw data for this user-defined object.
    raw_data: bytes = attrs.field()

    @property
    @override
    def ruby_class_name(self) -> RubySymbol:
        return self.name

    @override
    def get_raw_bytes(self) -> bytes:
        return self.raw_data


@attrs.define(slots=True, kw_only=False)
@final
class RubyUserSpecialSubtypeObject(GenericRubyUserObject):
    """
    A Ruby type that is a subclass of one of four Ruby built-in types.

    These types are either ``String``, ``Regexp``, ``Array``, or ``Hash``. The wrapped value will
    be one of those four objects.
    """

    wrapped_object: (
        bytes | str | Sequence[RubyMarshalValue] | Mapping[RubyMarshalValue, RubyMarshalValue]
    ) = attrs.field()

    @property
    @override
    def ruby_class_name(self) -> RubySymbol:
        return self.name
