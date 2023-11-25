import configuration as config
import pymongo
import threading
import time
import Application
import matplotlib

matplotlib.use('TkAgg')

from OpenMap import latest_weather_map
from PlotData import plot_data

matplotlib.use('Agg')

import httplib2

from geopy.geocoders import Nominatim

from FiveDay_ThreeHour import weather_forecast
from WeatherMaps import weather_maps

# variables for creating setup

geolocator = Nominatim(user_agent="Weather Forecast App")

# OpenWeatherMap API key goes here
API_Key = " "

API_endpoint = "http://api.openweathermap.org/"

open_weather_map_API_endpoint = "http://tile.openweathermap.org/"

# initializing MongoDB client
client = pymongo.MongoClient('mongodb://localhost:27017/')

http_initializer = httplib2.Http()

cities = config.locations

# default location to fetch data and alerts in case individual threads are run instead of the application
city = config.city

# refresh frequency for threads
refresh_frequency = config.refresh_frequency

# Creating Mongodb database
db = client.weather_data


def runOpenMap(cities):
    locations = {}
    for city in cities:
        locations[city] = geolocator.geocode(city)

        try:
            t1 = threading.Thread(target=lambda: latest_weather_map(locations, cities, db), name='t1',
                                  daemon=True)
            t1.start()
            t1.join()
            print("Started thread")
            break
            t1.stop()

        except Exception as e:
            print(e)


def runPlotMap(cities):
    locations = {}
    for city in cities:
        locations[city] = geolocator.geocode(city)

        try:
            t2 = threading.Thread(target=lambda: plot_data(cities, client), name='t2',
                                  daemon=True)
            t2.start()
            t2.join()
            print("Started thread")
            break
            t2.stop()

        except Exception as e:
            print(e)


if __name__ == "__main__":
    locations = {}

    # Get latitude and longitude of cities for which we want to forecast weather
    for city in cities:
        locations[city] = geolocator.geocode(city)

    while 1:
        try:
            t1 = threading.Thread(target=lambda: weather_forecast(cities, API_endpoint,
                                                                  API_Key,
                                                                  db), name='t1', daemon=True)

            t2 = threading.Thread(target=lambda: weather_maps(locations, cities, db), name='t2', daemon=True)

            t3 = threading.Thread(target=lambda: latest_weather_map(locations, cities, db), name='t3',
                                  daemon=True)

            t4 = threading.Thread(target=lambda: plot_data(cities, client), name='t4',
                                  daemon=True)

            t5 = threading.Thread(target=lambda: Application.showWeather(), name='t5',
                                  daemon=True)

            t1.start()
            t1.join()
            time.sleep(refresh_frequency)

        except Exception as e:
            print(e)
