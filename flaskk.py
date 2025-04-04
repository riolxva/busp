from flask import Flask, render_template, request
from random import randint
import requests
import json
from datetime import datetime, timedelta, timezone


def vehicle_type(a):
    if a == "Автобус":
        return "🚌"
    elif a == "Троллейбус":
        return "🚎"
    elif a == "Трамвай":
        return "🚃"


app = Flask(__name__)


@app.route("/data/", methods=["GET"])
def fetch_ticket_data():
    code = request.args.get("code")
    count = request.args.get("count")
    userid = request.args.get("userid")

    time = datetime.now(timezone(timedelta(hours=7)))
    ticket_number = f"977 {randint(100, 999)} {randint(100, 999)}"

    data = {
            "initData":"query_id=AAEZvLYzAwAAABm8tjN7BtFP&user=%7B%22id%22%3A7310064665%2C%22first_name%22%3A%22Grisha%22%2C%22last_name%22%3A%22Markovkin%22%2C%22username%22%3A%22Markovkincosinus11pina6%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1722363617&hash=3723cb1bdf27e20eed7071b1ceb8fec7612b46c4edbb6e9fdee7e97f8c40da6c"
    }
    response = requests.post(
        f"https://buspaybot.icom24.ru/api/search/qr?botName=buspaybot&scannedCode={code}",
        json=data,
    ).json()


    info = response["basicTripInfo"]
    tariffs = response['tariffs'][0]
    
    post_data = {
        "chat_id": int(userid),
        "text": f"Билет куплен успешно.\n{info['carrierName']}\n🚏 {info['routeName']}\n{vehicle_type(info['vehicleTypeName'])} {info['vehicleGovNumber']}\n🪙 Тариф: Полный {tariffs['tariffValueCent']*int(count)//100},00 ₽\n🎫 Билет № {ticket_number}\n🕑 Действует до {(time + timedelta(hours=1, minutes=10)).strftime('%H:%M')}",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🎫 Предъявить билет",
                        "web_app": {
                            "url": f"""https://busp-1.onrender.com?perevoz={info['carrierName'].replace('"','@').replace(' ', '+')}&route={info['routeName'].replace('"','@').replace(' ', '+')}&govno={info['vehicleGovNumber'].replace(' ', '+')}&cost={tariffs['tariffValueCent']//100*int(count)}&date={time.day}&hour={str(time.hour).zfill(2)}&min={str(time.minute).zfill(2)}&count={count}&nomer={str(ticket_number).replace(' ', '+')}"""
                        }
                    }
                ]
            ]
        }
    }

    requests.post("https://api.telegram.org/bot7123200792:AAEUI5j0OhDnDObRIGXCN8NEInwSPSEh5z4/sendMessage", json=post_data)
    return {"status": 200}


@app.route("/", methods=["GET"])
def generate_ticket():
    perevoz = request.args.get("perevoz")
    route = request.args.get("route")
    govno = request.args.get("govno")
    cost = request.args.get("cost")
    date = request.args.get("date")
    hour = request.args.get("hour")
    min = request.args.get("min")
    count = request.args.get("count")
    jopa = request.args.get("nomer")
    return render_template("index.html", perevoz=str(perevoz).replace("@", '"'), route=str(route).replace("@", '"'), govno=govno, cost=cost, date=date, hour=hour, min=min, count=count, jopa=jopa)


app.run(host='0.0.0.0', port=5000)
 
