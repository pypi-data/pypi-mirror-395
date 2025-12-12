"""
Integration tests for geobank - real end-to-end tests without mocking.

These tests actually download data from remote sources and populate the database.
They are slower but provide full confidence that everything works correctly.

Run with: pytest src/geobank/tests/test_integration.py -v -s
"""

import pytest
from django.test import TestCase, TransactionTestCase

from geobank.constants import (
    GEOBANK_TRANSLATIONS_URL,
    GEONAMES_CITIES_URL_TEMPLATE,
    GEONAMES_COUNTRY_INFO_URL,
    GEONAMES_REGION_INFO_URL,
)
from geobank.downloaders import download_with_retry
from geobank.models import (
    CallingCode,
    City,
    Country,
    Currency,
    Language,
    Region,
)
from geobank.parsers import (
    parse_city_data,
    parse_country_data,
    parse_currencies_data,
    parse_flags_data,
    parse_languages_data,
    parse_region_data,
)
from geobank.populators import (
    populate_cities,
    populate_countries,
    populate_currencies,
    populate_flags,
    populate_languages,
    populate_regions,
)

# Mark all tests in this module as integration tests (slow)
pytestmark = pytest.mark.integration


class TestRealDownloads(TestCase):
    """Test actual downloads from remote sources."""

    def test_download_country_info(self):
        """Test downloading country info TSV file."""
        content = download_with_retry(GEONAMES_COUNTRY_INFO_URL)

        assert content is not None
        assert len(content) > 0

        # Should be valid TSV with country data
        text = content.decode("utf-8")
        lines = [line for line in text.splitlines() if line.strip() and not line.startswith("#")]

        # Should have many countries
        assert len(lines) >= 200, f"Expected at least 200 countries, got {len(lines)}"

        # Check first non-comment line has expected format (tab-separated)
        first_line = lines[0]
        parts = first_line.split("\t")
        assert len(parts) >= 17, f"Expected at least 17 columns, got {len(parts)}"

    def test_download_region_info(self):
        """Test downloading region info TSV file."""
        content = download_with_retry(GEONAMES_REGION_INFO_URL)

        assert content is not None
        assert len(content) > 0

        text = content.decode("utf-8")
        lines = [line for line in text.splitlines() if line.strip() and not line.startswith("#")]

        # Should have many regions
        assert len(lines) >= 1000, f"Expected at least 1000 regions, got {len(lines)}"

    def test_download_cities_zip(self):
        """Test downloading cities zip file."""
        url = GEONAMES_CITIES_URL_TEMPLATE.format(population=15000)
        content = download_with_retry(url)

        assert content is not None
        assert len(content) > 0

        # Check it's a valid zip file (starts with PK)
        assert content[:2] == b"PK", "Downloaded file is not a valid ZIP"

    def test_download_translations_zip(self):
        """Test downloading translations zip file."""
        content = download_with_retry(GEOBANK_TRANSLATIONS_URL)

        assert content is not None
        assert len(content) > 0

        # Check it's a valid zip file
        assert content[:2] == b"PK", "Downloaded file is not a valid ZIP"


class TestRealParsers(TestCase):
    """Test parsing real data from remote sources."""

    def test_parse_real_country_data(self):
        """Test parsing real country data."""
        data = parse_country_data()

        assert len(data) >= 200, f"Expected at least 200 countries, got {len(data)}"

        # Find United States
        us_data = next((c for c in data if c["code2"] == "US"), None)
        assert us_data is not None, "United States not found in data"
        assert us_data["code3"] == "USA"
        assert us_data["name"] == "United States"
        assert us_data["continent"] == "NA"
        assert us_data["currency_code"] == "USD"
        assert int(us_data["population"]) > 300000000

    def test_parse_real_region_data(self):
        """Test parsing real region data."""
        data = parse_region_data()

        assert len(data) >= 1000, f"Expected at least 1000 regions, got {len(data)}"

        # Find California
        ca_data = next(
            (r for r in data if r["country_code"] == "US" and r["region_code"] == "CA"), None
        )
        assert ca_data is not None, "California not found in data"
        assert "California" in ca_data["name"]

    def test_parse_real_city_data(self):
        """Test parsing real city data."""
        data = parse_city_data(population_gte=15000)

        assert len(data) >= 10000, f"Expected at least 10000 cities, got {len(data)}"

        # Find New York City (geoname_id: 5128581)
        nyc_data = next((c for c in data if c["geoname_id"] == 5128581), None)
        assert nyc_data is not None, "New York City not found in data"
        assert "New York" in nyc_data["name"]
        assert nyc_data["country_code"] == "US"

    def test_parse_real_languages_data(self):
        """Test parsing real languages from restcountries API."""
        data = parse_languages_data()

        assert len(data) >= 100, f"Expected at least 100 languages, got {len(data)}"
        assert "eng" in data
        assert "spa" in data
        assert "fra" in data

    def test_parse_real_currencies_data(self):
        """Test parsing real currencies from restcountries API."""
        data = parse_currencies_data()

        assert len(data) >= 100, f"Expected at least 100 currencies, got {len(data)}"
        assert "USD" in data
        assert "EUR" in data
        assert data["USD"]["symbol"] == "$"

    def test_parse_real_flags_data(self):
        """Test parsing real flags from restcountries API."""
        data = parse_flags_data()

        assert len(data) >= 200, f"Expected at least 200 countries with flags, got {len(data)}"
        assert "US" in data
        assert "png" in data["US"]
        assert "svg" in data["US"]
        assert data["US"]["png"].startswith("http")


