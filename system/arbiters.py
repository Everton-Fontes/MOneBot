"""Contains all the Objects that handle with the result"""
import asyncio
from dataclasses import dataclass, field
import json
from system.Interfaces.represent import Entry, Observer, Result
import nest_asyncio

from system.Strategy.chains.loss import CheckLoss
from system.utils.files import load_file, save_file
nest_asyncio.apply()


@dataclass
class Consulter(Observer):
    """
    Job: Get the result stored in results.json and comunicate
    params:
        observers:list store all objects that depends of the result
        result:Result its the actual result on site
        last_result: its the second result on site, actuay start at a dummy

    methods:
        that has a property result thats when set, comunicate all observers and
        set the last with actual

        _sync_result: Read the file results.json and set the result if its
        diferent
    """
    result_file: str = "./results.json"
    observers: list = field(default_factory=list)
    _result: Result = Result(1, "small", "double")
    last_result: Result = Result(1, "small", "double")

    @property
    def result(self) -> Result:
        return self._result

    async def update(self) -> None:
        await self._sync_result()

    @result.setter
    def result(self, result: Result) -> None:
        # set the diferent
        self._result = result
        self.last_result = self.result

        # comunicate
        for observer in self.observers:
            asyncio.run(observer.update(self.result))

    async def _sync_result(self) -> bool:
        # load a file
        with open(self.result_file, "r") as file:
            data = json.load(file)
        # update if diferent
        result = Result(
            block=int(data['block']),
            left_result=data["leftResult"],
            right_result=data["rightResult"])
        if self.result:
            if self.result.block != result.block:
                self.result = result
                return True
            return False
        else:
            self.result = result
            return True


@dataclass
class Arbiter(Observer):
    """
    Job: Get the result and check how to do the entry:
    cases of entry:
        if result its BO the entry will be S, so if the result its B,
        get the right result E and entry will be E
        if in this case the result its SO then entry will be B

    Parans:
        observers:list store all objects that depends of the entry
        that has a property entry thats when set, comunicate all observers and
        set the last with actual

        and a property result, thats when is set activate the chain to see whats
        the next entry

        strategies:list of strategies to see whats entry will be
    """
    checker = CheckLoss()
    dummy_entry: Entry = Entry()
    _entry: Entry = dummy_entry
    _last_entry: Entry = dummy_entry
    _result: Result = Result()
    last_result: Result = Result()
    observers: list = field(default_factory=list)
    state: bool = False
    first = True

    @property
    def last_entry(self) -> Entry:
        return self._last_entry

    @last_entry.setter
    def last_entry(self, entry: Entry):

        self._last_entry = entry
        win = asyncio.run(self.check_win())
        asyncio.run(self.save_win(win))
        for observer in self.observers:
            asyncio.run(observer.update(win, self.first))

    @ property
    def entry(self) -> Entry:
        return self._entry

    @ entry.setter
    def entry(self, entry: Entry):

        self._entry = entry

        for observer in self.observers:
            observer.entry = self.entry

    @ property
    def result(self) -> Result:
        return self._result

    @ result.setter
    def result(self, result: Result) -> None:
        self.last_result = self.result
        self._result = result

    async def update(self, result: Result) -> None:
        self.result = result

    async def check_win(self) -> bool:
        """Compare result to entry"""
        if self.last_entry == self.dummy_entry:
            self.first = True
            return True
        entry_type = self.last_entry.entry_type[0].upper()
        if entry_type == self.result.left_result:
            self.first = False
            return True
        if entry_type == self.result.right_result:
            self.first = False
            return True
        self.first = False
        return False

    async def save_win(self, win: bool) -> None:
        data = await load_file("./system/store/results.json")
        data['win'] = win
        await save_file("./system/store/results.json", data)

    async def _get_entry(self):
        self.last_entry = self.entry
        win = await self.check_win()
        entry = await self.checker.get_entry(self.result, self.last_entry, win)
        if self.entry == self.dummy_entry:
            last_entry = Entry(entry_type=self.result.left_result)
            entry = await self.checker.get_entry(self.result, last_entry, win)
        # Set entry

        self.entry = entry
