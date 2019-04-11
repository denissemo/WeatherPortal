import requests
from datetime import datetime
import calendar
from collections import Counter


class Weather:
    api_key = 'f84baa428cbb55cab32452c999b76fba'
    api_url = 'http://api.openweathermap.org/data/2.5/forecast?&q={}&units=metric&APPID={}'

    def __init__(self, city):
        self.city = city
        r = requests.get(url=self.api_url.format(city, self.api_key))
        self.data = r.json()
        self.isFound = False
        if self.data['cod'] == '200':
            self.isFound = True
            # each day information
            self.dates = []
            self.min_temps = []
            self.max_temps = []
            self.winds = []
            self.descriptions = []
            self.clouds = []
            self.icons = []

            for i in range(0, self.data['cnt'], 8):
                date = datetime.fromtimestamp(self.data['list'][i]['dt'])
                self.dates.append('{} {}'.format(date.day, calendar.month_name[date.month]))
                tmp_temp = []
                tmp_wind = []
                tmp_desc = []
                tmp_icon = []
                tmp_cloud = []
                for j in range(0, self.data['cnt']):
                    if str(date.date()) == str(datetime.fromtimestamp(self.data['list'][j]['dt']).date()):
                        tmp_temp.append(self.data['list'][j]['main']['temp'])
                        tmp_wind.append(self.data['list'][j]['wind']['speed'])
                        tmp_desc.append(self.data['list'][j]['weather'][0]['description'])
                        tmp_cloud.append(self.data['list'][j]['clouds']['all'])
                        tmp_icon.append(self.data['list'][j]['weather'][0]['icon'])
                # minimum and maximum temperature per day
                self.min_temps.append(min(tmp_temp))
                self.max_temps.append(max(tmp_temp))
                # the value that is most often repeated
                self.winds.append(self.often_value(tmp_wind))
                self.descriptions.append(self.often_value(tmp_desc))
                self.clouds.append(self.often_value(tmp_cloud))
                self.icons.append(self.often_value(tmp_icon))

    @staticmethod
    def often_value(arr):
        return max(list(Counter(arr).items()), key=lambda x: x[1])[0]

    @property
    def days_count(self):
        return len(self.dates)

    def __str__(self):
        return self.city
