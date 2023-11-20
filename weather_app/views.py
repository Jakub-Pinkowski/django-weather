import datetime
import requests

from django.shortcuts import render


# Create your views here.
def index(request):
    API_KEY = open("AIP_KEY", "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.get('city2', None)
    else:
        return render(request, "weather_app/index.html")
    

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "tempature": round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
    }