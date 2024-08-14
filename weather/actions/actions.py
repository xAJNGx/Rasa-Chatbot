from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
from dotenv import load_dotenv
import requests

load_dotenv()

class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot('city')
        
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        
        if not api_key:
            dispatcher.utter_message(text="I'm sorry, I can't access the weather information rightnow")
            return []
        
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q':city,
            'appid':api_key,
            'units':'metric'
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            weather_data = response.json()
            
            temp_celsius = weather_data['main']['temp']
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            description = weather_data['weather'][0]['description']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            pressure = weather_data['main']['pressure']
            
            weather_info = (
                f"Here's the current weather in {city}:\n"
                f"• Temperature: {temp_celsius:.1f}°C ({temp_fahrenheit:.1f}°F)\n"
                f"• Condition: {description}\n"
                f"• Humidity: {humidity}%\n"
                f"• Wind Speed: {wind_speed} m/s\n"
                f"• Pressure: {pressure} hPa"
            )

            dispatcher.utter_message(text=weather_info)
        except requests.exceptions.RequestException as e:
            error_message = f"Sorry, I couldn't get the weather information for {city}. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
        return []

