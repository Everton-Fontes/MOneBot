import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from getpass import getpass
import logging
from typing import Awaitable
from system.Interfaces.represent import Entry, Observer, Result
from system.Interfaces.robot import Robot
from system.utils.files import load_file, save_file
from playwright.async_api import Playwright, async_playwright
from playwright._impl._api_types import TimeoutError


@dataclass
class MOneBot(Robot):
    test: bool
    dummy_result: Result = Result()
    _result: Result = dummy_result
    _entry: Entry = Entry()
    _win: bool = True
    _count: int = 0
    gales: int = 12
    page = None
    observers: list[Observer] = field(default_factory=list)
    amount: list[float] = field(default_factory=list)
    gain_amount: list[float] = field(default_factory=list)
    max_gain: float = 30
    first: bool = True
    wallet: float = 0
    traded = False

    @property
    def entry(self) -> Entry:
        """Represents the entry"""
        return self._entry

    @entry.setter
    def entry(self, entry: Entry) -> Entry:
        """Represents the entry"""
        self._entry = entry
        asyncio.run(self._make_entry())

    @property
    def win(self) -> bool:
        """Represents the win of last entry"""
        return self._win

    @win.setter
    def win(self, win: bool):
        self._win = win
        asyncio.run(self.update_max_gain())

        res = "Gain" if win else "Loss"
        if self.traded:
            self.count = self.count + 1
            if not self.first:
                print(
                    f"Resultado da ultima entrada: {res} - > {self._result.left_result}/{self._result.right_result} ")
            if win:
                if not self.first:
                    self.gain_amount.append(round(
                        (self.gain_amount[-1]*-1)*1.95, 2))
                    print(
                        f"Saldo de ganho do bot {round(sum(self.gain_amount),2)}")
                    if sum(self.gain_amount) >= self.max_gain:
                        print(f"\n Meta Batida! {self.max_gain}")
                        asyncio.run(self._stop())
                self.count = 0
            else:
                if not self.first:
                    print(
                        f"Saldo de ganho do bot {round(sum(self.gain_amount),2)}")

    @ property
    def count(self) -> int:
        """Represents the count of orders"""
        return self._count

    @ count.setter
    def count(self, count: int) -> int:
        """Represents the count of orders"""
        if count >= self.gales:
            if not self.win and self.deinit_gale:
                print(f"Maximo de percas possíveis {self.gales}")
                asyncio.run(self._stop())
            self._count = 0
        else:
            self._count = count
            if not self.traded:
                self._count = count-1

    async def __aenter__(self) -> Playwright:  # setting up a connection
        self.p = await async_playwright().start()
        self.browser = await self.p.chromium.launch(headless=True)
        self.context = await self.browser.new_context()

    # Open new page
        self.page = await self.context.new_page()

    # Go to https://77uu.co/#/
        await self.page.goto("https://77uu.co/#/", timeout=240000)
        print("*"*39)
        print("*                 Bem Vindo!             *")
        print("*"*42)
        await self.login_on_site()
        await asyncio.sleep(10)
        await save_file("./system/store/running.json", {"running": True})
        await self.save_wallet()
        await save_file("./system/store/results.json", {
            "block": 1,
            "leftResult": "S",
            "rightResult": "O",
            "win": False
        })
        return self.page

    async def __aexit__(self, exc_type, exc, tb):  # closing the connection
        try:
            await asyncio.sleep(1)
            await self.context.storage_state(path="./system/store/broser_data.json")
            await self.context.close()
            await self.browser.close()
            await self.p.stop()
        except Exception as e:
            logging.warning("Algo aocnteceu %s", e)
        else:
            logging.info("MOneBot Desligado")

    async def save_amount(self):
        amounts = await load_file("./system/store/amounts.json", debug=False)
        await self.update_gale()
        while True:
            try:
                if amounts:
                    if len(amounts) == self.gales:
                        answer = input(
                            f"Tens salvo estes valores {[amount for amount in amounts.values()]}, deseja utilizar eles? S/N: \n").lower()
                    else:
                        answer = "n"
                else:
                    answer = 'n'
            except Exception as e:
                logging.info("Por favor digite algo %s", e)
            else:
                match answer:
                    case "s":
                        await self.update_amount()
                        break
                    case "n":
                        print("Selecione os valores que deseja")
                        counter = 0
                        vals = {}
                        close = False
                        while counter < self.gales:
                            try:
                                if counter == 1:
                                    while True:
                                        try:
                                            answer = input(
                                                "Deseja multiplicar o restante automaticamente? S/N \n").lower()
                                        except Exception as e:
                                            logging.info(
                                                "Por favor digite algo %s", e)
                                        else:
                                            match answer:
                                                case "s":
                                                    try:
                                                        val = float(
                                                            input(f"Qual o valor para a multiplicação? \n"))
                                                    except ValueError:
                                                        logging.warning(
                                                            "Por favor digite apenas números e utilize . (ponto) ao invés de , (vírgula)")
                                                    else:
                                                        for n in range(1, self.gales):
                                                            vals[n] = round(
                                                                vals[n-1]*val, 2)
                                                        close = True
                                                        break
                                                case "n":
                                                    val = float(
                                                        input(f"Qual o valor para a {counter+1}ª? \n"))
                                                    close = True
                                                    break

                                                case _:
                                                    print(
                                                        "Apenas é possível responder S ou N")

                                else:

                                    val = float(
                                        input(f"Qual o valor para a {counter+1}ª? \n"))
                            except ValueError:
                                logging.warning(
                                    "Por favor digite apenas números e utilize . (ponto) ao invés de , (vírgula)")
                            else:
                                if close:
                                    break
                                vals[counter] = val
                                counter += 1
                        await save_file("./system/store/amounts.json", vals)
                        break
                    case _:
                        print("Apenas é possível responder S ou N")

    async def save_gale(self):
        while True:
            answer = input("Quantos gale deseja?\n")
            try:
                await save_file("./system/store/gale.json", {"gale": int(answer), "deinit_gale": True})

            except ValueError:
                logging.warning("Por favor digite um número inteiro")
            else:
                print(f"Quantidade de gale definida como {answer}")

                answer = input(
                    "Desligar robo se perder ultimo gale? S/N\n").upper()
                try:
                    gale = await load_file("./system/store/gale.json", debug=False)
                    gale['deinit_gale'] = True if answer == "S" else False

                except Exception:
                    logging.warning("Por favor digite S ou N")
                else:
                    await save_file("./system/store/gale.json", gale)
                    print(f"Ok.")

                break

    async def save_max_gain(self):
        while True:
            answer = input("Qual a porcentagem maxima de ganho para hoje?\n")
            try:
                wallet = await load_file("./system/store/wallet.json", debug=False)
                if wallet:
                    wallet['max_gain'] = float(answer)
                else:
                    wallet = {"wallet": 205, "max_gain": float(answer)}
                await save_file("./system/store/wallet.json", wallet)

            except ValueError:
                logging.warning(
                    "Por favor digite apenas números e utilize . (ponto) ao invés de , (vírgula)")
            else:
                print(
                    f"Ganho máximo definido como {answer}%")
                break

    async def save_wallet(self):
        amount = float(await self.page.locator("body > div.page-view > div.page-content > div.guessBlock > div.center > div > div > div.betBox > div.betInfo > div:nth-child(1) > div:nth-child(1) > span.balance").text_content())
        wallet = await load_file("./system/store/wallet.json", debug=False)
        if wallet:
            wallet['start_balance'] = amount
        else:
            wallet = {"start_balance": amount}
        await save_file("./system/store/wallet.json", wallet)
        self.wallet = amount if not self.test else 205

    async def update_gale(self):
        data = await load_file("./system/store/gale.json")
        if data:
            self.gales = int(data['gale'])
            self.deinit_gale = data['deinit_gale']

    async def update_max_gain(self):
        wallet = await load_file("./system/store/wallet.json", debug=False)
        if wallet:
            self.max_gain = round(
                (self.wallet*float(wallet['max_gain']))/100, 2)

    async def update_amount(self):
        amounts = await load_file("./system/store/amounts.json")
        if not amounts:
            await self.save_amount()
            amounts = await load_file("./system/store/amounts.json")
        self.amount = [amount for amount in amounts.values()]

    async def update(self, win: bool, first: bool = True):
        self.first = first
        self.win = win

    async def _start(self) -> None:
        """Represents the start of bot"""

        # set the bot runing

        await self.save_gale()
        await self.save_amount()

        await self.save_max_gain()

        print()

    async def _deinnit(self) -> None:
        """Represents the deinit of bot"""
        run = await load_file("./system/store/running.json")
        if run["running"]:
            return False
        return True

    async def _stop(self) -> None:
        print("Desligando MOneBot")
        await save_file("./system/store/running.json", {"running": False})

    async def check_timeout_entry(self, locator: Awaitable):
        try:
            await locator
        except TimeoutError:
            await self._make_entry()

    async def _make_entry(self) -> None:
        """Represents the method to make entry"""
        if not self.page:
            print("Primeiro inicie o bot")

        if not await self._deinnit() and self._result != self.dummy_result:

            if datetime.now().second < 40:
                await self.check_timeout_entry(self.page.locator(
                    f"text={self.entry.entry_type.capitalize()} 1.9500x").click())
                # Click [placeholder="Amount of per bet"]
                await self.check_timeout_entry(self.page.locator(
                    "[placeholder=\"Amount of per bet\"]").click())

                # Fill [placeholder="Amount of per bet"]
                await self.check_timeout_entry(self.page.locator(
                    "[placeholder=\"Amount of per bet\"]").fill(str(self.amount[self.count])))
                try:
                    # Click text=Bet Now
                    await self.page.locator("text=Bet Now").click()

                    # Click button:has-text("OK") >> nth=1
                    await self.page.locator("button:has-text(\"OK\")").nth(1).click()
                except TimeoutError:
                    print("Não foi possível fazer a aposta")
                    self.traded = False
                else:
                    print(
                        f"\nEntrada {self.entry.entry_type}, valor: {self.amount[self.count]} - {str(datetime.now().time())[:8]}")
                    self.gain_amount.append(-self.amount[self.count])
                    self.traded = True

    @ staticmethod
    async def save_user() -> None:
        print("Vamos definir um usuário..")
        username = input("Qual o username?\n")
        password = getpass("Qual o password?\n")
        await save_file("./system/store/auth.json", {"username": username, "password": password})

    async def get_user(self) -> tuple[str, str]:
        login_data = await load_file("./system/store/auth.json")
        if not login_data:
            print("\nNão foi encontrado um usuário para logar...")
            await self._stop()

        else:
            username = login_data['username']
            password = login_data['password']
            return (username, password,)

    async def login_on_site(self):
        if not self.page:
            print("Primeiro inicie o bot")

        username, password = await self.get_user()
        print("Iniciando Login")
        await self.page.locator("text=Log In").click()
        # await expect(page).to_have_url("https://77uu.co/#/login")

        # Click [placeholder="Enter the username"]
        await self.page.locator("[placeholder=\"Enter the username\"]").click()

        # Fill [placeholder="Enter the username"]
        await self.page.locator("[placeholder=\"Enter the username\"]").fill(username)

        # Press Tab
        await self.page.locator("[placeholder=\"Enter the username\"]").press("Tab")

        # Fill [placeholder="Enter the password"]
        await self.page.locator("[placeholder=\"Enter the password\"]").fill(password)

        # Press Enter
        # async with page.expect_navigation(url="https://77uu.co/#/uc/safe"):
        async with self.page.expect_navigation():
            await self.page.locator("[placeholder=\"Enter the password\"]").press("Enter")

        # Go to https://77uu.co/#/gameCenter
        await self.page.goto("https://77uu.co/#/gameCenter?gameName=CQK1M", timeout=240000)

    async def check_result(self) -> None:
        await self.update_amount()
        await self.update_gale()
        # Primeira linha
        # esquerda
        # Click left result
        left = await self.page.locator("div.issueItem:nth-child(1) > span:nth-child(4) > b:nth-child(1)").text_content(timeout=150000)
        # direita
        # Click right result
        right = await self.page.locator("div.issueItem:nth-child(1) > span:nth-child(4) > b:nth-child(2)").text_content(timeout=150000)
        # tempo
        # Click blick number
        block = await self.page.locator("div.issueItem:nth-child(1) > span:nth-child(1)").text_content(timeout=150000)
        # primeira linha
        last_result = await load_file("./system/store/results.json")
        if int(block) != last_result['block']:
            new_result = {
                "block": int(block),
                "leftResult": left,
                "rightResult": right,
                "win": last_result['win']
            }
            if not self.first:
                self._result = Result(
                    int(block),
                    left,
                    right
                )
            await save_file("./system/store/results.json", new_result)
        return (left, right, block,)
