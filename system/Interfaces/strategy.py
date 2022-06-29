from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod
from dataclasses import dataclass
from typing import Any
from system.Interfaces.represent import Entry, Result


@dataclass
class IStrategy(ABC):
    """Represents a Type of Strategy"""

    @abstractmethod
    async def get_entry(self, result: Result, last_entry: Entry) -> Entry:
        """Make the calculations of strategy"""
