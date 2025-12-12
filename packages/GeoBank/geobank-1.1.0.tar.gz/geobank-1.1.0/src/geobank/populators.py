"""
Database population functions for populating geobank models with data.
"""

import json
import logging
import zipfile

from django.core.exceptions import FieldDoesNotExist
from django.db import transaction

from .constants import (
    GEOBANK_TRANSLATIONS_URL,
    ISO_639_2_TO_1,
)
from .downloaders import download_with_retry
from .models import CallingCode, City, Country, Currency, Language, Region
from .parsers import (
    parse_city_data,
    parse_country_data,
    parse_currencies_data,
    parse_flags_data,
    parse_languages_data,
    parse_region_data,
)

logger = logging.getLogger(__name__)


def populate_languages():
    """Populate Language model from restcountries API data."""
    logger.info("Populating languages...")

    try:
        all_languages = parse_languages_data()

        for code, name in all_languages.items():
            # Get the 2-letter code if it exists
            code2 = ISO_639_2_TO_1.get(code, "")
            Language.objects.update_or_create(
                code=code,
                defaults={
                    "code2": code2,
                    "name": name,
                },
            )
    except Exception as e:
        logger.error(f"Error populating languages: {e}")


def populate_currencies():
    """Populate Currency model from restcountries API data."""
    logger.info("Populating currencies...")

    try:
        all_currencies = parse_currencies_data()

        for code, info in all_currencies.items():
            Currency.objects.update_or_create(
                code=code,
                defaults={
                    "name": info["name"],
                    "symbol": info["symbol"],
                },
            )
    except Exception as e:
        logger.error(f"Error populating currencies: {e}")


def populate_countries():
    """Populate Country model and related data from geonames."""
    logger.info("Populating countries...")
    data = parse_country_data()

    # Build lookup maps
    currencies = {c.code: c for c in Currency.objects.all()}
    languages_map = _build_languages_map()

    # Store country data for neighbor processing
    country_neighbors_map = {}

    for item in data:
        country = _create_or_update_country(item, currencies)
        _update_calling_codes(country, item["calling_codes"])
        _assign_languages(country, item["languages"], languages_map)

        # Store neighbors for later processing (after all countries are created)
        if item["neighbors"]:
            country_neighbors_map[item["code2"]] = item["neighbors"].split(",")

    # Update neighbors (second pass, after all countries exist)
    _update_neighbors(country_neighbors_map)


def _build_languages_map():
    """Build a map of language codes to Language objects (both 2-letter and 3-letter)."""
    languages_map = {}
    for lang in Language.objects.all():
        languages_map[lang.code] = lang  # 3-letter code
        if lang.code2:
            languages_map[lang.code2] = lang  # 2-letter code
    return languages_map


def _create_or_update_country(item, currencies):
    """Create or update a country record."""
    # Parse population
    try:
        population = int(item["population"]) if item["population"] else None
    except ValueError:
        population = None

    # Get currency
    currency = currencies.get(item["currency_code"])

    country, _ = Country.objects.update_or_create(
        geoname_id=item["geoname_id"],
        defaults={
            "name": item["name"],
            "name_ascii": item["name_ascii"],
            "fips": item["fips"],
            "continent": item["continent"],
            "population": population,
            "tld": item["tld"],
            "code2": item["code2"],
            "code3": item["code3"],
            "currency": currency,
            "postal_code_format": item["postal_code_format"],
            "postal_code_regex": item["postal_code_regex"],
        },
    )
    return country


def _update_calling_codes(country, calling_codes):
    """Update calling codes for a country."""
    country.calling_codes.all().delete()
    for code in calling_codes:
        CallingCode.objects.create(country=country, code=code)


def _assign_languages(country, languages_str, languages_map):
    """Assign languages to a country based on geonames language codes."""
    # Geonames uses 2-letter codes like "en", "ar-AE", "fa-AF"
    if languages_str:
        lang_codes = languages_str.split(",")
        country_languages = []
        for lang_code in lang_codes:
            # Language codes can be like "en-US" or "en", we want the base 2-letter code
            base_code = lang_code.split("-")[0].strip().lower()
            if base_code and base_code in languages_map:
                country_languages.append(languages_map[base_code])
        country.languages.set(country_languages)


