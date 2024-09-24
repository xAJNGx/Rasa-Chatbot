# Weather Bot

This is a weather bot built using the Rasa conversational AI framework. The bot is designed to provide users with information about the weather in different cities, including temperature, humidity, wind, and weather description.
The bot utilizes the following Rasa pipeline components:

- SpacyNLP: This component loads the en_core_web_md SpaCy language model, which provides advanced natural language processing capabilities.
- SpacyTokenizer: This component uses the SpaCy tokenizer to split the user's input into meaningful tokens.
- SpacyFeaturizer: This component uses the SpaCy library to generate word vectors, which are used as features for the machine learning models.
- SpacyEntityExtractor: This component extracts entities, such as cities and countries (GPE - Geopolitical Entities), from the user's input.
- CountVectorsFeaturizer: This component generates bag-of-words features from the user's input, which are used for text classification.
- DIETClassifier: This component is responsible for both intent classification and entity recognition. It is trained for 100 epochs to achieve high accuracy.
- FallbackClassifier: This component handles cases where the bot is not confident about the predicted intent or entity. It uses a threshold of 0.3 and an ambiguity threshold of 0.1 to determine when to trigger the fallback response.

The bot uses the OpenWeatherMap API to fetch the weather data for the specified city. It supports a variety of intents, including greetings, weather queries, and user sentiment expressions.
Users can interact with the bot through a web interface, and the bot's responses are generated dynamically based on the user's input and the available weather data.

## Features

The bot supports the following intents:

- `greet`: The user greets the bot.
- `goodbye`: The user says goodbye to the bot.
- `ask_weather`: The user asks about the weather.
- `inform_city`: The user specifies the city they want to know the weather for.
- `ask_temperature`: The user asks for the temperature.
- `ask_humidity`: The user asks for the humidity.
- `ask_wind`: The user asks for the wind information.
- `ask_weather_description`: The user asks for the weather description.
- `ask_full_weather_report`: The user asks for a full weather report.
- `user_feels_sad`: The user expresses feeling sad.
- `affirm`: The user affirms something.
- `bot_challenge`: The user challenges the bot.

The bot uses the OpenWeatherMap API to fetch the weather data for the specified city.

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/weather-bot.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Obtain an API key from OpenWeatherMap and set it as an environment variable:

```
OPENWEATHERMAP_API_KEY=your-api-key
```

4. Run the Rasa server:

```
rasa run --enable-api --cors "*"
```

5. Run the Flask server:

```
python index.py
```

The bot should now be running and ready to answer your weather-related questions.

## Usage

You can interact with the bot through the web interface at `http://localhost:5000/`. You can also use the Rasa API to interact with the bot programmatically.

Here are some example interactions:

```
User: Hello
Bot: Hello! I'm a weather bot. How can I help you today?

User: What's the weather like in New York?
Bot: The current temperature in New York is 20.0°C (68.0°F). It feels like 18.5°C (65.3°F).

User: What's the humidity?
Bot: The current humidity in New York is 60%.

User: What about the wind?
Bot: In New York, the wind speed is 5 m/s, and the direction is 270°.

User: Can you give me the full weather report for London?
Bot: Here's the full weather report for London:
• Temperature: 15.0°C (59.0°F)
• Condition: broken clouds
• Humidity: 70%
• Wind Speed: 7 m/s
• Pressure: 1020 hPa

User: That's great, thanks!
Bot: Did that help you?

User: Yes, it did. Goodbye!
Bot: Goodbye! Have a great day!
```

## Screenshots

Here are some screenshots of the weather bot in action:

![alt text](screenshots/image.png)

*Weather Bot Homepage*

![alt text](screenshots/image-1.png)

*Weather Information*

![alt text](screenshots/image-3.png)

*Full Weather Report*

## Contact Me

If you have any questions or feedback, feel free to reach out to me:

- Email: ajngworks@gmail.com

I'd be happy to assist you or discuss any improvements or new features you'd like to see in the weather bot.