from tkinter import *
import httplib2
import pymongo
import requests
import json
from datetime import datetime
import main

# initializing database client
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.weather_data

# Initializing application Window
root = Tk()
root.geometry("500x680")  # size of the window by default
root['background'] = "#f5f5f5"
root.resizable(height=None, width=None)  # to make the window size fixed
root.title("IUPUI - WeatherJag")
IU = PhotoImage(file = 'IU.png')
root.iconphoto(False, IU)

city_value = StringVar()
cities = []


def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()


city_value = StringVar()


# function to fetch weather details and display alerts
def weather_forecast():
    city_name = city_value.get()
    cities.clear()
    cities.append(city_name)
    tfield.delete("1.0", "end")

    for city in cities:

        print(city)

        url = main.API_endpoint + "/data/2.5/forecast?q=" + city + "&appid=" + main.API_Key + "&units=metric"
        http_initializer = httplib2.Http()
        response, content = http_initializer.request(url, 'GET')
        utf_decoded_content = content.decode('utf-8')
        json_object = json.loads(utf_decoded_content)

        for element in json_object["list"]:
            try:
                datetime = element['dt']
                del element['dt']
                db['{}'.format(city)].insert_one({'_id': datetime, "data": element})
            except pymongo.errors.DuplicateKeyError:
                continue

        print("fetched data")

        for a in db['{}'.format(city)].find({}):
            if a["data"]["weather"][0]["main"] == "Snow":
                alert = "\nSnow in " + city + " on " + str(a["data"]["dt_txt"]).split(" ")[0] + " at " + \
                        str(a["data"]["dt_txt"]).split(" ")[1]
                # tfield.insert(INSERT, alert)
            elif a["data"]["weather"][0]["main"] == "Rain":
                alert = "\nRain in " + city + " on " + str(a["data"]["dt_txt"]).split(" ")[0] + " at " + \
                        str(a["data"]["dt_txt"]).split(" ")[1]
                # tfield.insert(INSERT, alert)
            elif a["data"]["weather"][0]["main"] == "Clouds":
                alert = "\nClouds in " + city + " on " + str(a["data"]["dt_txt"]).split(" ")[0] + " at " + \
                        str(a["data"]["dt_txt"]).split(" ")[1]
                # tfield.insert(INSERT, alert)
            elif a["data"]["weather"][0]["main"] == "Clear":
                alert = "\nClear sky in " + city + " on " + str(a["data"]["dt_txt"]).split(" ")[0] + " at " + \
                        str(a["data"]["dt_txt"]).split(" ")[1]
                # tfield.insert(INSERT, alert)
            elif a["data"]["weather"][0]["main"] == "Smoke":
                alert = "\nSmoke in " + city + " on " + str(a["data"]["dt_txt"]).split(" ")[0] + " at " + \
                        str(a["data"]["dt_txt"]).split(" ")[1]
                # tfield.insert(INSERT, alert)
            elif a["data"]["weather"][0]["main"] == "Fog":
                alert = "\nFog in " + city + " on " + str(a["data"]["dt_txt"]).split(" ")[0] + " at " + \
                        str(a["data"]["dt_txt"]).split(" ")[1]
                # tfield.insert(INSERT, alert)
            elif a["data"]["weather"][0]["main"] == "Tornado":
                alert = "\nTornado in " + city + " on " + str(a["data"]["dt_txt"]).split(" ")[0] + " at " + \
                        str(a["data"]["dt_txt"]).split(" ")[1]
                # tfield.insert(INSERT, alert)
            tfield.insert(INSERT, alert)


# function to display weather information for a given city
def showWeather():
    # city name that user inputs
    city_name = city_value.get()

    weather_url = main.API_endpoint + "/data/2.5/weather?q=" + city_name + "&appid=" + main.API_Key

    response = requests.get(weather_url)

    # changing response from json to python readable
    weather_info = response.json()
    print(weather_info)
    tfield.delete("1.0", "end")  # to clear the text field for every new output

    if weather_info['cod'] == 200:
        kelvin = 273
        # converting values from kelvin to celcius
        temp = int(weather_info['main']['temp'] - kelvin)
        feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed'] * 3.6
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']

        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)

        weather = f"\nWeather of: {city_name}\nTemperature (Celsius): {temp}°\nFeels like in (Celsius): {feels_like_temp}°\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
    else:
        weather = f"\n\tWeather for '{city_name}' not found!\n\tKindly Enter valid City Name !!"

    tfield.insert(INSERT, weather)  # to insert or send value in our Text Field to display output


# function to open the city map of a given city
def openMap():
    city_name = city_value.get()
    cities.clear()
    cities.append(city_name)
    print("Inside OpenMap-Application")
    main.runOpenMap(cities)


# function to open a temperature scatter plot for a given city
def plotGraph():
    city_name = city_value.get()
    cities.clear()
    cities.append(city_name)
    print("Inside OpenMap-Application")
    main.runPlotMap(cities)


# application UI

Label(root, text='WeatherJag', font='FrankRuehl 22 bold').pack(pady=10)
Label(root, text='Enter City Name',  foreground="#5b0000",  font='FrankRuehl 10 bold').pack(pady=10)

Entry(root, textvariable=city_value, width=24, font='FrankRuehl 14 bold').pack()

Button(root, command=showWeather, text="Check Weather", font="FrankRuehl 10", bg='#a31919', fg='#ffffff',
       activebackground="#cc7f7f", padx=5, pady=5).pack(pady=20)

Button(root, command=weather_forecast, text="Get Alerts", font="FrankRuehl 10", bg='#a31919', fg='#ffffff',
       activebackground="#cc7f7f", padx=5, pady=5).pack(pady=20)

Button(root, command=openMap, text="Open Map", font="FrankRuehl 10", bg='#a31919', fg='#ffffff',
       activebackground="#cc7f7f", padx=5, pady=5).pack(pady=20)

Button(root, command=plotGraph, text="Statistics", font="FrankRuehl 10", bg='#a31919', fg='#ffffff',
       activebackground="#cc7f7f", padx=5, pady=5).pack(pady=20)
# to show output

Label(root, text="Weather details:", foreground="#5b0000",  font='FrankRuehl 10 bold').pack(pady=10)

tfield = Text(root, width=46, height=10)
tfield.pack()

root.mainloop()
