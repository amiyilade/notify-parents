from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Temporary storage for the URL extracted from the POST request
extracted_url = None

def get_attendee_details(url):
    response = requests.get(url)
    if response.headers['Content-Type'] == 'text/plain':
        return response.text
    else:
        return None

@app.route('/', methods=['POST'])
def handle_post():
    global extracted_url
    data = request.json
    
    # Log the incoming request data
    app.logger.info("Received data: %s", data)
    
    # Extract the relevant information from the webhook payload
    api_url = data.get('api_url')
    domain_uri = data.get('domain_uri')
    
    if api_url and domain_uri:
        extracted_url = f"{domain_uri}{api_url}"
        app.logger.info("Extracted URL: %s", extracted_url)
        return jsonify({"message": "URL extracted successfully"}), 200
    else:
        return jsonify({"error": "Missing webhook data"}), 400

@app.route('/', methods=['GET'])
def fetch_data():
    global extracted_url
    if extracted_url:
        # Fetch attendee details
        attendee_details = get_attendee_details(extracted_url)
        if attendee_details:
            # Log the contents of the .txt file
            app.logger.info("Attendee details: %s", attendee_details)
            return jsonify({"attendee_details": attendee_details})
        else:
            return jsonify({"error": "Failed to retrieve attendee details or unsupported content type"}), 400
    else:
        return jsonify({"error": "No URL available. Make sure to send a POST request first."}), 400

if __name__ == '__main__':
    app.run(debug=True)
