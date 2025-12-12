import math

import pytest

from rhodochrosite.exc import NotAMarshalFile
from rhodochrosite.reader import MarshalReader, read_object
from rhodochrosite.ruby import RubyClassReference, RubySpecialInstance, RubySymbol


def test_valid_magic_number() -> None:
    MarshalReader.from_bytes(b"\x04\x08")


def test_invalid_magic_number() -> None:
    with pytest.raises(NotAMarshalFile):
        MarshalReader.from_bytes(b"123")


def test_reading_booleans() -> None:
    assert read_object(b"\x04\x08T") is True
    assert read_object(b"\x04\x08F") is False


def test_reading_nils() -> None:
    assert read_object(b"\x04\b0") is None


def test_reading_multiple() -> None:
    reader = MarshalReader.from_bytes(b"\x04\x08TF0")
    assert (reader.next_object(), reader.next_object(), reader.next_object()) == (True, False, None)


def test_reading_fixed_zero() -> None:
    assert read_object(b"\x04\bi\x00") == 0


def test_reading_small_fixnums() -> None:
    """
    Tests reading small, single-byte fixnums.
    """

    assert read_object(b"\x04\bi\x11") == 12
    assert read_object(b"\x04\bi\xef") == -12


def test_reading_size_1_fixnums() -> None:
    assert read_object(b"\x04\bi\x01{") == 123
    assert read_object(b"\x04\bi\xff\x7f") == -129


def test_reading_size_2_fixnums() -> None:
    assert read_object(b"\x04\bi\x02\xe8\x80") == 33000
    assert read_object(b"\x04\bi\xfe\x18\x7f") == -33000
    assert read_object(b"\x04\bi\x02\xd2\x04") == 1234
    assert read_object(b"\x04\bi\xfe.\xfb") == -1234


def test_reading_size_3_fixnums() -> None:
    assert read_object(b"\x04\bi\x03\xf2O\xbc") == 12341234
    assert read_object(b"\x04\bi\xfd\x0e\xb0C") == -12341234


def test_reading_symbols() -> None:
    assert read_object(b"\x04\b:\tabdc") == RubySymbol(value="abdc")
    # synthetic marshal, as Marshal.dump doesn't let you (easily) just dump two symbols in a row
    # without a list.
    reader = MarshalReader.from_bytes(b"\x04\b:\tabdc;\x00")
    sym = reader.next_object()
    assert reader.next_object() == sym


def test_reading_raw_string() -> None:
    assert read_object(b'\x04\b"\babc') == b"abc"


def test_reading_wrapped_string() -> None:
    assert read_object(b'\x04\bI"\ttest\x06:\x06ET') == "test"


def test_reading_string_without_unwrapping() -> None:
    instance = read_object(b'\x04\bI"\ttest\x06:\x06ET', unwrap_strings=False)
    assert isinstance(instance, RubySpecialInstance)
    assert instance.base_object == b"test"
    assert instance.instance_variables == [(RubySymbol(value="E"), True)]


def test_reading_array() -> None:
    result = read_object(b'\x04\b[\bi\x06I"\babc\x06:\x06ET[\ai\aI"\bdef\x06;\x00T')
    assert result == [1, "abc", [2, "def"]]


def test_reading_hashes() -> None:
    assert read_object(b"\x04\b{\x06i\x06i\a") == {1: 2}
    assert read_object(b"\x04\b{\x06:\babci\x06") == {RubySymbol(value="abc"): 1}


def test_reading_class_reference() -> None:
    assert read_object(b"\x04\bc\tTest") == RubyClassReference(value=RubySymbol(value="Test"))


def test_reading_floats() -> None:
    assert read_object(b"\x04\bf\x062") == 2.0
    assert read_object(b"\x04\bf\binf") == float("inf")

    nan = read_object(b"\x04\bf\bnan")
    assert isinstance(nan, float)
    assert math.isnan(nan)


def test_reading_object_links() -> None:
    hash = {RubySymbol("a"): 1}

    assert read_object(b"\x04\b[\a[\a{\x06:\x06ai\x06@\a@\x06") == [[hash, hash], [hash, hash]]


def test_forcibly_decoding_string() -> None:
    assert read_object(b'\x04\b"\tmiku', decode_all_strings=True) == "miku"
