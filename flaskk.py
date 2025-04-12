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
    

def get_vehicle_data(code):
    data = {
            "initData":"query_id=AAGUJdhMAwAAAJQl2Ew2M4HW&user=%7B%22id%22%3A7731684756%2C%22first_name%22%3A%22Jos%C3%A9%20%F0%9F%87%B5%F0%9F%87%B8%22%2C%22last_name%22%3A%22%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FA5gihtv78BEIUPaTsOVfWIzy07vlqOkm7c34N5CvNqve2EPCkvdMW9dhGERN48pu.svg%22%7D&auth_date=1744457832&signature=z04e27N9SA6vLkjV7Az1fa79t2IlnAoIK3iknVez6zfGJZZeQvepnpwyXFtXO7yXnrucTXnnpKa8TsHDTUz8Cg&hash=c1f8865a0ffaab6435963132a7dceb5ac84ba15ff38faeea19c9db1743e118ae"
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