class TestRealPopulators(TransactionTestCase):
    """
    Test real database population with actual data.

    Uses TransactionTestCase to ensure proper database cleanup between tests.
    """

    def test_full_population_workflow(self):
        """
        Test the complete population workflow with real data.

        This is the main integration test that verifies the entire pipeline works.
        """
        # Step 1: Populate languages
        populate_languages()
        language_count = Language.objects.count()
        assert language_count >= 100, f"Expected at least 100 languages, got {language_count}"

        # Verify English exists
        eng = Language.objects.filter(code="eng").first()
        assert eng is not None, "English language not created"
        assert eng.code2 == "en"

        # Step 2: Populate currencies
        populate_currencies()
        currency_count = Currency.objects.count()
        assert currency_count >= 100, f"Expected at least 100 currencies, got {currency_count}"

        # Verify USD exists
        usd = Currency.objects.filter(code="USD").first()
        assert usd is not None, "USD currency not created"
        assert usd.symbol == "$"

        # Step 3: Populate countries
        populate_countries()
        country_count = Country.objects.count()
        assert country_count >= 200, f"Expected at least 200 countries, got {country_count}"

        # Verify United States
        us = Country.objects.filter(code2="US").first()
        assert us is not None, "United States not created"
        assert us.code3 == "USA"
        assert us.continent == "NA"
        assert us.currency == usd
        assert us.population > 300000000

        # Verify calling codes
        us_calling_codes = list(us.calling_codes.values_list("code", flat=True))
        assert "1" in us_calling_codes, "US calling code +1 not found"

        # Verify neighbors
        canada = Country.objects.filter(code2="CA").first()
        assert canada is not None, "Canada not created"
        assert canada in us.neighbors.all(), "Canada should be a neighbor of US"

        # Step 4: Populate flags
        populate_flags()
        us.refresh_from_db()
        assert us.flag_png is not None, "US flag PNG not set"
        assert us.flag_svg is not None, "US flag SVG not set"
        assert "http" in us.flag_png

        # Step 5: Populate regions
        populate_regions()
        region_count = Region.objects.count()
        assert region_count >= 1000, f"Expected at least 1000 regions, got {region_count}"

        # Verify California
        california = Region.objects.filter(country=us, code="CA").first()
        assert california is not None, "California not created"
        assert "California" in california.name

        # Step 6: Populate cities (using smaller dataset for speed)
        populate_cities(population_gte=15000)
        city_count = City.objects.count()
        assert city_count >= 10000, f"Expected at least 10000 cities, got {city_count}"

        # Verify Los Angeles
        la = City.objects.filter(geoname_id=5368361).first()
        assert la is not None, "Los Angeles not created"
        assert "Los Angeles" in la.name
        assert la.country == us
        assert la.region == california
        assert la.population > 3000000

        # Verify New York City
        nyc = City.objects.filter(geoname_id=5128581).first()
        assert nyc is not None, "New York City not created"
        assert nyc.country == us

    def test_populate_languages_real(self):
        """Test populating languages with real API data."""
        populate_languages()

        # Check we got a reasonable number of languages
        count = Language.objects.count()
        assert count >= 100, f"Expected at least 100 languages, got {count}"

        # Check some specific languages exist
        assert Language.objects.filter(code="eng").exists(), "English not found"
        assert Language.objects.filter(code="spa").exists(), "Spanish not found"
        assert Language.objects.filter(code="zho").exists(), "Chinese not found"
        assert Language.objects.filter(code="ara").exists(), "Arabic not found"

        # Check code2 mapping works
        eng = Language.objects.get(code="eng")
        assert eng.code2 == "en"

    def test_populate_currencies_real(self):
        """Test populating currencies with real API data."""
        populate_currencies()

        count = Currency.objects.count()
        assert count >= 100, f"Expected at least 100 currencies, got {count}"

        # Check some specific currencies
        usd = Currency.objects.filter(code="USD").first()
        assert usd is not None
        assert usd.symbol == "$"

        eur = Currency.objects.filter(code="EUR").first()
        assert eur is not None
        assert eur.symbol == "€"

    def test_populate_countries_real(self):
        """Test populating countries with real data."""
        # Need languages and currencies first
        populate_languages()
        populate_currencies()
        populate_countries()

        count = Country.objects.count()
        assert count >= 200, f"Expected at least 200 countries, got {count}"

        # Verify specific countries
        us = Country.objects.get(code2="US")
        assert us.code3 == "USA"
        assert us.population > 300000000

        # Verify ManyToMany relationships work
        assert us.languages.count() > 0, "US should have languages"
        assert us.neighbors.count() > 0, "US should have neighbors"

    def test_populate_regions_real(self):
        """Test populating regions with real data."""
        # Need countries first
        populate_languages()
        populate_currencies()
        populate_countries()
        populate_regions()

        count = Region.objects.count()
        assert count >= 1000, f"Expected at least 1000 regions, got {count}"

        # Verify US regions
        us = Country.objects.get(code2="US")
        us_regions = Region.objects.filter(country=us)
        assert us_regions.count() >= 50, "US should have at least 50 regions/states"

    def test_populate_cities_real(self):
        """Test populating cities with real data."""
        # Need countries and regions first
        populate_languages()
        populate_currencies()
        populate_countries()
        populate_regions()
        populate_cities(population_gte=15000)

        count = City.objects.count()
        assert count >= 10000, f"Expected at least 10000 cities, got {count}"

        # Verify relationships
        us = Country.objects.get(code2="US")
        us_cities = City.objects.filter(country=us)
        assert us_cities.count() >= 500, "US should have at least 500 cities"

    def test_idempotent_population(self):
        """Test that running population twice doesn't create duplicates."""
        populate_languages()
        populate_currencies()
        populate_countries()

        first_count = Country.objects.count()

        # Run again
        populate_languages()
        populate_currencies()
        populate_countries()

        second_count = Country.objects.count()

        assert first_count == second_count, "Population should be idempotent"

    def test_update_existing_data(self):
        """Test that existing data gets updated correctly."""
        # Create a country with old data
        Country.objects.create(
            geoname_id=6252001,  # US geoname_id
            code2="US",
            code3="USA",
            name="Old United States Name",
            continent="NA",
            population=1,
        )

        # Need dependencies
        populate_languages()
        populate_currencies()

        # Now populate - should update the existing country
        populate_countries()

        us = Country.objects.get(code2="US")
        assert us.name == "United States", "Country name should be updated"
        assert us.population > 300000000, "Population should be updated"


