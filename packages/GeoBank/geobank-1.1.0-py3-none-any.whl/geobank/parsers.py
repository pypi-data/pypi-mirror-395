"""
Data parsing functions for fetching and parsing geographic data from external sources.
"""

import io
import json
import logging
import zipfile

from .constants import (
    GEONAMES_CITIES_URL_TEMPLATE,
    GEONAMES_COUNTRY_INFO_URL,
    GEONAMES_REGION_INFO_URL,
    RESTCOUNTRIES_CURRENCIES_URL,
    RESTCOUNTRIES_FLAGS_URL,
    RESTCOUNTRIES_LANGUAGES_URL,
)
from .downloaders import download_with_retry

logger = logging.getLogger(__name__)


def parse_country_data():
    """
    Fetches and parses country data from geonames.org.

    Returns:
        list: List of dictionaries containing country data.
    """
    data = []
    try:
        content_bytes = download_with_retry(GEONAMES_COUNTRY_INFO_URL)
        content = content_bytes.decode("utf-8")

        for line in content.splitlines():
            if line.startswith("#") or not line.strip():
                continue

            parts = line.split("\t")
            if len(parts) < 17:
                continue

            # ISO(0), ISO3(1), ISO-Numeric(2), fips(3), Country(4), Capital(5), Area(6),
            # Population(7), Continent(8), tld(9), CurrencyCode(10), CurrencyName(11),
            # Phone(12), Postal Code Format(13), Postal Code Regex(14), Languages(15),
            # geonameid(16), neighbours(17), EquivalentFipsCode(18)

            try:
                geoname_id = int(parts[16])
            except ValueError:
                continue

            calling_codes = _parse_calling_codes(parts[12])

            data.append(
                {
                    "code2": parts[0],
                    "code3": parts[1],
                    "fips": parts[3],
                    "name": parts[4],
                    "name_ascii": parts[4],  # Assuming ASCII/English
                    "population": parts[7],
                    "continent": parts[8],
                    "tld": parts[9],
                    "currency_code": parts[10],
                    "currency_name": parts[11],
                    "calling_codes": calling_codes,
                    "postal_code_format": parts[13],
                    "postal_code_regex": parts[14],
                    "languages": parts[15],
                    "geoname_id": geoname_id,
                    "neighbors": parts[17],
                }
            )
    except Exception as e:
        logger.error(f"Error fetching country data: {e}")

    return data


def _parse_calling_codes(raw_calling_code: str) -> list:
    """
    Parse calling codes from raw string.
    Handles cases like "+1-809 and 1-829" by splitting and cleaning.

    Args:
        raw_calling_code: Raw calling code string from geonames.

    Returns:
        list: List of cleaned calling codes (numbers only).
    """
    calling_codes = []
    if raw_calling_code:
        # Split by " and " for cases like "+1-809 and 1-829"
        for part in raw_calling_code.split(" and "):
            # Remove + and - and whitespace
            clean_code = part.replace("+", "").replace("-", "").strip()
            if clean_code:
                calling_codes.append(clean_code)
    return calling_codes


def parse_region_data():
    """
    Fetches and parses region data from geonames.org.

    Returns:
        list: List of dictionaries containing region data.
    """
    data = []
    try:
        content_bytes = download_with_retry(GEONAMES_REGION_INFO_URL)
        content = content_bytes.decode("utf-8")

        for line in content.splitlines():
            if line.startswith("#") or not line.strip():
                continue

            parts = line.split("\t")
            if len(parts) < 4:
                continue

            # code(0), name(1), name_ascii(2), geoname_id(3)
            code_parts = parts[0].split(".")
            if len(code_parts) < 2:
                continue

            country_code = code_parts[0]
            region_code = code_parts[1]

            try:
                geoname_id = int(parts[3])
            except ValueError:
                continue

            data.append(
                {
                    "country_code": country_code,
                    "region_code": region_code,
                    "name": parts[1],
                    "name_ascii": parts[2],
                    "geoname_id": geoname_id,
                }
            )
    except Exception as e:
        logger.error(f"Error fetching region data: {e}")

    return data


def parse_city_data(population_gte: int = 15000):
    """
    Fetches and parses city data from geonames.org.

    Args:
        population_gte: Minimum population threshold for cities.

    Returns:
        list: List of dictionaries containing city data.
    """
    file_name = f"cities{population_gte}"
    url = GEONAMES_CITIES_URL_TEMPLATE.format(population=population_gte)
    data = []

    try:
        zip_content = download_with_retry(url)

        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            with z.open(f"{file_name}.txt") as f:
                with io.TextIOWrapper(f, encoding="utf-8") as text_file:
                    for line in text_file:
                        if not line.strip():
                            continue

                        parts = line.split("\t")
                        if len(parts) < 19:
                            continue

                        try:
                            geoname_id = int(parts[0])
                        except ValueError:
                            continue

                        # Parse population
                        try:
                            population = int(parts[14]) if parts[14] else None
                        except ValueError:
                            population = None

                        data.append(
                            {
                                "geoname_id": geoname_id,
                                "name": parts[1],
                                "name_ascii": parts[2],
                                "latitude": parts[4],
                                "longitude": parts[5],
                                "country_code": parts[8],
                                "region_code": parts[10],
                                "population": population,
                                "timezone": parts[17] if len(parts) > 17 else None,
                            }
                        )
    except Exception as e:
        logger.error(f"Error fetching city data: {e}")

    return data


def parse_languages_data():
    """
    Fetches and parses language data from restcountries API.

    Returns:
        dict: Dictionary mapping language codes to names.
    """
    all_languages = {}
    try:
        response_data = json.loads(download_with_retry(RESTCOUNTRIES_LANGUAGES_URL))
        for country_data in response_data:
            languages = country_data.get("languages", {})
            for code, name in languages.items():
                if code and len(code) == 3:  # 3-letter ISO 639-2 codes
                    all_languages[code.lower()] = name
    except Exception as e:
        logger.error(f"Error fetching languages data: {e}")

    return all_languages


def parse_currencies_data():
    """
    Fetches and parses currency data from restcountries API.

    Returns:
        dict: Dictionary mapping currency codes to info dicts.
    """
    all_currencies = {}
    try:
        response_data = json.loads(download_with_retry(RESTCOUNTRIES_CURRENCIES_URL))
        for country_data in response_data:
            currencies = country_data.get("currencies", {})
            for code, info in currencies.items():
                if code and len(code) == 3:
                    all_currencies[code] = {
                        "name": info.get("name", ""),
                        "symbol": info.get("symbol", ""),
                    }
    except Exception as e:
        logger.error(f"Error fetching currencies data: {e}")

    return all_currencies


def parse_flags_data():
    """
    Fetches and parses flag data from restcountries API.

    Returns:
        dict: Dictionary mapping country codes to flag URLs.
    """
    flags_data = {}
    try:
        response_data = json.loads(download_with_retry(RESTCOUNTRIES_FLAGS_URL))
        for row in response_data:
            flags_data[row["cca2"]] = row["flags"]
    except Exception as e:
        logger.error(f"Error fetching flags data: {e}")

    return flags_data
