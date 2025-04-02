import asyncio
import logging
import sys
import requests
import time
import threading
from random import randint
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

        
def asd(a):
    if a.json()['basicTripInfo']['vehicleTypeName'] == "Автобус":
        return "🚌 "
    elif a.json()['basicTripInfo']['vehicleTypeName'] == "Троллейбус":
        return "🚎 "
    elif a.json()['basicTripInfo']['vehicleTypeName'] == "Трамвай":
        return "🚃 "
    

def rint():
  return f"977 {randint(100, 999)} {randint(100, 999)}"


white = [ 1749290548, 706686986, 1820132315, 1389182288, 752618557, 1816422993, 943904951, 5025077400, 952619704, 630120548, 1690631961, 1429180981 ] 
#             я          саша      марго     ильягаранин    мать      ёмиёри     тимурик     Диана        Дима      володя     серега     петька
TOKEN = "7123200792:AAEUI5j0OhDnDObRIGXCN8NEInwSPSEh5z4"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user.id in white:
        button1 = KeyboardButton(text='Купить билет')
        button2 = KeyboardButton(text='Действующие билеты')
        button3 = KeyboardButton(text='Подписка СБП')
        button4 = KeyboardButton(text='Ещё...')
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[button1, button2], [button3, button4]],  
            resize_keyboard=True  
        )
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!",reply_markup=keyboard)
        


@dp.message()
async def echo_handler(message: Message) -> None:
    if message.from_user.id in white:
        jopa = rint()
        await message.delete()
        sp = message.text.split()
        mul = int(sp[1]) if len(sp) == 2 else 1
        data = {"initData": "query_id=AAH4J3doAgAAAPgnd2j3JsBl&user=%7B%22id%22%3A6047606776%2C%22first_name%22%3A%22%D0%98%D0%BE%D1%81%D0%B8%D1%84%22%2C%22last_name%22%3A%22%D0%9E%D0%B1%D1%80%D1%83%D1%87%D0%BD%D0%B8%D0%BA%22%2C%22username%22%3A%22iosiffffffffff%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FPCoBIep_PONogRkLgAO4JO8rZZ9FtXKMUaJ_mxJamtW4YuAkWVpuafJT0t4mY0vb.svg%22%7D&auth_date=1743497860&signature=RkwFfNGg4fRhNF9sdxSzS9L1dIjN8MGxqWffroH7NZ34W7Jfo7yvq1xNLAF8Dt5yK7RrfvePignNWnHiNgQaAg&hash=3f3e2890e68f8119965676db5836ecbaec1a9c046d43e66bf710cefb722c7fb6"}
        response = requests.post(f"https://buspaybot.icom24.ru/api/search/qr?botName=buspaybot&scannedCode={sp[0]}", json=data)  
        time = datetime.now() + timedelta(hours = 7)
        w = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎫 Предъявить билет", web_app=WebAppInfo(url=f'''https://busp-1.onrender.com?perevoz={response.json()['basicTripInfo']['carrierName'].replace('"','@').replace(' ', '+')}&route={response.json()['basicTripInfo']['routeName'].replace('"','@').replace(' ', '+')}&govno={response.json()['basicTripInfo']['vehicleGovNumber'].replace(' ', '+')}&cost={response.json()['tariffs'][0]['tariffValueCent']//100*mul}&date={time.day}&hour={str(time.hour).zfill(2)}&min={str(time.minute).zfill(2)}&count={mul}&nomer={str(jopa).replace(' ', '+')}'''))]
        ])
        await message.answer(f"Билет куплен успешно.\n{response.json()['basicTripInfo']['carrierName']}\n🚏 {response.json()['basicTripInfo']['routeName']}\n{asd(response)}{response.json()['basicTripInfo']['vehicleGovNumber']}\n🪙 Тариф: Полный {response.json()['tariffs'][0]['tariffValueCent']*mul//100},00 ₽\n🎫 Билет № {jopa}\n🕑 Действует до {(datetime.now() + timedelta(hours=8, minutes=10)).strftime('%H:%M')}", reply_markup=w)
    else:
        return 

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

