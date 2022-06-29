

import asyncio
from system.speed_block import MOneBot


async def test_check_result(robot: MOneBot):
    left, right, block = await robot.check_result()

    assert left == "S" or left == "B"
    assert right == "E" or right == "O"


async def tests():
    robot = MOneBot()
    async with robot:
        await test_check_result(robot)
    # await robot.update_gale()

if __name__ == "__main__":
    asyncio.run(tests())
