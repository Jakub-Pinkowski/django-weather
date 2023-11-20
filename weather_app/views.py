import datetime
import requests

from django.shortcuts import render


# Create your views here.
def index(request):
    API_KEY = open("AIP_KEY", "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"

    if request.method == "POST":
        pass
    else:
        return render()