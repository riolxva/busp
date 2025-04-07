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
            "initData":"query_id=AAGAZRZNAwAAAIBlFk1o_h_S&user=%7B%22id%22%3A7735764352%2C%22first_name%22%3A%22445%22%2C%22last_name%22%3A%22%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FsjwxKvUTfSfXsGLWJIyW5LKdBcgzN7l19jMm26AARcm-LZiddOhqH5IKWrebo1gi.svg%22%7D&auth_date=1744007527&signature=blXHIvw7P6H_22991dsr0vPF5brhBB6wD2e0IVY3UdbTl_hrNmY0OBywaMTMvKjjgWIuyaxFAUUtDIcjg5rWBg&hash=d8843412f7ed686ee0aac1f134262d0329926e1001a8a7dab03fea7291fa2314"
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
 
