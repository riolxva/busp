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
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from datetime import datetime, timedelta

        
def asd(a):
    if a.json()['basicTripInfo']['vehicleTypeName'] == "Автобус":
        return "🚌 "
    elif a.json()['basicTripInfo']['vehicleTypeName'] == "Троллейбус":
        return "🚎 "
    elif a.json()['basicTripInfo']['vehicleTypeName'] == "Трамвай":
        return "🚃 "
    

def rint():
    x = randint(7900000000,7999999999)
    return x 


def run_every_1_minute():
    while True:
        resp = requests.get("https://busp.onrender.com?дабдаб54")
        print(resp.text)
        time.sleep(120)

        
thread = threading.Thread(target=run_every_1_minute)

thread.daemon = True

thread.start()

white = [ 1749290548, 706686986, 1820132315, 1389182288, 752618557, 1816422993, 1240163871, 7802718619, 943904951 ] 
#             я          саша       марго    ильягаранин   мать       ёмиёри      кира       Игорек      тимурик
TOKEN = "7123200792:AAEUI5j0OhDnDObRIGXCN8NEInwSPSEh5z4"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user.id in white:
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    await message.delete()
    if message.from_user.id in white:
        sp = message.text.split()
        mul = int(sp[1]) if len(sp) == 2 else 1
        data = {"initData":"query_id=AAE0DkRoAAAAADQORGg9OzFj&user=%7B%22id%22%3A1749290548%2C%22first_name%22%3A%224s%F0%9F%A4%A7%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22xva4s2%22%2C%22language_code%22%3A%22ru%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F-YLJccB6b9ek6pGSbp3w3rxjTbDtfodmS15XAqHu65c.svg%22%7D&auth_date=1733844565&signature=7on5VhQOH8o2V0dh8wnZIgVIiyvW5aM3nATKQ-3OOJxgnZpB4hw8hDH0eNCOoSUyxubVpy0kw6Kq72MFVD9VDw&hash=4744f6bb621839f00783969f312b38a9afb6410b4a9f24c9f4c9caaa242eaba4"}
        response = requests.post(f"https://buspaybot.icom24.ru/api/search/qr?botName=buspaybot&scannedCode={sp[0]}", json=data)  
        time = datetime.now() + timedelta(hours=7)
        w = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎫 Предъявить билет", web_app=WebAppInfo(url=f'''https://busp.onrender.com?perevoz={response.json()['basicTripInfo']['carrierName']}&route={response.json()['basicTripInfo']['routeName'].replace('"','@')}&govno={response.json()['basicTripInfo']['vehicleGovNumber']}&cost={response.json()['tariffs'][0]['tariffValueCent']//100*mul}&date={time.day}&hour={str(time.hour).zfill(2)}&min={str(time.minute).zfill(2)}&count={mul}'''))]
        ])
        await message.answer(f"Билет куплен успешно.\n{response.json()['basicTripInfo']['carrierName']}\n🚏 {response.json()['basicTripInfo']['routeName']}\n{asd(response)}{response.json()['basicTripInfo']['vehicleGovNumber']}\n🪙 Тариф: Полный {response.json()['tariffs'][0]['tariffValueCent']*mul//100},00 ₽\n🎫 Билет №{rint()}", reply_markup=w)
    else:
        return

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

