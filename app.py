from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import logging
import json

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

def prettify_json(json_content):
    return json.dumps(json_content, indent=4)

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    
    # Log the incoming request data
    app.logger.info("Received data: %s", data)
    
    # Extract domain and API URL
    domain_url = data.get('domain_url')
    api_url = data.get('api_url')
    
    if domain_url and api_url:
        full_url = f"{domain_url}{api_url}"
        
        try:
            response = requests.get(full_url)
            response.raise_for_status()
            json_content = response.json()
            pretty_json = prettify_json(json_content)
            
            # Log the prettified JSON content
            app.logger.info("Prettified JSON content from %s: %s", full_url, pretty_json)
        except requests.RequestException as e:
            app.logger.error("Error fetching JSON from %s: %s", full_url, str(e))
            return jsonify({"error": "Failed to fetch JSON from URL"}), 500
    
    checkin_time = (datetime.now() + timedelta(hours=1)).strftime("%d-%b-%Y %H:%M:%S")
    message = f"They checked in to Global STAR 2024 at {checkin_time}."
    response = send_sms("2348029002325", message)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
