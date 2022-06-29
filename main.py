
import asyncio
from system.InputControl.cli import CLI
from system.speed_block import MOneBot


def main():
    cli = CLI(bot=MOneBot(False))
    asyncio.run(cli.open_menu())


if __name__ == "__main__":
    main()
