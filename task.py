import requests
import datetime


weather_api_url = 'https://api.openweathermap.org/data/2.5/weather'


def call_weather_api(token: str, city: str, units: str = 'standard'):
    response = requests.request(method='GET', url=weather_api_url, params={
                                'appid': token, 'q': city, 'units': units})
    return response.json()


def create_data(content):
    return {
        'temp': content['main']['temp'],
        'main': content['weather'][0]['main'],
        'feels_like': content['main']['feels_like'],
        'timestamp': datetime.datetime.fromtimestamp(content['dt'], datetime.timezone.utc),
        'city': content['name']
    }
