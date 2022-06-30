
import asyncio
from dataclasses import dataclass
import subprocess
import asyncbg
from system.Interfaces.represent import Observer

from system.Interfaces.robot import Robot
from system.arbiters import Arbiter, Consulter
from system.speed_block import MOneBot
from system.utils.files import load_file, save_file


@dataclass
class CLI:
    bot: Robot
    arbiter: Observer = Arbiter()
    consulter: Observer = Consulter("./system/store/results.json")
    started = False
    print_menu = False
    close = False
    printed = False
    proc = None
    user = False

    async def show_menu(self):
        if not self.print_menu:
            print("\nEscolha um número das opções abaixo")
            print()
            for key, item in self.commands.items():
                print(f'{key}. {item["desc"]}:')
            self.print_menu = True

    async def open_menu(self):
        await save_file("./system/store/running.json", {"running": True})
        self.commands = {
            "1": {
                "desc": "Definir Usuário",
                "action": self.save_user
            },
            "2": {
                "desc": "Definir configuraçẽs do robo",
                "action": self.define_configurations
            },
            "3":
            {
                "desc": "Iniciar o bot",
                "action": self.init_bot
            },
            "4":
            {
                "desc": "Fechar Programa",
                "action": self.close_program
            }
        }

        stop = False
        while not stop:
            await self.show_menu()
            choose = input("## ")
            try:
                command = self.commands[choose]
            except KeyError:
                print("Opção inválida")
            else:
                if choose == "4":
                    self.close = True
                    break
                await asyncio.sleep(3)
                await command['action']()
                self.print_menu = False
            await asyncio.sleep(3)
        await self.close_program()

    async def define_configurations(self):
        await self.bot._start()

        self.started = True

    async def save_user(self):
        login_data = await load_file("./system/store/auth.json", debug=False)
        if not login_data:
            print("\nNão foi encontrado um usuário para logar...")
            await self.bot.save_user()

        else:
            username = login_data['username']
            password = login_data['password']
            while True:
                answer = input(
                    f"\nTem um usuário salvo ({username}), deseja utilizar ele? S/N \n").lower()
                match answer:
                    case "s":
                        break
                    case "n":
                        await self.bot.save_user()
                        login_data = await load_file("./system/store/auth.json")
                        username = login_data['username']
                        password = login_data['password']
                        break
                    case _:
                        print("Escolha apenas S ou N")
            await save_file("./system/store/auth.json", {"username": username, "password": password})

        self.user = True

    async def init_bot(self):
        if self.proc:
            if await self.bot._deinnit():
                self.proc.terminate()
                self.proc = None
            else:
                print("O robo já esta funcionando")
                print("Por Favor espere ele carregar")
                return
        if self.started and self.user:
            self.proc = subprocess.Popen(["python", "trade.py"])
        else:
            print("por favor defina as configurações e o usuário primeiro")

    async def close_program(self):
        await self.bot._stop()
        if self.proc:
            await asyncio.sleep(3)
            self.proc.terminate()
            self.proc = None
