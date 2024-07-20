from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# BulkSMS API configuration
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

def get_attendee_details(api_url, domain_uri):
    url = f"{domain_uri}{api_url}"
    response = requests.get(url)
    return response

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    
    # Log the incoming request data
    app.logger.info("Received data: %s", data)
    
    # Extract the relevant information from the webhook payload
    api_url = data.get('api_url')
    domain_uri = data.get('domain_uri')
    
    if api_url and domain_uri:
        # Fetch attendee details
        attendee_details = get_attendee_details(api_url, domain_uri)
        app.logger.info("Attendee details: %s", attendee_details)
        
        checkin_time = (datetime.now() + timedelta(hours=1)).strftime("%d-%b-%Y %H:%M:%S")
        
        message = f"They checked in to Global STAR 2024 at {checkin_time}."
        response = send_sms("2348029002325", message)
        return jsonify(response)

    else:
        return jsonify({"error": "Missing webhook data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
