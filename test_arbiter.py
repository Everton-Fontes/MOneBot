import json
from asyncio import run
from system.Interfaces.represent import Entry
from system.arbiters import Consulter, Arbiter


def load_file():
    with open("test_result.json", "r") as f:
        return json.load(f)


def save_file(data: dict):
    with open("test_result.json", "w") as f:
        f.write(json.dumps(data))


def test_check_win():
    data = {
        "block": "06221212",
        "leftResult": "B",
        "rightResult": "O"
    }

    save_file(data)
    entry_dummy = Entry(entry_type="Odd")
    c = Consulter("test_result.json")
    a = Arbiter(_last_entry=entry_dummy)
    run(c.add(a))
    assert a.last_entry.entry_type == "Odd"
    run(c._sync_result())

    assert run(a.check_win()) == True


def test_change_orders():
    entry = Entry(entry_type="Small")
    # print("Primeira entrada S")

    c = Consulter("test_result.json")
    a = Arbiter(_last_entry=entry)
    run(c.add(a))

    data = {
        "block": "06221212",
        "leftResult": "B",
        "rightResult": "O"
    }

    save_file(data)
    assert a.last_entry.entry_type == "Small"
    run(c._sync_result())
    run(a._get_entry())
    assert a.entry.entry_type == "Odd"

    data = {
        "block": "06221213",
        "leftResult": "B",
        "rightResult": "E"
    }

    save_file(data)
    run(c._sync_result())
    run(a._get_entry())
    assert a.entry.entry_type == "Small"

    data = {
        "block": "06221214",
        "leftResult": "B",
        "rightResult": "E"
    }

    save_file(data)
    run(c._sync_result())
    run(a._get_entry())
    assert a.entry.entry_type == "Even"

    data = {
        "block": "06221215",
        "leftResult": "B",
        "rightResult": "E"
    }

    save_file(data)
    run(c._sync_result())
    run(a._get_entry())
    assert a.entry.entry_type == "Small"

    data = {
        "block": "06221216",
        "leftResult": "S",
        "rightResult": "E"
    }

    save_file(data)
    run(c._sync_result())
    run(a._get_entry())
    assert a.entry.entry_type == "Big"

    data = {
        "block": "06221217",
        "leftResult": "S",
        "rightResult": "O"
    }

    save_file(data)
    run(c._sync_result())
    run(a._get_entry())
    assert a.entry.entry_type == "Odd"

    data = {
        "block": "06221218",
        "leftResult": "S",
        "rightResult": "E"
    }

    save_file(data)
    run(c._sync_result())
    run(a._get_entry())
    assert a.entry.entry_type == "Big"


if __name__ == "__main__":

    test_check_win()
    test_change_orders()
