import os
import requests
import json
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from daydashapi.models import DashUser


class WeatherView(ViewSet):
    """DayDash API weather API interface"""

    def retrieve(self, request, pk):
        """Handle GET requests to get friend
        Returns:
            Response -- JSON serialized friend object
        """
        try:
            load_dotenv()
            KEY = os.getenv('WEATHER_API_KEY')
            user = DashUser.objects.get(pk=pk)
            url = f"http://api.weatherapi.com/v1/forecast.json?key={KEY}&q={user.zipcode}&days=2&aqi=no&alerts=no"
            response = requests.get(url)
            data = json.loads(response.content)
            location = {
                'name': data['location']['name'],
                'region': data['location']['region']
            }
            current = {
                'temp': data['current']['temp_f'],
                'condition': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
                'wind': data['current']['wind_mph'],
                'humidity': f"{data['current']['humidity']}%",
            }
            today = {
                'high': data['forecast']['forecastday'][0]['day']['maxtemp_f'],
                'low': data['forecast']['forecastday'][0]['day']['mintemp_f'],
                'rain': data['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
                'condition': data['forecast']['forecastday'][0]['day']['condition']['text'],
                'icon': data['forecast']['forecastday'][0]['day']['condition']['icon'],
                'sunrise': data['forecast']['forecastday'][0]['astro']['sunrise'],
                'sunset': data['forecast']['forecastday'][0]['astro']['sunset'],
                'moon': data['forecast']['forecastday'][0]['astro']['moon_phase'],
            }
            tomorrow = {
                'high': data['forecast']['forecastday'][1]['day']['maxtemp_f'],
                'low': data['forecast']['forecastday'][1]['day']['mintemp_f'],
                'rain': data['forecast']['forecastday'][1]['day']['daily_chance_of_rain'],
                'condition': data['forecast']['forecastday'][1]['day']['condition']['text'],
                'icon': data['forecast']['forecastday'][1]['day']['condition']['icon'],
                'sunrise': data['forecast']['forecastday'][1]['astro']['sunrise'],
                'sunset': data['forecast']['forecastday'][1]['astro']['sunset'],
                'moon': data['forecast']['forecastday'][1]['astro']['moon_phase'],
            }
            response_data = {
                'location': location,
                'current': current,
                'today': today,
                'tomorrow': tomorrow
            }

        except ObjectDoesNotExist:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

        return Response(response_data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get friends

        Returns:
            Response -- JSON serialized list of friends
        """

        load_dotenv()
        KEY = os.getenv('WEATHER_API_KEY')
        user = DashUser.objects.get(user=request.auth.user)
        url = f"http://api.weatherapi.com/v1/forecast.json?key={KEY}&q={user.zipcode}&days=2&aqi=no&alerts=no"
        response = requests.get(url)
        data = json.loads(response.content)
        location = {
            'name': data['location']['name'],
            'region': data['location']['region']
        }
        current = {
            'temp': data['current']['temp_f'],
            'condition': data['current']['condition']['text'],
            'icon': data['current']['condition']['icon'],
            'wind': data['current']['wind_mph'],
            'humidity': f"{data['current']['humidity']}%",
        }
        today = {
            'high': data['forecast']['forecastday'][0]['day']['maxtemp_f'],
            'low': data['forecast']['forecastday'][0]['day']['mintemp_f'],
            'rain': data['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
            'condition': data['forecast']['forecastday'][0]['day']['condition']['text'],
            'icon': data['forecast']['forecastday'][0]['day']['condition']['icon'],
            'sunrise': data['forecast']['forecastday'][0]['astro']['sunrise'],
            'sunset': data['forecast']['forecastday'][0]['astro']['sunset'],
            'moon': data['forecast']['forecastday'][0]['astro']['moon_phase'],
        }
        tomorrow = {
            'high': data['forecast']['forecastday'][1]['day']['maxtemp_f'],
            'low': data['forecast']['forecastday'][1]['day']['mintemp_f'],
            'rain': data['forecast']['forecastday'][1]['day']['daily_chance_of_rain'],
            'condition': data['forecast']['forecastday'][1]['day']['condition']['text'],
            'icon': data['forecast']['forecastday'][1]['day']['condition']['icon'],
            'sunrise': data['forecast']['forecastday'][1]['astro']['sunrise'],
            'sunset': data['forecast']['forecastday'][1]['astro']['sunset'],
            'moon': data['forecast']['forecastday'][1]['astro']['moon_phase'],
        }
        response_data = {
            'location': location,
            'current': current,
            'today': today,
            'tomorrow': tomorrow
        }
        # response_data = {
        #     "location": {
        #         "name": "Clarksville",
        #         "region": "Tennessee"
        #     },
        #     "current": {
        #         "temp": 39.0,
        #         "condition": "Overcast",
        #         "wind": 17.4,
        #         "humidity": "52%"
        #     },
        #     "today": {
        #         "high": 49.5,
        #         "low": 30.6,
        #         "rain": 0.0,
        #         "condition": "Partly cloudy",
        #         "sunrise": "07:04 AM",
        #         "sunset": "06:55 PM",
        #         "moon": "Waning Gibbous"
        #     },
        #     "tomorrow": {
        #         "high": 45.9,
        #         "low": 27.5,
        #         "rain": 0.0,
        #         "condition": "Partly cloudy",
        #         "sunrise": "07:02 AM",
        #         "sunset": "06:56 PM",
        #         "moon": "Waning Gibbous"
        #     }
        # }
        return Response(response_data, status=status.HTTP_200_OK)
