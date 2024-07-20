from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_attendee_details(api_url, domain_uri):
    url = f"{domain_uri}{api_url}"
    response = requests.get(url)
    if response.headers['Content-Type'] == 'text/plain':
        return response.text
    else:
        return None

@app.route('/', methods=['GET'])
def webhook():
    # Extract domain_uri and api_url from query parameters
    domain_uri = request.args.get('domain_uri')
    api_url = request.args.get('api_url')
    
    if domain_uri and api_url:
        # Fetch attendee details
        attendee_details = get_attendee_details(api_url, domain_uri)
        if attendee_details:
            # Log the contents of the .txt file
            app.logger.info("Attendee details: %s", attendee_details)
            return jsonify({"attendee_details": attendee_details})
        else:
            return jsonify({"error": "Failed to retrieve attendee details or unsupported content type"}), 400
    else:
        return jsonify({"error": "Missing required parameters"}), 400

if __name__ == '__main__':
    app.run(debug=True)
