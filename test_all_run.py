

import asyncio
from system.arbiters import Arbiter, Consulter

from system.speed_block import MOneBot


async def test_deInit():
    consulter = Consulter("./system/store/results.json")
    arbiter = Arbiter()
    robot = MOneBot(test=True)
    await consulter.add(arbiter)
    await arbiter.add(robot)
    async with robot:
        await robot._start()
        while True:
            deinit = await robot._deinnit()
            if deinit:
                break
            await asyncio.sleep(5)
            await robot._stop()
        assert deinit == True


async def tests():
    consulter = Consulter("./system/store/results.json")
    arbiter = Arbiter()
    robot = MOneBot(test=True)
    await consulter.add(arbiter)
    await arbiter.add(robot)
    async with robot:
        await robot._start()
        while True:
            deinit = await robot._deinnit()
            if deinit:
                break
            await robot.check_result()
            result = await consulter._sync_result()
            if result:
                await arbiter._get_entry()
            await asyncio.sleep(1)
    # await robot.update_gale()

if __name__ == "__main__":
    asyncio.run(tests())
