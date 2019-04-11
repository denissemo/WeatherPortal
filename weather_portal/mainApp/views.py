from django.shortcuts import render
from django.views import View
from .weather_models import Weather
from .models import City, Day
from django.http import HttpResponse
import calendar
import datetime


def index(request):
    return render(request, 'mainPage/index.html')


def cities(request):
    template = 'city/cities_template.html'
    city = City.objects.in_bulk()
    day = Day.objects.in_bulk()
    days = list(set([day[id_].date for id_ in day]))
    days.sort()
    context = {
        'cities': [city[id_].name for id_ in city],
        'days': days
    }
    return render(request, template, context)


class SubmitCity(View):
    template = 'city/cities_template.html'

    def get(self, *args, **kwargs):
        city_name = self.request.GET['city_name']
        date_from = self.request.GET['date_from']
        date_to = self.request.GET['date_to']
        if date_from == date_to:
            return HttpResponse(Day.objects.filter(city__name=city_name, date=date_from).values())
        else:
            """Weather response from DB like: 
            {'id': 21, 'date': '11 April', 'min_temp': '7.92', 'max_temp': '12.2', 
            'wind': '5.97', 'description': 'light rain', 'clouds': '92', 'icon': '10d', 'city_id': 4}"""
            response = []

            date_from_day = date_from.split()[0]  # day value [1...31]
            date_from_month = list(calendar.month_name).index(date_from.split()[1])  # month number [1...12]
            date_to_day = date_to.split()[0]
            date_to_month = list(calendar.month_name).index(date_to.split()[1])
            # datetime object from str
            date_from_datetime = datetime.datetime.strptime(
                "{} {} {} {}:{}".format(date_from_day, date_from_month, datetime.datetime.today().year, 0, 0),
                "%d %m %Y %H:%M")
            date_to_datetime = datetime.datetime.strptime(
                "{} {} {} {}:{}".format(date_to_day, date_to_month, datetime.datetime.today().year, 0, 0),
                "%d %m %Y %H:%M")
            # calculate dates range
            difference_between_dates = (date_to_datetime - date_from_datetime).days
            for day in range(difference_between_dates + 1):
                # add to date_from days
                day_str = (date_from_datetime + datetime.timedelta(days=day)).day
                month_str = calendar.month_name[(date_from_datetime + datetime.timedelta(days=day)).month]
                date = "{} {}".format(day_str, month_str)  # date like '11 April'
                # get data from DB
                response.append(Day.objects.filter(city__name=city_name, date=date).values()[0])
            return HttpResponse("\n".join([str(i) for i in response]))  # join responses by '\n'


class AddCity(View):
    template = 'mainPage/index.html'

    def get(self, *args, **kwargs):
        weather = Weather(self.request.GET['city'])
        if weather.isFound:
            city = City.objects.update_or_create(name=weather.city)
            for i in range(weather.days_count):
                city[0].day_set.update_or_create(
                    date=weather.dates[i],
                    min_temp=weather.min_temps[i],
                    max_temp=weather.max_temps[i],
                    wind=weather.winds[i],
                    description=weather.descriptions[i],
                    clouds=weather.clouds[i],
                    icon=weather.icons[i]
                )
        context = {
            'visible': True,
            'weather': weather
        }
        return render(self.request, self.template, context)
