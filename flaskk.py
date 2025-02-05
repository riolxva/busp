from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/", methods =["GET"])
def popakaka():
    perevoz = request.args.get("perevoz")
    route = request.args.get("route")
    govno = request.args.get("govno")
    cost = request.args.get("cost")
    date = request.args.get("date")
    hour = request.args.get("hour")
    min = request.args.get("min")
    count = request.args.get("count")
    return render_template("index.html", perevoz=str(perevoz).replace("@", '"'), route=str(route).replace("@", '"'), govno=govno, cost=cost, date=date, hour=hour, min=min, count=count)


app.run(host='0.0.0.0', port=5000)
 
