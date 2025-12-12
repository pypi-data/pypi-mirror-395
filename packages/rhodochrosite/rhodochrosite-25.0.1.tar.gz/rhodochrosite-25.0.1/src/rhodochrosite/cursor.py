from collections.abc import Iterator
from contextlib import contextmanager

import attrs


@attrs.define(slots=True, kw_only=False)
class Cursor:
    wrapped: bytes = attrs.field()
    cursor: int = attrs.field(init=False, default=0)

    def read(self, count: int) -> bytes:
        slice = self.wrapped[self.cursor : self.cursor + count]
        self.cursor += count
        return slice

    @contextmanager
    def with_seeked_to(self, seeked: int) -> Iterator[None]:
        old_cur = self.cursor
        self.cursor = seeked
        try:
            yield
        finally:
            self.cursor = old_cur
