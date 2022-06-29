from dataclasses import dataclass

from system.Interfaces.represent import Entry, Observer, Result


@dataclass
class Robot(Observer):
    _result: Result
    _entry: Entry
    _win: bool
    _count: int

    def entry(self) -> Entry:
        """Represents the entry"""

    @property
    def win(self) -> bool:
        """Represents the win of last entry"""
        return self._win

    @property
    def count(self) -> int:
        """Represents the count of orders"""
        return self._count

    async def _start(self) -> None:
        """Represents the start of bot"""

    async def _deinnit(self) -> None:
        """Represents the deinit of bot"""

    async def _make_entry(self) -> None:
        """Represents the method to make entry"""
