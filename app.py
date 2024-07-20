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
    if response.headers['Content-Type'] == 'text/plain':
        return response.text
    else:
        return None

@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        data = request.json
        
        # Log the incoming request data
        app.logger.info("Received data: %s", data)
        
        # Extract the relevant information from the webhook payload
        api_url = data.get('api_url')
        domain_uri = data.get('domain_uri')
        
        if api_url and domain_uri:
            # Fetch attendee details
            attendee_details = get_attendee_details(api_url, domain_uri)
            if attendee_details:
                app.logger.info("Attendee details: %s", attendee_details)
                
                checkin_time = (datetime.now() + timedelta(hours=1)).strftime("%d-%b-%Y %H:%M:%S")
                
                message = f"They checked in to Global STAR 2024 at {checkin_time}."
                response = send_sms("2348029002325", message)
                return jsonify(response)
            else:
                return jsonify({"error": "Failed to retrieve attendee details or unsupported content type"}), 400

        else:
            return jsonify({"error": "Missing webhook data"}), 400

    elif request.method == 'GET':
        api_url = request.args.get('api_url')
        domain_uri = request.args.get('domain_uri')
        
        if api_url and domain_uri:
            attendee_details = get_attendee_details(api_url, domain_uri)
            if attendee_details:
                return jsonify({"attendee_details": attendee_details})
            else:
                return jsonify({"error": "Failed to retrieve attendee details or unsupported content type"}), 400
        else:
            return jsonify({"error": "Missing required parameters"}), 400

if __name__ == '__main__':
    app.run(debug=True)