class TestRealTranslations(TransactionTestCase):
    """Test real translation functionality."""

    def test_translation_download_and_parse(self):
        """Test that translations can be downloaded and parsed."""
        import io
        import json
        import zipfile

        content = download_with_retry(GEOBANK_TRANSLATIONS_URL)
        assert content is not None

        # Parse the zip
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            filenames = z.namelist()

            # Should contain translation files
            assert "country_translations.json" in filenames
            assert "region_translations.json" in filenames
            assert "city_translations.json" in filenames

            # Parse country translations
            with z.open("country_translations.json") as f:
                country_trans = json.load(f)

                # Should have translations for many countries
                assert len(country_trans) >= 100

                # Check US translations exist (geoname_id: 6252001)
                us_trans = country_trans.get("6252001", {})
                assert len(us_trans) > 0, "US should have translations"


class TestDataIntegrity(TransactionTestCase):
    """Test data integrity after full population."""

    def test_foreign_key_integrity(self):
        """Test that all foreign key relationships are valid."""
        populate_languages()
        populate_currencies()
        populate_countries()
        populate_regions()
        populate_cities(population_gte=15000)

        # All cities should have valid countries
        orphan_cities = City.objects.filter(country__isnull=True).count()
        assert orphan_cities == 0, f"Found {orphan_cities} cities without countries"

        # All regions should have valid countries
        orphan_regions = Region.objects.filter(country__isnull=True).count()
        assert orphan_regions == 0, f"Found {orphan_regions} regions without countries"

        # All calling codes should have valid countries
        orphan_codes = CallingCode.objects.filter(country__isnull=True).count()
        assert orphan_codes == 0, f"Found {orphan_codes} calling codes without countries"

    def test_unique_constraints(self):
        """Test that unique constraints are respected."""
        populate_languages()
        populate_currencies()
        populate_countries()
        populate_regions()

        # All country codes should be unique
        from django.db.models import Count

        duplicates = Country.objects.values("code2").annotate(count=Count("id")).filter(count__gt=1)
        assert duplicates.count() == 0, f"Found duplicate country codes: {list(duplicates)}"

        # All language codes should be unique
        duplicates = Language.objects.values("code").annotate(count=Count("id")).filter(count__gt=1)
        assert duplicates.count() == 0, f"Found duplicate language codes: {list(duplicates)}"

    def test_geoname_id_uniqueness(self):
        """Test that geoname_ids are unique across entities."""
        populate_languages()
        populate_currencies()
        populate_countries()
        populate_regions()
        populate_cities(population_gte=15000)

        # Collect all geoname_ids
        country_ids = set(Country.objects.values_list("geoname_id", flat=True))
        region_ids = set(Region.objects.values_list("geoname_id", flat=True))
        city_ids = set(City.objects.values_list("geoname_id", flat=True))

        # Each should be unique within its own model
        assert len(country_ids) == Country.objects.count()
        assert len(region_ids) == Region.objects.count()
        assert len(city_ids) == City.objects.count()