def _update_neighbors(country_neighbors_map):
    """Update neighbor relationships for all countries."""
    logger.info("Updating country neighbors...")
    countries_by_code = {c.code2: c for c in Country.objects.all()}

    for country_code, neighbor_codes in country_neighbors_map.items():
        country = countries_by_code.get(country_code)
        if country:
            neighbors = []
            for neighbor_code in neighbor_codes:
                neighbor_code = neighbor_code.strip()
                if neighbor_code and neighbor_code in countries_by_code:
                    neighbors.append(countries_by_code[neighbor_code])
            country.neighbors.set(neighbors)


def populate_regions():
    """Populate Region model from geonames data."""
    logger.info("Populating regions...")
    data = parse_region_data()

    countries = {c.code2: c for c in Country.objects.all()}

    # Load existing regions
    existing = {r.geoname_id: r for r in Region.objects.all()}

    to_create = []
    to_update = []

    for item in data:
        country = countries.get(item["country_code"])
        if not country:
            continue

        geo_id = item["geoname_id"]
        name = item["name"]
        code = item["region_code"]
        name_ascii = item["name_ascii"]

        if geo_id in existing:
            # Update existing region
            obj = existing[geo_id]
            obj.name = name
            obj.code = code
            obj.name_ascii = name_ascii
            obj.country = country
            to_update.append(obj)
        else:
            # Create a new region
            to_create.append(
                Region(
                    geoname_id=geo_id,
                    name=name,
                    code=code,
                    name_ascii=name_ascii,
                    country=country,
                )
            )

    # Bulk operations
    if to_create:
        Region.objects.bulk_create(to_create, batch_size=5000)

    if to_update:
        Region.objects.bulk_update(
            to_update,
            fields=["name", "code", "name_ascii", "country"],
            batch_size=5000,
        )

    logger.info(f"Regions populated. Created: {len(to_create)}, Updated: {len(to_update)}")


def populate_cities(population_gte: int = 15000):
    logger.info("Populating cities...")
    data = parse_city_data(population_gte)

    countries = {c.code2: c for c in Country.objects.all()}
    regions = {f"{r.country.code2},{r.code}": r for r in Region.objects.all()}

    # Fetch existing cities by geoname_id (NOT by PK)
    existing = City.objects.in_bulk(field_name="geoname_id")

    new_objects = []
    update_objects = []

    for item in data:
        country = countries.get(item["country_code"])
        region = regions.get(f"{item['country_code']},{item['region_code']}")

        if not country:
            continue

        try:
            latitude = float(item["latitude"])
            longitude = float(item["longitude"])
        except (TypeError, ValueError):
            latitude = longitude = None

        geoname_id = item["geoname_id"]

        if geoname_id in existing:
            # UPDATE existing instance (which already includes correct PK)
            obj = existing[geoname_id]
            obj.name = item["name"]
            obj.name_ascii = item["name_ascii"]
            obj.latitude = latitude
            obj.longitude = longitude
            obj.country = country
            obj.region = region
            obj.population = item["population"]
            obj.timezone = item["timezone"]

            update_objects.append(obj)

        else:
            # CREATE new instance
            new_objects.append(
                City(
                    geoname_id=geoname_id,
                    name=item["name"],
                    name_ascii=item["name_ascii"],
                    latitude=latitude,
                    longitude=longitude,
                    country=country,
                    region=region,
                    population=item["population"],
                    timezone=item["timezone"],
                )
            )

    logger.info(f"Creating {len(new_objects)} new cities...")
    logger.info(f"Updating {len(update_objects)} existing cities...")

    with transaction.atomic():
        if new_objects:
            City.objects.bulk_create(new_objects, batch_size=1000)

        if update_objects:
            City.objects.bulk_update(
                update_objects,
                fields=[
                    "name",
                    "name_ascii",
                    "latitude",
                    "longitude",
                    "country",
                    "region",
                    "population",
                    "timezone",
                ],
                batch_size=1000,
            )


