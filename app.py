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

# Global variable to store the full URL
full_url = ""

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

@app.route('/', methods=['GET', 'POST'])
def webhook():
    global full_url  # Access the global variable

    if request.method == 'POST':
        data = request.json

        # Log the incoming request data
        app.logger.info("Received data: %s", data)

        # Concatenate domain_uri and api_url to form the full URL
        domain_uri = data.get('domain_uri', '')
        api_url = data.get('api_url', '')

        if domain_uri and api_url:
            full_url = domain_uri + api_url
            app.logger.info("Full URL: %s", full_url)

            # Make a GET request to the full URL
            response = requests.get(full_url)

            # Check if the response was successful
            if response.status_code == 200:
                # Read and log the content of the txt file
                txt_content = response.text
                app.logger.info("Text file content: %s", txt_content)

                # You can process the txt_content here if needed

            else:
                app.logger.error("Failed to fetch content from URL: %s", response.status_code)
        else:
            app.logger.error("Invalid domain_uri or api_url received")

        # Send an SMS notification
        checkin_time = (datetime.now() + timedelta(hours=1)).strftime("%d-%b-%Y %H:%M:%S")
        message = f"They checked in to Global STAR 2024 at {checkin_time}."
        sms_response = send_sms("2348029002325", message)

        return jsonify(sms_response)

    elif request.method == 'GET':
        return jsonify({
            "message": "Welcome to the webhook server! This server only accepts POST requests from Zoho Backstage."
        })

if __name__ == '__main__':
    app.run(debug=True)
