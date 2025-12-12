# pyright: reportImplicitOverride=false

from typing import cast

import attr

from rhodochrosite.ruby import RubySymbol, RubyUserObject, ruby_converter, ruby_name, ruby_skip


def test_finding_normal_ivars() -> None:
    @attr.define
    class NormalType(RubyUserObject):
        field: str = attr.field()

        @property
        def ruby_class_name(self) -> RubySymbol:
            raise NotImplementedError

    fields = NormalType(field="abc").find_instance_variables()
    assert fields == [(RubySymbol("@field"), "abc")]


def test_finding_skipped_ivars() -> None:
    @attr.define
    class NormalType(RubyUserObject):
        field: str = attr.field(metadata=ruby_skip())

        @property
        def ruby_class_name(self) -> RubySymbol:
            raise NotImplementedError

    fields = NormalType(field="abc").find_instance_variables()
    assert fields == []


def test_finding_renamed_ivars() -> None:
    @attr.define
    class NormalType(RubyUserObject):
        field: str = attr.field(metadata=ruby_name("other_field"))

        @property
        def ruby_class_name(self) -> RubySymbol:
            raise NotImplementedError

    fields = NormalType(field="abc").find_instance_variables()
    assert fields == [(RubySymbol("@other_field"), "abc")]


def test_finding_converted_ivars() -> None:
    @attr.define
    class WithConverter(RubyUserObject):
        field: str = attr.field(
            converter=lambda it: it[::-1],
            metadata=ruby_converter(lambda it: str(cast(str, it)[::-1])),
        )

        @property
        def ruby_class_name(self) -> RubySymbol:
            raise NotImplementedError

    f = WithConverter("abcdef")
    assert f.field == "fedcba"
    fields = f.find_instance_variables()
    assert fields == [(RubySymbol("@field"), "abcdef")]
