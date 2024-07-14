from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

BULKSMS_API_URL = "https://portal.nigeriabulksms.com/api/"
USERNAME = "tcwsecretariat@gmail.com"
PASSWORD = "UFyd6@UxytPXi8"
SENDER_ID = "welcome"

def send_sms(parent_phone, message):
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "message": message,
        "sender": SENDER_ID,
        "mobiles": parent_phone
    }
    response = requests.get(BULKSMS_API_URL, params=payload)
    return response.json()

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    parent_name = data.get('dynamic__116192000000047924')
    parent_phone = data.get('dynamic__116192000000067523')
    attendee_name = data.get('dynamic__116192000000013014')
    order_id = data.get('orderId')
    checkin_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

    if parent_name and parent_phone and attendee_name and order_id:
        message = f"Hello, {parent_name}. You were listed as the parent/guardian of {attendee_name} with ticket order ID {order_id}. They checked in to Global STAR 2024 at {checkin_time}."
        response = send_sms(parent_phone, message)
        return jsonify(response)
    else:
        return jsonify({"error": "Missing data"}), 400

if __name__ == '__main__':
    app.run(debug=True)

