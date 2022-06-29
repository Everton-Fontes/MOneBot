from dataclasses import dataclass
from system.Interfaces.represent import Entry, Result
from system.Interfaces.strategy import IStrategy
from system.Strategy.chains.wins import CheckWin


@dataclass
class CheckLoss(IStrategy):
    async def get_entry(self, result: Result, last_entry: Entry, win: bool) -> Entry:
        entry = await CheckWin().get_entry(result, win)
        entry_type = last_entry.entry_type[0].upper()
        if not entry:
            if entry_type == "B" or entry_type == "S":
                entry = "Odd" if result.right_result == "O" else "Even"
            if entry_type == "O" or entry_type == "E":
                entry = "Big" if result.left_result == "S" else "Small"

            return Entry(entry_type=entry)

        return entry
