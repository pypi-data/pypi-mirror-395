from typing import Protocol, TypeVar

T = TypeVar("T", covariant=True)


class Parser(Protocol[T]):
    def parse(self, data: bytes) -> T: ...
