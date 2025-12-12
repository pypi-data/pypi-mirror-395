# Ruby definition:
# class Test
#   def initialize
#     @abc = 1
#   end
# end

from collections.abc import Mapping
from typing import cast, final, override

import attrs
import pytest

from rhodochrosite.cursor import Cursor
from rhodochrosite.reader import MarshalReader, read_object
from rhodochrosite.ruby import (
    GenericRubyUserObject,
    RubyMarshalValue,
    RubySymbol,
    RubyUserObject,
    RubyUserSpecialSubtypeObject,
    atom,
    make_ruby_attrs_object_fn,
    ruby_name,
    ruby_skip,
)

TEST_NAME = RubySymbol(value="Test")


@final
class _Test(RubyUserObject):
    def __init__(self, value: int) -> None:
        self.value = value

    @property
    @override
    def ruby_class_name(self) -> RubySymbol:
        return TEST_NAME


def _make_test(name: RubySymbol, args: dict[RubySymbol, RubyMarshalValue]) -> _Test:
    return _Test(value=cast(int, args[RubySymbol(value="@abc")]))


def test_reading_generic_user_object() -> None:
    data = read_object(b"\x04\bo:\tTest\x06:\t@abci\x06")
    assert isinstance(data, GenericRubyUserObject)
    assert data.name == TEST_NAME
    assert data.find_instance_variables() == [(RubySymbol(value="@abc"), 1)]


def test_reading_custom_user_object() -> None:
    reader = MarshalReader(stream=Cursor(wrapped=b"\x04\bo:\tTest\x06:\t@abci\x06"))
    reader.object_factories[TEST_NAME] = _make_test
    next_object = reader.next_object()

    assert isinstance(next_object, _Test)
    assert next_object.value == 1


@pytest.mark.parametrize(
    ("marshalled", "real_value", "has_ivar"),
    [
        (b'\x04\bC:\x0eTestEmpty"\x00', b"", False),
        (b"\x04\bIC:\rTestList[\bi\x06i\ai\b\x06:\n@testi\x06", [1, 2, 3], True),
        (b'\x04\bIC:\x0eTestEmpty"\ttest\x06:\x06ET', "test", False),
        (b'\x04\bIC:\x0fTestString"\ttest\a:\x06ET:\n@testi\x06', "test", True),
        (b"\x04\bC:\rTestDict{\x06i\x06i\a", {1: 2}, False),
        (b"\x04\bIC:\rTestDict{\x06i\x06i\a\x06:\n@testi\x06", {1: 2}, True),
    ],
    ids=[
        "unencoded-string",
        "array",
        "encoded-string",
        "encoded-string-with-extra-ivars",
        "hash",
        "hash-with-extra-ivars",
    ],
)
def test_unmarshal_special_subtype(
    marshalled: bytes,
    real_value: bytes | str | list[RubyMarshalValue] | Mapping[RubyMarshalValue, RubyMarshalValue],
    has_ivar: bool,
) -> None:
    obb = read_object(marshalled)
    assert isinstance(obb, RubyUserSpecialSubtypeObject)
    assert obb.wrapped_object == real_value

    if has_ivar:
        assert obb.get_ivar("@test") == 1
    else:
        assert not obb.get_ivar("@test")


def test_special_subtype_force_decode_strings() -> None:
    obb = read_object(b'\x04\bC:\x0eTestEmpty"\x00', decode_all_strings=True)
    assert isinstance(obb, RubyUserSpecialSubtypeObject)
    assert obb.wrapped_object == ""


def test_make_ruby_attrs_object_fn() -> None:
    @attrs.define()
    @final
    class Test(RubyUserObject):
        ivar: int = attrs.field()
        ivar_2: list[int] = attrs.field(metadata=ruby_name("ivar2"))
        non_ivar: int = attrs.field(default=1, init=False, metadata=ruby_skip())

        @property
        @override
        def ruby_class_name(self):
            return atom("Test")

    reader = MarshalReader(stream=Cursor(b"\x04\bo:\tTest\a:\n@ivari\x06:\v@ivar2[\bi\x06i\ai\b"))
    reader.object_factories[atom("Test")] = make_ruby_attrs_object_fn(Test)

    next = reader.next_object()
    assert isinstance(next, Test)
    assert next.ivar == 1
    assert next.ivar_2 == [1, 2, 3]
    assert next.non_ivar == 1
