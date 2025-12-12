import pytest

from rhodochrosite.reader import read_object
from rhodochrosite.ruby import GenericRubyUserObject, RubyMarshalValue, RubySymbol, atom


def test_reading_zero_size() -> None:
    assert read_object(b'\x04\bI"\x00\x06:\x06ET') == ""


def test_reading_invalid_size() -> None:
    with pytest.raises(EOFError):
        read_object(b'\x04\bI"\x00\x07:\x06ET')


def test_object_with_symlink_name() -> None:
    result: list[RubyMarshalValue] = read_object(b"\x04\b[\a:\tTesto;\x00\x00")  # type: ignore

    assert result[0] == RubySymbol("Test")
    obb = result[1]
    assert isinstance(obb, GenericRubyUserObject)
    assert obb.name == result[0]


def test_truncated_marshal_stream() -> None:
    with pytest.raises(EOFError):
        read_object(b'\x04\x08"\x07a')


def test_reading_unicode_string() -> None:
    assert (
        read_object(b'\x04\bI"\x12\xe6\x9a\x81\xe5\xb1\xb1 \xe7\x91\x9e\xe5\xb8\x8c\x06:\x06ET')
        == "暁山 瑞希"
    )


def test_reading_symlink_after_objlink() -> None:
    abc = atom("abc")
    def_ = atom("def")
    assert read_object(b"\x04\b[\t[\x06:\babc@\x06:\bdef;\x06") == [[abc], [abc], def_, def_]


def test_unwrapping_dict_keys() -> None:
    assert read_object(b"\x04\b{\x06:\x06ai\x06", unwrap_dict_keys=True) == {"a": 1}


def test_insane_dict_key_unmarshal():
    obb = read_object(b"\x04\b{\x06{\x06i\x06i\ai\b")
    assert isinstance(obb, dict)
    assert next(iter(obb.keys())) == {1: 2}
