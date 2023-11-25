import folium
import matplotlib

matplotlib.use('Agg')


def weather_maps(locations, cities, db):

    # For each city, we call its location in Google Maps
    for city in cities:
        for a in db['{}'.format(city)].find({}):
            location = locations[city]
            maps = folium.Map(location=[location.latitude, location.longitude], tiles='cartodbdark_matter',
                              zoom_start=8,
                              attr="<a href=https://endless-sky.github.io/>Endless Sky</a>")
            weather = str(a["data"]['weather'][0]['description'])
            last_timestamp_date = str(a["data"]['dt_txt'])
            temperature = str(round(float((a["data"]["main"]["temp"] - 273.15) * (9 / 5) + 32), 2))
            # Get the icon that represents weather on that date for that city

            icon = a["data"]['weather'][0]['icon']

            icon_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"

            # Downloading icon for the weather
            icon = folium.features.CustomIcon(icon_url,
                                              icon_size=(100, 100),
                                              icon_anchor=(22, 94),
                                              popup_anchor=(-3, -76))

            # Subtracting values just to adjust the marker on Map
            marker = folium.Marker(location=[location.latitude - 0.03, location.longitude - 0.12], icon=icon,
                                   popup="Temperature is " + temperature + "F",
                                   html='<div style="font-size:12pt">%s F</div>' % temperature)
            popup = folium.Popup(temperature)

            #           folium.TileLayer('cartodbpositron').add_to(maps)
            maps.add_child(marker)
            maps.add_child(popup)
            # Adding a legend to the map
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

            # Create and save the map
            maps.get_root().html.add_child(folium.Element(legend_html))
            maps.save("D:/Coursework/FA22 DATABASE SYSTEMS 29229/Project/realtime-weather-changes/Maps/" + city + "_" + last_timestamp_date.replace(":",
                                                                                                                 "_") + ".html")
