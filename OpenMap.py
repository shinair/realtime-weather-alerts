import webbrowser
from datetime import datetime

import folium
import matplotlib

matplotlib.use('Agg')


def latest_weather_map(locations, cities, db):
    print("Inside OpenMap function")
    for city in cities:
        # Find the last record for each city as latest map record
        cursor = list(db['{}'.format(city)].find().sort([('_id', -1)]).limit(1))

        location = locations[city]
        print(locations)
        maps = folium.Map(location=[location.latitude, location.longitude], tiles='cartodbdark_matter', zoom_start=8,
                          attr="<a href=https://endless-sky.github.io/>Endless Sky</a>")
        weather = str(cursor[0]["data"]['weather'][0]['description'])
        last_timestamp_date = str(cursor[0]["data"]['dt_txt'])
        temperature = str(round(float((cursor[0]["data"]["main"]["temp"] - 273.15) * (9 / 5) + 32), 2))
        icon = cursor[0]["data"]['weather'][0]['icon']

        icon_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"

        icon = folium.features.CustomIcon(icon_url,
                                          icon_size=(100, 100),
                                          icon_anchor=(22, 94),
                                          popup_anchor=(-3, -76))

        marker = folium.Marker(location=[location.latitude - 0.03, location.longitude - 0.12], icon=icon,
                               popup="Temperature is " + temperature + "F",
                               html='<div style="font-size:12pt">%s F</div>' % temperature)

        maps.add_child(marker)
        maps.add_child(folium.Popup(temperature))
        legend_html = '''
                <div style="position: fixed; 
                            bottom: 100px; left: 50px; width: 120px; height: 90px; 
                            border:2px solid grey; z-index:9999; font-size:12px;
                            "
                            >
                            <b>
                            <font color="red">
                            &nbsp;                             
                            Legend
                            </font>
                            </b>
                            <br>
                                 <img 
                                     src="%s" alt="weather" height="40" width="40"
                                 />
                                  <b> <font color="green">
                                  &nbsp; %s &nbsp;
                                  </font>
                                  </b?
                                  <i 
                                      class="icon" style="color:red">
                                  </i>
                            <br>
                </div>
                ''' % (icon_url, weather)
        maps.get_root().html.add_child(folium.Element(legend_html))
        maps.save(
            "~/realtime-weather-alerts/OpenMap/" + city + "_" + last_timestamp_date.replace(
                ":", "_") + "_latest_weather.html")

        webbrowser.open("file://~/realtime-weather-alerts/OpenMap/" + city + "_" + last_timestamp_date.replace(
                ":", "_") + "_latest_weather.html")
        ct = datetime.now()
        print("Latest Map downloaded on", ct)
