from flask import Flask, render_template, request, jsonify
from random import randint
import requests
import json
from datetime import datetime, timedelta, timezone


white = [ 1749290548, 706686986, 1820132315, 1389182288, 752618557, 943904951, 5025077400, 952619704, 630120548, 1690631961, 1429180981, 2125373340 ] 
#             я          саша      марго     ильягаранин    мать      тимурик     Диана        Дима      володя     серега     петька     удалить завтра
TOKEN = "7123200792:AAEUI5j0OhDnDObRIGXCN8NEInwSPSEh5z4"


def vehicle_type(a):
    if a == "Автобус":
        return "🚌"
    elif a == "Троллейбус":
        return "🚎"
    elif a == "Трамвай":
        return "🚃"
    
#"query_id=AAHYc7VhAwAAANhztWH-D-s0&user=%7B%22id%22%3A8081732568%2C%22first_name%22%3A%22%D0%B5%D1%80%D0%BC%D0%B0%D0%B0%D1%80%D0%BE%22%2C%22last_name%22%3A%22%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FI6IuWBpzFecTROIkp-DtS4rq7dVJg1bfKy9hbT3ee-uY8DvSEA7qThp3oEqGlClS.svg%22%7D&auth_date=1744208772&signature=JHk-7KuRIvzaegfxJ4J4okhaI6m2J8qF7EkGV5MTg6sv4OB43F9C2x7-vHMl0hsmAezMrVyerf8QllaEtAh_DQ&hash=c1b18db9c140489a6be54ffc07d69edad0b7495617a500234540a4d75df7fd29"
def get_vehicle_data(code):
    data = {
            "initData":"query_id=AAGAZRZNAwAAAIBlFk1o_h_S&user=%7B%22id%22%3A7735764352%2C%22first_name%22%3A%22445%22%2C%22last_name%22%3A%22%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FsjwxKvUTfSfXsGLWJIyW5LKdBcgzN7l19jMm26AARcm-LZiddOhqH5IKWrebo1gi.svg%22%7D&auth_date=1744007527&signature=blXHIvw7P6H_22991dsr0vPF5brhBB6wD2e0IVY3UdbTl_hrNmY0OBywaMTMvKjjgWIuyaxFAUUtDIcjg5rWBg&hash=d8843412f7ed686ee0aac1f134262d0329926e1001a8a7dab03fea7291fa2314"
    }
    response = requests.post(
        f"https://buspaybot.icom24.ru/api/search/qr?botName=buspaybot&scannedCode={code}",
        json=data,
    )
    return response


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)


def delete_message(chat_id, message_id):
    url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    requests.post(url, json=payload)


app = Flask(__name__)


@app.route("/data", methods=["POST"])
def fetch_ticket_data():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        message_id = data['message']['message_id']
        text = data['message'].get('text', '').split()
        code = text[0]
        count = int(text[1]) if len(text) == 2 and text[1].isdigit() else 1

    if chat_id in white:
        delete_message(chat_id, message_id)

        try:
            with open("codes.json", "r", encoding='utf-8') as codes:
                cached_codes = json.load(codes)
        except (FileNotFoundError, json.JSONDecodeError):
            cached_codes = {}

        if code in cached_codes:
            response = cached_codes[code]
        else:
            response = get_vehicle_data(code)
            if response.status_code != 200:
                send_message(chat_id, "Ошибка получения данных. Попробуйте позже.")
                return jsonify({"status": "error"}), 200
            cached_codes[code] = response.json()
            with open("codes.json", "w", encoding='utf-8') as codes:
                json.dump(cached_codes, codes, indent=4)

        time = datetime.now(timezone(timedelta(hours=7)))
        ticket_number = f"977 {randint(100, 999)} {randint(100, 999)}"

        info = response["basicTripInfo"]
        tariffs = response['tariffs'][0]
        
        post_data = {
            "chat_id": chat_id,
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
        return jsonify({"status": "ok"}), 200


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

