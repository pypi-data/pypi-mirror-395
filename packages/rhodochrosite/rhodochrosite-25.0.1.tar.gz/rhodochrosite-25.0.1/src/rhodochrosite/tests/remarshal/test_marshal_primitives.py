from typing import Any

import pytest

from rhodochrosite.ruby import RubySpecialInstance, atom
from rhodochrosite.writer import write_object


@pytest.mark.parametrize(
    ("what", "marshalled"),
    [
        (True, b"\x04\bT"),
        (False, b"\x04\bF"),
        (None, b"\x04\b0"),
    ],
)
def test_writing_statics(what: Any, marshalled: bytes) -> None:
    assert write_object(what) == marshalled


def test_marshal_string() -> None:
    assert write_object("test") == b'\x04\bI"\ttest\x06:\x06ET'


def test_marshal_bytestring() -> None:
    assert write_object(b"test") == b'\x04\b"\ttest'


def test_writing_array() -> None:
    assert write_object([1, 2, 3]) == b"\x04\b[\bi\x06i\ai\b"


def test_writing_symbols() -> None:
    assert write_object(atom("abc")) == b"\x04\b:\babc"


def test_writing_symbol_links() -> None:
    # official marshaller won't dupe symbols, make sure we don't either
    assert write_object([atom("abc"), atom("abc")]) == b"\x04\b[\a:\babc;\x00"


def test_writing_dicts() -> None:
    assert write_object({atom("name"): "abc"}) == b'\x04\b{\x06:\tnameI"\babc\x06:\x06ET'


def test_writing_floats() -> None:
    assert write_object([1.5, 1.5]) == b"\x04\b[\af\b1.5f\b1.5"


def test_writing_floats_with_truncation() -> None:
    assert write_object(1.0) == b"\x04\bf\x061"


def test_writing_instances() -> None:
    assert (
        write_object(
            RubySpecialInstance(base_object=b"test", instance_variables=[(atom("E"), True)])
        )
        == b'\x04\bI"\ttest\x06:\x06ET'
    )


def test_writing_wrapped_string() -> None:
    assert (
        write_object(
            RubySpecialInstance(base_object="test", instance_variables=[(atom("E"), True)])
        )
        == b'\x04\bI"\ttest\x06:\x06ET'
    )
