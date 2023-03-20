import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from pip._vendor import requests
import datetime

# Looks up the city and returns a list of key-value pairs for weather conditions for a particular city.
def locate(city):
    api_key = "dc2f0197edbfd9235684496174dca96f" # Hide this key

    # Contact API
    try:

        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"

        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()

    except requests.RequestException:
        return None

    location = geo_response.json()

    return {
        "lat": location[0]["lat"],
        "lon": location[0]["lon"],
        "name": location[0]["name"]
    }

def lookup(lat, lon):
    api_key = "dc2f0197edbfd9235684496174dca96f"
    
    try:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()

    except requests.RequestException:
        return None
    
    weather = weather_response.json()

    celcius_temp = '{:.1f}°C'.format(float(weather["main"]["temp"]) - 273.15)
    celcius_like = '{:.1f}°C'.format(float(weather["main"]["feels_like"]) - 273.15)

    return {
        "temp": celcius_temp,
        "like": celcius_like,
        "main": weather["weather"][0]["main"],
        "desc": weather["weather"][0]["description"],
        "humidity": weather["main"]["humidity"],
        "wind": weather["wind"]["speed"],
        "dt": weather["dt"],
        "tz": weather["timezone"]
    }

def find(city):
    api_key = "dc2f0197edbfd9235684496174dca96f"

    # Contact API
    try:

        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=10&appid={api_key}"

        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()

    except requests.RequestException:
        return None

    location = geo_response.json()

    names = []
    states = []

    for i in range(0, len(location)):
        names.append(location[i]["name"])
        states.append(location[i]["state"])

    return {
        "name": names,
        "state": states
    }

def local_time(dt, tz):
    
    local_time = dt + tz

    time = datetime.datetime.fromtimestamp(local_time)

    print(f"dt_current = {time.hour}")

    if time.hour <= 5 or time.hour >= 19:
        return {
        "status": "night",
        "time": time
        }
    elif time.hour > 5 and time.hour < 7:
        return {
        "status": "evening",
        "time": time
        }
    elif time.hour > 17 and time.hour < 19:
        return {
        "status": "evening",
        "time": time
        }
    else:
        return {
        "status": "day",
        "time": time
        }