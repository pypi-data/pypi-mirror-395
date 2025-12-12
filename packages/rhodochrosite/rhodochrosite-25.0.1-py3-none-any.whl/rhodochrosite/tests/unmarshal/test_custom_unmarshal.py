from __future__ import annotations

from typing import cast, override

from rhodochrosite.cursor import Cursor
from rhodochrosite.reader import MarshalReader, read_object
from rhodochrosite.ruby import CustomMarshal, RubySymbol, atom
from rhodochrosite.writer import write_object

# class UserMarshal
#    def _dump _
#      Marshal.dump [1, 2, 3]
#    end
#    def _load args
#      Marshal.load args
#    end
# end


class UserMarshal(CustomMarshal):
    def __init__(self, arr: list[int]) -> None:
        self.arr: list[int] = arr

    @property
    @override
    def ruby_class_name(self) -> RubySymbol:
        return atom("UserMarshal")

    @override
    def get_raw_bytes(self) -> bytes:
        return write_object(self.arr)

    @classmethod
    def load_from_data(cls, _: RubySymbol, data: bytes) -> UserMarshal:
        return UserMarshal(cast(list[int], read_object(data)))


def test_reading_custom_marshal_data() -> None:
    reader = MarshalReader(stream=Cursor(b"\x04\bu:\x10UserMarshal\x0f\x04\b[\bi\x06i\ai\b"))
    reader.custom_factories[atom("UserMarshal")] = UserMarshal.load_from_data
    marshalled = reader.next_object()
    assert isinstance(marshalled, UserMarshal)
    assert marshalled.arr == [1, 2, 3]
