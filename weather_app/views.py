import datetime
from datetime import datetime
import requests

from django.shortcuts import render


# Create your views here.
def index(request):
    API_KEY = open("API_KEY", "r").read()
    current_weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    )
    forecast_url = (
        "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"
    )

    if request.method == "POST":
        city1 = request.POST["city1"]
        city2 = request.POST.get("city2", None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(
            city1, API_KEY, current_weather_url, forecast_url
        )

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(
                city2, API_KEY, current_weather_url, forecast_url
            )
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2,
        }

        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response["coord"]["lat"], response["coord"]["lon"]
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": round(response["main"]["temp"] - 273.15, 2),
        "description": response["weather"][0]["description"],
        "icon": response["weather"][0]["icon"],
    }

    daily_forecasts = []
    for day in forecast_response["list"]:
        if day["dt_txt"].split()[1] == "12:00:00":
            date_str = day["dt_txt"].split()[0]
            datetime_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            daily_forecasts.append(
                {
                    "date": datetime_obj.strftime("%m-%d"),  # Format to display month and day
                    "temperature": round(day["main"]["temp"] - 273.15, 0),
                    "description": day["weather"][0]["description"],
                    "icon": day["weather"][0]["icon"],
                }
            )

    return weather_data, daily_forecasts
