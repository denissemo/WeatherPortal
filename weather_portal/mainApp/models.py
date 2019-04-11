from django.db import models


class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Day(models.Model):
    date = models.CharField(max_length=30)
    min_temp = models.CharField(max_length=5)
    max_temp = models.CharField(max_length=5)
    wind = models.CharField(max_length=5)
    description = models.CharField(max_length=100)
    clouds = models.CharField(max_length=5)
    icon = models.CharField(max_length=5)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
