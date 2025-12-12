import requests
from licensing.methods import Helpers
from colorama import Fore, Style
import os
import asyncio

machine_code = Helpers.GetMachineCode(v=2)
PASS_FILE = os.path.join(os.path.expanduser("~"), ".ismoiloff_pass.txt")


def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f:
            return f.read().strip()
    pw = input(f"{Fore.YELLOW}Parolni kiriting: {Style.RESET_ALL}")
    with open(PASS_FILE, "w") as f:
        f.write(pw)
    return pw


def run_async_if_needed(namespace):
    if "main" in namespace and asyncio.iscoroutinefunction(namespace["main"]):
        try:
            asyncio.run(namespace["main"]())
        except RuntimeError:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(namespace["main"]())


def runcode(code_value):
    password = get_password()
    url = (
        f"https://new.u11240.xvest3.ru/Device/2.0/getcoder.php?"
        f"pass={password}&device={machine_code}&code={code_value}"
    )

    headers = {"Authorization": "true"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Kodni yuklab olishda xatolik yuz berdi:", response.status_code)
        return

    code = response.text.strip()

    if code == "2":
        print(
            f"{Fore.LIGHTRED_EX}Siz bu kodimizni ishlatishdan BAN olgansiz!\n"
            "@ismoiloff_S ga murojaat qiling "
            f"{Style.RESET_ALL}"
        )
        return

    if code == "0":
        print(
            f"{Fore.LIGHTRED_EX}No'malum device!\n"
            "@ismoiloff_S ga murojaat qiling "
            f"{Style.RESET_ALL}"
        )
        return

    namespace = {}
    try:
        exec(code, namespace)
        run_async_if_needed(namespace)
    except Exception as e:
        print(f"{Fore.RED}Kodda xatolik bor: {e}{Style.RESET_ALL}")
