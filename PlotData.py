from datetime import datetime
import matplotlib
from PIL import Image
from matplotlib import pyplot as plt
import seaborn as sns

matplotlib.use('Agg')


def plot_data(cities, client):

    temperature_data_timestamps = []
    temperatures = {}
    date_times = []
    first_time = True

    for city in cities:
        temperatures[city] = []
    with client:
        db = client.weather_data
        for city in cities:
            data = db['{}'.format(city)].find({})
            for record in data:
                temperatures[city].append(record["data"]["main"]["temp"])
                if first_time:
                    date_times.append(record["data"]["dt_txt"])
            first_time = False

    # Plot the lineplot
    for city in cities:
        plt.figure(figsize=(16, 16))
        plt.xticks(rotation=90, fontsize=10)
        plt.title("Temperature forecast for " + str(city), fontsize=20)
        plt.xlabel("Date and Time", fontsize=12)
        plt.ylabel("Temperature (C)", fontsize=12)
        sns.lineplot(x=date_times, y=temperatures[city], zorder=2)
        plt.savefig(
            "~/realtime-weather-alerts/PlotMap/" + city + ".png",
            bbox_inches='tight')
        plt.close()

        im = Image.open(
            "~/realtime-weather-alerts/PlotMap/" + city + ".png")
        im.show()

        ct = datetime.now()
        print("Plotted on", ct)
