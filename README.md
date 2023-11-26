# Recording real time weather changes using MongoDB and OpenWeather API.

# Aim/Purpose: 
To generate warnings using database triggers during extreme weather conditions.
# Approach: 
1. We will be using OpenWeather’s openweathermapAPI to fetch real time and historical weather data. This REST API allows fetching weather information for locations mentioned in the API request.
2. The API response (json/XML/HTML) will be stored in MongoDB as a collection or document. The type of response from the endpoint led to this choice of using a NoSQL database.
3. The collection/document will keep updating as new responses from the openweathermapAPI are stored in the database with every API call. The frequency of these calls can be controlled and defined in the configuration file of the endpoint.
4. The endpoint offers the following combinations of weather data in one response:
a. Minute forecast for 1 hour
b. Hourly forecast for 48 hours
c. Daily forecast for 8 days
d. Historical data for 40+ years back by timestamp
e. National weather alerts
Reference: https://openweathermap.org/api
We will use any one of these combinations to be stored in the database.
5. Documents in MongoDB consist of key-value pairs and are most suitable to store json
responses from the endpoint. A trigger will be configured on one of the keys to alert
the user in case of severe weather conditions like extreme hot or cold temperature.

# The deliverable:
1. An API configuration file for the API requests (containing the request body).
2. Main driver file that has the MongoDB localhost connection, makes the API calls and
stores the data in the database, all written in Python

# Post midterm update:
The final application "WeatherJag" is a multithreaded application that uses the 5 day/3 hour API endpoint to fetch weather data which is then stored in MongoDB. 
Alerts are generated in python which uses queries the data stored in the database to generate alerts. 
WeatherJag is also capable of generating a map of the city showing current weather and also generates a lineplot showing temperature with respect to dates.

# How to run the application:
1. You must only run main.py. The main file has function and thread calls to other files. No need to run the applciation.py file seperately. This causes circular dependencies.
2. Change the location/path where you want to save the maps and lineplots on your location machine. The default path is my local machine's path.
3. For the evaluation of this project, we have not changed the API key and is the original key of our OpenWeatherMap account.
4. All the modules supporting python modules need to be installed if the system requires it. (Just install the modules as the interpreter asks in case any errors are seen after the main file is run.)



