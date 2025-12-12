"""
Utility functions for populating geobank data.

This module provides the main entry point for populating the geobank database
with geographic data from external sources (geonames.org, restcountries.com).
"""

import logging

from django.conf import settings
from django.db.models import F, FloatField
from django.db.models.functions import Power, Sqrt

from .models import City
from .populators import (
    populate_cities,
    populate_countries,
    populate_currencies,
    populate_flags,
    populate_languages,
    populate_regions,
    translate_data,
)

logger = logging.getLogger(__name__)


def populate_geobank_data(population_gte: int = 15000):
    """
    Populate all geobank data from external sources.

    This function orchestrates the entire data population process:
    1. Populates reference data (languages, currencies)
    2. Populates geographic data (countries, regions, cities)
    3. Populates supplementary data (flags)
    4. Applies translations based on configured languages

    Args:
        population_gte: Minimum population threshold for cities.
                       Common values: 500, 1000, 5000, 15000
    """
    # Get configured languages for translation
    languages = [lang[0] for lang in getattr(settings, "LANGUAGES", [])]
    logger.info(f"Detected languages: {languages}")

    # Populate reference data first (languages, currencies)
    # These are needed before populating countries
    populate_languages()
    populate_currencies()

    # Populate geographic data
    populate_countries()
    populate_regions()
    populate_cities(population_gte)

    # Populate supplementary data
    populate_flags()

    # Apply translations
    translate_data(languages)

    logger.info("Geobank data population complete.")


class LocationTypeChoices:
    CITY = "city"
    REGION = "region"
    COUNTRY = "country"


def get_location_by_coordinates(
    lat, lng, location_type: LocationTypeChoices = LocationTypeChoices.CITY
):
    """Find country by nearest city (approximate)."""
    if location_type not in {
        LocationTypeChoices.CITY,
        LocationTypeChoices.REGION,
        LocationTypeChoices.COUNTRY,
    }:
        raise ValueError("The location_type argument must be an instance of LocationTypeChoices")

    nearest_city = (
        City.objects.annotate(
            distance=Sqrt(
                Power(F("latitude") - lat, 2, output_field=FloatField())
                + Power(F("longitude") - lng, 2, output_field=FloatField()),
                output_field=FloatField(),
            )
        )
        .order_by("distance")
        .select_related("region__country")
        .first()
    )

    if nearest_city:
        mapping = {
            LocationTypeChoices.CITY: nearest_city,
            LocationTypeChoices.REGION: nearest_city.region,
            LocationTypeChoices.COUNTRY: nearest_city.region.country,
        }
        return mapping.get(location_type)
    return None


# Re-export individual functions for granular control
__all__ = [
    "populate_geobank_data",
    "populate_languages",
    "populate_currencies",
    "populate_countries",
    "populate_regions",
    "populate_cities",
    "populate_flags",
    "translate_data",
    "LocationTypeChoices",
    "get_location_by_coordinates",
]
