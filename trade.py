
import asyncio
from system.arbiters import Arbiter, Consulter
from system.speed_block import MOneBot


async def run():
    consulter = Consulter("./system/store/results.json")
    arbiter = Arbiter()
    robot = MOneBot(test=False)
    print("Checando configurações...")
    print("Aguarde...")
    await consulter.add(arbiter)
    await arbiter.add(robot)
    async with robot:
        print("Login realizado, checando entradas")
        while True:
            deinit = await robot._deinnit()
            if deinit:
                break
            await robot.check_result()
            result = await consulter._sync_result()
            if result:
                await arbiter._get_entry()
            await asyncio.sleep(1)


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
