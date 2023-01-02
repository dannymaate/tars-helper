import requests
import json 

class Weather(object):
    API_KEY = 'be89fd5112588defdd48c3b013d16e04'
    URL = 'https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units=metric'

    def __init__(self):
        pass

    def fetch_weather(self, city_name):
        data = requests.get(Weather.URL.format(city_name, Weather.API_KEY))
        dataJSON = (data.json())
        temp = self._get_temp(dataJSON)
        desc = self._get_desc(dataJSON)

        return "Today in {0} it's {1} degrees with {2}".format(city_name, temp, desc)

    def _get_temp(self, weatherData):
        return weatherData['main']['temp']

    def _get_desc(self, weatherData):
        return weatherData['weather'][0]['description']