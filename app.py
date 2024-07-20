from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

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
    
    # Log the incoming request data
    app.logger.info("Received data: %s", data)
    
    checkin_time = (datetime.now() + timedelta(hours=1)).strftime("%d-%b-%Y %H:%M:%S")
    message = f"They checked in to Global STAR 2024 at {checkin_time}."
    response = send_sms("2348029002325", message)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