def populate_flags():
    """Populate flag URLs for countries from restcountries API."""
    logger.info("Populating flags...")

    flags_data = parse_flags_data()

    countries = Country.objects.all()
    for country in countries:
        country_flags = flags_data.get(country.code2)
        if country_flags:
            country.flag_png = country_flags.get("png")
            country.flag_svg = country_flags.get("svg")
            country.save(update_fields=["flag_png", "flag_svg"])


def translate_data(languages):
    """
    Translate entity names using geobank translations data.

    Args:
        languages: List of language codes to translate.
    """
    logger.info("Starting translation...")

    # Map geoname_id to model instance
    entities = _load_entities()
    logger.info(f"Loaded {len(entities)} entities.")

    try:
        logger.info(f"Downloading translations from {GEOBANK_TRANSLATIONS_URL}")
        content = download_with_retry(GEOBANK_TRANSLATIONS_URL)

        logger.info("Processing translations...")
        translations = _parse_translations(content, entities, languages)

        logger.info("Applying translations...")
        modified_instances = _apply_translations(translations, entities)

        logger.info("Saving translations...")
        _save_translations(modified_instances, languages)

    except Exception as e:
        logger.error(f"Error processing translations: {e}")


def _load_entities():
    """Load all translatable entities into memory."""
    logger.info("Loading entities into memory...")
    entities = {}
    for country in Country.objects.all():
        entities[country.geoname_id] = country
    for region in Region.objects.all():
        entities[region.geoname_id] = region
    for city in City.objects.all():
        entities[city.geoname_id] = city
    return entities


def _parse_translations(content, entities, languages):
    """Parse translations from the geobank translations zip file.

    The zip file contains three JSON files:
    - country_translations.json
    - region_translations.json
    - city_translations.json

    Each file has the structure:
    {
        "geoname_id": {
            "lang_code": "translated_name",
            ...
        },
        ...
    }

    Args:
        content: The raw bytes content of the zip file.
        entities: Dict mapping geoname_id to model instances.
        languages: List of language codes to include.
    """
    import io

    translations = {}  # (geoname_id, lang) -> name

    translation_files = [
        "country_translations.json",
        "region_translations.json",
        "city_translations.json",
    ]

    with zipfile.ZipFile(io.BytesIO(content)) as z:
        for filename in translation_files:
            try:
                with z.open(filename) as f:
                    data = json.load(f)

                    for geoname_id_str, lang_dict in data.items():
                        try:
                            geoname_id = int(geoname_id_str)
                        except ValueError:
                            continue

                        if geoname_id not in entities:
                            continue

                        for lang, name in lang_dict.items():
                            if lang not in languages:
                                continue

                            translations[(geoname_id, lang)] = name
            except KeyError:
                logger.warning(f"Translation file {filename} not found in zip")
                continue

    return translations


def _apply_translations(translations, entities):
    """Apply translations to entities."""
    modified_instances = set()

    for (geoname_id, lang), name in translations.items():
        instance = entities[geoname_id]
        field_name = f"name_{lang}"
        if hasattr(instance, field_name):
            setattr(instance, field_name, name)
            modified_instances.add(instance)

    return modified_instances


def _save_translations(modified_instances, languages):
    """Save translated entities to database."""
    countries_to_update = []
    regions_to_update = []
    cities_to_update = []

    for instance in modified_instances:
        if isinstance(instance, Country):
            countries_to_update.append(instance)
        elif isinstance(instance, Region):
            regions_to_update.append(instance)
        elif isinstance(instance, City):
            cities_to_update.append(instance)

    # Ensure translation fields exist
    for lang in languages:
        for model in (Country, Region, City):
            _ensure_field(model, f"name_{lang}")

    update_fields = [f"name_{lang}" for lang in languages]

    if countries_to_update:
        Country.objects.bulk_update(countries_to_update, update_fields)
    if regions_to_update:
        Region.objects.bulk_update(regions_to_update, update_fields)
    if cities_to_update:
        City.objects.bulk_update(cities_to_update, update_fields)


def _ensure_field(model, field_name):
    """Ensure a field exists on a model."""
    try:
        model._meta.get_field(field_name)
    except FieldDoesNotExist:
        logger.error(f"Field '{field_name}' does not exist on {model.__name__}.")
        exit(1)
