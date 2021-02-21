from django.db import models


class UtilityMeterType(models.Choices):
    water_cold = 'water cold'
    water_hot = 'water hot'
    electricity_day = 'electricity day'
    electricity_night = 'electricity night'
