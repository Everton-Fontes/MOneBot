import json
from asyncio import run

from system.arbiters import Consulter


def load_file():
    with open("test_result.json", "r") as f:
        return json.load(f)


def test_sync_result(c: Consulter):
    data = load_file()
    run(c._sync_result())
    assert int(data['block']) == c.result.block
    assert data['leftResult'] == c.result.left_result
    assert data['rightResult'] == c.result.right_result


if __name__ == "__main__":
    consulter = Consulter("test_result.json")
    test_sync_result(consulter)
