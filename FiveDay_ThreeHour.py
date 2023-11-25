# file for 5day/3hour forecast thread

import pymongo
import json
import matplotlib
import httplib2

matplotlib.use('Agg')


def weather_forecast(cities, API_endpoint, API_Key, db):
    alerts = {"rain": [], "snow": [], "freezing_temperature": []}

    for city in cities:

        url = API_endpoint + "/data/2.5/forecast?q=" + city + "&appid=" + API_Key + "&units=metric"
        http_initializer = httplib2.Http()
        response, content = http_initializer.request(url, 'GET')
        utf_decoded_content = content.decode('utf-8')
        json_object = json.loads(utf_decoded_content)

        print(json_object)

        for element in json_object["list"]:
            try:
                datetime = element['dt']
                del element['dt']
                db['{}'.format(city)].insert_one({'_id': datetime, "data": element})
            except pymongo.errors.DuplicateKeyError:
                continue

        print("fetched data")
