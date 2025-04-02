import asyncio
import logging
import sys
import requests
from random import randint
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def rint():
    return f"977 {randint(100, 999)} {randint(100, 999)}"


white = [ 1749290548, 706686986, 1820132315, 1389182288, 752618557, 1816422993, 943904951, 5025077400, 952619704, 630120548, 1690631961, 1429180981 ] 
#             я          саша      марго     ильягаранин    мать      ёмиёри     тимурик     Диана        Дима      володя     серега     петька
TOKEN = "7123200792:AAEUI5j0OhDnDObRIGXCN8NEInwSPSEh5z4"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user.id in white:
        button1 = KeyboardButton(text="Купить билет")
        button2 = KeyboardButton(text="Действующие билеты")
        button3 = KeyboardButton(text="Подписка СБП")
        button4 = KeyboardButton(text="Ещё...")
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[button1, button2], 
                      [button3, button4]], 
            resize_keyboard=True
        )
        await message.answer(
            f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=keyboard
        )


@dp.message()
async def echo_handler(message: Message) -> None:
    if (user_id := message.from_user.id) in white:
        await message.delete()
        sp = message.text.split()
        count = int(sp[1]) if len(sp) == 2 else 1
        requests.get(f"https://busp-1.onrender.com/data?code={sp[0]}&count={count}&userid={user_id}")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
