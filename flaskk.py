from flask import Flask, render_template, request
from random import randint
import requests


app = Flask(__name__)


@app.route("/data/", methods=["GET"])
def fetch_ticket_data():
    code = request.args.get("code")
    data = {
            "initData": "query_id=AAH4J3doAgAAAPgnd2j3JsBl&user=%7B%22id%22%3A6047606776%2C%22first_name%22%3A%22%D0%98%D0%BE%D1%81%D0%B8%D1%84%22%2C%22last_name%22%3A%22%D0%9E%D0%B1%D1%80%D1%83%D1%87%D0%BD%D0%B8%D0%BA%22%2C%22username%22%3A%22iosiffffffffff%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FPCoBIep_PONogRkLgAO4JO8rZZ9FtXKMUaJ_mxJamtW4YuAkWVpuafJT0t4mY0vb.svg%22%7D&auth_date=1743497860&signature=RkwFfNGg4fRhNF9sdxSzS9L1dIjN8MGxqWffroH7NZ34W7Jfo7yvq1xNLAF8Dt5yK7RrfvePignNWnHiNgQaAg&hash=3f3e2890e68f8119965676db5836ecbaec1a9c046d43e66bf710cefb722c7fb6"
    }
    response = requests.post(
        f"https://buspaybot.icom24.ru/api/search/qr?botName=buspaybot&scannedCode={code}",
        json=data,
    )
    return response.json()


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
 
