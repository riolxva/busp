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
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from datetime import datetime, timedelta


def vehicle_type(a):
    if a.json()["basicTripInfo"]["vehicleTypeName"] == "Автобус":
        return "🚌"
    elif a.json()["basicTripInfo"]["vehicleTypeName"] == "Троллейбус":
        return "🚎"
    elif a.json()["basicTripInfo"]["vehicleTypeName"] == "Трамвай":
        return "🚃"


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
    if message.from_user.id in white:
        await message.delete()
        sp = message.text.split()
        mul = int(sp[1]) if len(sp) == 2 else 1
        response = requests.get(f"https://busp-1.onrender.com/data?code={sp[0]}")
        time = datetime.now() + timedelta(hours=7)
        ticket_number = f"977 {randint(100, 999)} {randint(100, 999)}"
        w = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎫 Предъявить билет",
                        web_app=WebAppInfo(
                            url=f"""https://busp-1.onrender.com?perevoz={response.json()['basicTripInfo']['carrierName'].replace('"','@').replace(' ', '+')}&route={response.json()['basicTripInfo']['routeName'].replace('"','@').replace(' ', '+')}&govno={response.json()['basicTripInfo']['vehicleGovNumber'].replace(' ', '+')}&cost={response.json()['tariffs'][0]['tariffValueCent']//100*mul}&date={time.day}&hour={str(time.hour).zfill(2)}&min={str(time.minute).zfill(2)}&count={mul}&nomer={str(ticket_number).replace(' ', '+')}"""
                        ),
                    )
                ]
            ]
        )
        await message.answer(
            f"Билет куплен успешно.\n{response.json()['basicTripInfo']['carrierName']}\n🚏 {response.json()['basicTripInfo']['routeName']}\n{vehicle_type(response)} {response.json()['basicTripInfo']['vehicleGovNumber']}\n🪙 Тариф: Полный {response.json()['tariffs'][0]['tariffValueCent']*mul//100},00 ₽\n🎫 Билет № {ticket_number}\n🕑 Действует до {(datetime.now() + timedelta(hours=8, minutes=10)).strftime('%H:%M')}",
            reply_markup=w,
        )
    else:
        return


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
