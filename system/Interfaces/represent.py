from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Result:
    """
    Represents a result on 77uu.co
    paramns:
        block: int  -> number of block on site
        leftResult: str -> class of the result that apears big | small (B|S)
        rightResult: str -> class of the result that apears single | double (E|O)
    """

    block: int = 1
    left_result: str = "S"
    right_result: str = "O"


@dataclass
class Entry:
    """
    Represents a entry on 77uu.co
    paramns:
        id: int  -> Optional
        entry_type: str ->  big | small | even | odd
        amount: float -> value to enter
    """
    id: int = Optional[int]
    entry_type: str = "small"
    amount: float = 0.1


class Observer(ABC):

    @abstractmethod
    async def update(self) -> None:
        """Represents the update to (self) or observers"""

    async def add(self, observer: Observer):
        self.observers.append(observer)
