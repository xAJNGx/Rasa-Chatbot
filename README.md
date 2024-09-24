# Rasa-Chatbot

Start the Rasa server:

        rasa run --enable-api --cors "*"

In another terminal, start the Rasa action server:

        rasa run actions

In a third terminal, run the Flask web interface:

        python index.py