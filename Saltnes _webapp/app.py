from flask import Flask, render_template, request, jsonify
import math
from datetime import datetime
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("KJØRER FRA:", os.getcwd())

app = Flask(__name__)

PRISER = {
    "B20": 55,
    "B30": 80,
    "B35": 109,
    "MEGAPLAN": 91
}

SEKK_VOLUM = {
    "B20": 0.012,
    "B30": 0.012,
    "B35": 0.012,
    "MEGAPLAN": 0.010
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/beregn", methods=["POST"])
def beregn():
    d = request.json

    lengde = float(d["lengde"])
    bredde = float(d["bredde"])
    tykkelse = float(d["tykkelse"])
    materiale = d["materiale"]

    areal = lengde * bredde
    volum = areal * (tykkelse / 100)

    sekker = math.ceil(volum / SEKK_VOLUM[materiale])
    pris = sekker * PRISER[materiale]

    ps = (
        "PS: Husk primer, membran og korrekt fall mot sluk 💧"
        if materiale == "MEGAPLAN"
        else "PS: 2–3 øl mens det herder 🍺"
    )

    return jsonify({
        "areal": round(areal, 2),
        "volum": round(volum, 3),
        "sekker": sekker,
        "pris": pris,
        "ps": ps
    })

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    tekst = data.get("tekst", "").strip()

    if not tekst:
        return {"status": "empty"}, 400

    # NB: anbefalt mappe pga OneDrive
    with open("data/feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}]\n{tekst}\n---\n")

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
