from django.db import models


class ContinentChoices(models.TextChoices):
    AFRICA = "AF", "Africa"
    ASIA = "AS", "Asia"
    EUROPE = "EU", "Europe"
    NORTH_AMERICA = "NA", "North America"
    SOUTH_AMERICA = "SA", "South America"
    ANTARCTICA = "AN", "Antarctica"
    OCEANIA = "OC", "Oceania"
