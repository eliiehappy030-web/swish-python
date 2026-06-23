from flask import Flask, jsonify, request, send_from_directory
import os
import uuid
from datetime import datetime

app = Flask(__name__, static_folder=".", static_url_path="")

payments = []

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/send", methods=["POST"])
def send_payment():
    data = request.get_json()
    number = data.get("number", "").strip()
    amount = data.get("amount", "").strip()
    message = data.get("message", "").strip()

    if not number or not amount:
        return jsonify({"status": "error", "message": "Nummer och belopp krävs."}), 400

    try:
        amount_float = float(amount)
        if amount_float <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"status": "error", "message": "Ogiltigt belopp."}), 400

    payment = {
        "id": str(uuid.uuid4())[:8].upper(),
        "number": number,
        "amount": amount_float,
        "message": message if message else "Ingen meddelande",
        "time": datetime.now().strftime("%H:%M"),
        "date": datetime.now().strftime("%d %b"),
    }
    payments.insert(0, payment)
    return jsonify({"status": "ok", "payment": payment})

@app.route("/api/history", methods=["GET"])
def get_history():
    return jsonify({"payments": payments})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
