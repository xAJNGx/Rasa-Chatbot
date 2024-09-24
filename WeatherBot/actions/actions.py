import os
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv

load_dotenv()

class ActionCheckCitySlot(Action):
    def name(self) -> Text:
        return "check_city_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot('city')

        if not city:
            dispatcher.utter_message(text="For which city would you like to know?")
            return [dict(action="utter_ask_city")]
        return []
    
    
class ActionGetWeatherBase(Action):
    def name(self) -> Text:
        return "action_get_weather_base"
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather_data(self, city):
        if not self.api_key:
            return None
        
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

class ActionGetTemperature(ActionGetWeatherBase):
    def name(self) -> Text:
        return "action_get_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot('city')
        weather_data = self.get_weather_data(city)
        
        if weather_data:
            temp_celsius = weather_data['main']['temp']
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            feels_like_celsius = weather_data['main']['feels_like']
            feels_like_fahrenheit = (feels_like_celsius * 9/5) + 32
            
            message = (f"The current temperature in {city} is {temp_celsius:.1f}°C ({temp_fahrenheit:.1f}°F). "
                       f"It feels like {feels_like_celsius:.1f}°C ({feels_like_fahrenheit:.1f}°F).")
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't get the temperature for {city}.")
        return []

class ActionGetHumidity(ActionGetWeatherBase):
    def name(self) -> Text:
        return "action_get_humidity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot('city')
        weather_data = self.get_weather_data(city)
        
        if weather_data:
            humidity = weather_data['main']['humidity']
            message = f"The current humidity in {city} is {humidity}%."
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't get the humidity for {city}.")
        return []

class ActionGetWindInfo(ActionGetWeatherBase):
    def name(self) -> Text:
        return "action_get_wind_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot('city')
        weather_data = self.get_weather_data(city)
        
        if weather_data:
            wind_speed = weather_data['wind']['speed']
            wind_direction = weather_data['wind'].get('deg', 'N/A')
            message = f"In {city}, the wind speed is {wind_speed} m/s, and the direction is {wind_direction}°."
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't get the wind information for {city}.")
        return []

class ActionGetWeatherDescription(ActionGetWeatherBase):
    def name(self) -> Text:
        return "action_get_weather_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot('city')
        weather_data = self.get_weather_data(city)
        
        if weather_data:
            description = weather_data['weather'][0]['description']
            message = f"The current weather condition in {city} is: {description}."
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't get the weather description for {city}.")
        return []

class ActionGetFullWeatherReport(ActionGetWeatherBase):
    def name(self) -> Text:
        return "action_get_full_weather_report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot('city')
        weather_data = self.get_weather_data(city)
        print(weather_data)
        if weather_data:
            temp_celsius = weather_data['main']['temp']
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            description = weather_data['weather'][0]['description']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            pressure = weather_data['main']['pressure']
            
            message = (
                f"Here's the full weather report for {city}:\n"
                f"• Temperature: {temp_celsius:.1f}°C ({temp_fahrenheit:.1f}°F)\n"
                f"• Condition: {description}\n"
                f"• Humidity: {humidity}%\n"
                f"• Wind Speed: {wind_speed} m/s\n"
                f"• Pressure: {pressure} hPa"
            )
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't get the weather report for {city}.")
        return []