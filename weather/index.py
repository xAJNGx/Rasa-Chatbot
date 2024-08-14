from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

# Set to the correct Rasa endpoint
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    user_message = request.json.get("message")
    app.logger.info(f"Received message: {user_message}")

    if not user_message:
        app.logger.error("No message received in request")
        return jsonify({"response": "No message received"}), 400

    try:
        rasa_response = requests.post(
            RASA_API_URL,
            json={"sender": "user", "message": user_message}
        )
        rasa_response.raise_for_status()

        bot_responses = rasa_response.json()
        app.logger.info(f"Rasa response: {bot_responses}")

        if bot_responses:
            bot_response = bot_responses[0].get('text', "Sorry, I didn't understand that.")
        else:
            bot_response = "Sorry, I didn't understand that."

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error communicating with Rasa server: {str(e)}")
        bot_response = "Sorry, there was an error processing your request."

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
