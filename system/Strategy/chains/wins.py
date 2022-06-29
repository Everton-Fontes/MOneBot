

from dataclasses import dataclass
from system.Interfaces.represent import Entry, Result
from system.Interfaces.strategy import IStrategy


@dataclass
class CheckWin(IStrategy):

    async def get_entry(self, result: Result, win: bool) -> Entry:
        if win:
            entry = "Big" if result.left_result == "S" else "Small"
            return Entry(entry_type=entry)
        return None
