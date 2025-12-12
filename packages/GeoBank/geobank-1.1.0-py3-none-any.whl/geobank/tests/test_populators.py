"""
Tests for the populators module.
"""

import io
import json
import zipfile
from unittest.mock import patch

from django.test import TestCase

from geobank.models import (
    City,
    Country,
    Currency,
    Language,
    Region,
)
from geobank.populators import (
    _apply_translations,
    _build_languages_map,
    _parse_translations,
    populate_cities,
    populate_countries,
    populate_currencies,
    populate_flags,
    populate_languages,
    populate_regions,
    translate_data,
)


class TestPopulateLanguages(TestCase):
    """Tests for populate_languages function."""

    @patch("geobank.populators.parse_languages_data")
    def test_populate_languages_creates_new(self, mock_parse):
        """Test that new languages are created."""
        mock_parse.return_value = {
            "eng": "English",
            "spa": "Spanish",
        }

        populate_languages()

        assert Language.objects.count() == 2
        eng = Language.objects.get(code="eng")
        assert eng.name == "English"
        assert eng.code2 == "en"

    @patch("geobank.populators.parse_languages_data")
    def test_populate_languages_updates_existing(self, mock_parse):
        """Test that existing languages are updated."""
        Language.objects.create(code="eng", code2="en", name="Old English")
        mock_parse.return_value = {"eng": "English"}

        populate_languages()

        eng = Language.objects.get(code="eng")
        assert eng.name == "English"


class TestPopulateCurrencies(TestCase):
    """Tests for populate_currencies function."""

    @patch("geobank.populators.parse_currencies_data")
    def test_populate_currencies_creates_new(self, mock_parse):
        """Test that new currencies are created."""
        mock_parse.return_value = {
            "USD": {"name": "US Dollar", "symbol": "$"},
            "EUR": {"name": "Euro", "symbol": "€"},
        }

        populate_currencies()

        assert Currency.objects.count() == 2
        usd = Currency.objects.get(code="USD")
        assert usd.name == "US Dollar"
        assert usd.symbol == "$"


class TestPopulateCountries(TestCase):
    """Tests for populate_countries function."""

    def setUp(self):
        """Set up test data."""
        self.currency = Currency.objects.create(code="USD", name="US Dollar", symbol="$")
        self.language = Language.objects.create(code="eng", code2="en", name="English")

    @patch("geobank.populators.parse_country_data")
    def test_populate_countries_creates_new(self, mock_parse):
        """Test that new countries are created."""
        mock_parse.return_value = [
            {
                "code2": "US",
                "code3": "USA",
                "fips": "US",
                "name": "United States",
                "name_ascii": "United States",
                "population": "331000000",
                "continent": "NA",
                "tld": ".us",
                "currency_code": "USD",
                "calling_codes": ["1"],
                "postal_code_format": "#####",
                "postal_code_regex": "^\\d{5}$",
                "languages": "en",
                "geoname_id": 6252001,
                "neighbors": "",
            }
        ]

        populate_countries()

        assert Country.objects.count() == 1
        us = Country.objects.get(code2="US")
        assert us.name == "United States"
        assert us.population == 331000000
        assert us.currency == self.currency

    @patch("geobank.populators.parse_country_data")
    def test_populate_countries_with_calling_codes(self, mock_parse):
        """Test that calling codes are created."""
        mock_parse.return_value = [
            {
                "code2": "US",
                "code3": "USA",
                "fips": "US",
                "name": "United States",
                "name_ascii": "United States",
                "population": "331000000",
                "continent": "NA",
                "tld": ".us",
                "currency_code": "USD",
                "calling_codes": ["1", "1809"],
                "postal_code_format": "",
                "postal_code_regex": "",
                "languages": "",
                "geoname_id": 6252001,
                "neighbors": "",
            }
        ]

        populate_countries()

        us = Country.objects.get(code2="US")
        calling_codes = list(us.calling_codes.values_list("code", flat=True))
        assert "1" in calling_codes
        assert "1809" in calling_codes

    @patch("geobank.populators.parse_country_data")
    def test_populate_countries_with_neighbors(self, mock_parse):
        """Test that neighbor relationships are set up."""
        Currency.objects.create(code="CAD", name="Canadian Dollar", symbol="$")
        mock_parse.return_value = [
            {
                "code2": "US",
                "code3": "USA",
                "fips": "US",
                "name": "United States",
                "name_ascii": "United States",
                "population": "331000000",
                "continent": "NA",
                "tld": ".us",
                "currency_code": "USD",
                "calling_codes": ["1"],
                "postal_code_format": "",
                "postal_code_regex": "",
                "languages": "",
                "geoname_id": 6252001,
                "neighbors": "CA",
            },
            {
                "code2": "CA",
                "code3": "CAN",
                "fips": "CA",
                "name": "Canada",
                "name_ascii": "Canada",
                "population": "38000000",
                "continent": "NA",
                "tld": ".ca",
                "currency_code": "CAD",
                "calling_codes": ["1"],
                "postal_code_format": "",
                "postal_code_regex": "",
                "languages": "",
                "geoname_id": 6251999,
                "neighbors": "US",
            },
        ]

        populate_countries()

        us = Country.objects.get(code2="US")
        ca = Country.objects.get(code2="CA")
        assert ca in us.neighbors.all()
        assert us in ca.neighbors.all()


class TestPopulateRegions(TestCase):
    """Tests for populate_regions function."""

    def setUp(self):
        """Set up test data."""
        self.country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            geoname_id=6252001,
            continent="NA",
        )

    @patch("geobank.populators.parse_region_data")
    def test_populate_regions_creates_new(self, mock_parse):
        """Test that new regions are created."""
        mock_parse.return_value = [
            {
                "country_code": "US",
                "region_code": "CA",
                "name": "California",
                "name_ascii": "California",
                "geoname_id": 5332921,
            },
            {
                "country_code": "US",
                "region_code": "NY",
                "name": "New York",
                "name_ascii": "New York",
                "geoname_id": 5128638,
            },
        ]

        populate_regions()

        assert Region.objects.count() == 2
        ca = Region.objects.get(code="CA")
        assert ca.name == "California"
        assert ca.country == self.country

    @patch("geobank.populators.parse_region_data")
    def test_populate_regions_updates_existing(self, mock_parse):
        """Test that existing regions are updated."""
        Region.objects.create(
            geoname_id=5332921,
            code="CA",
            name="Old California",
            name_ascii="Old California",
            country=self.country,
        )
        mock_parse.return_value = [
            {
                "country_code": "US",
                "region_code": "CA",
                "name": "California",
                "name_ascii": "California",
                "geoname_id": 5332921,
            },
        ]

        populate_regions()

        assert Region.objects.count() == 1
        ca = Region.objects.get(code="CA")
        assert ca.name == "California"


class TestPopulateCities(TestCase):
    """Tests for populate_cities function."""

    def setUp(self):
        """Set up test data."""
        self.country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            geoname_id=6252001,
            continent="NA",
        )
        self.region = Region.objects.create(
            geoname_id=5332921,
            code="CA",
            name="California",
            name_ascii="California",
            country=self.country,
        )

    @patch("geobank.populators.parse_city_data")
    def test_populate_cities_creates_new(self, mock_parse):
        """Test that new cities are created."""
        mock_parse.return_value = [
            {
                "geoname_id": 5368361,
                "name": "Los Angeles",
                "name_ascii": "Los Angeles",
                "latitude": "34.05223",
                "longitude": "-118.24368",
                "country_code": "US",
                "region_code": "CA",
                "population": 3979576,
                "timezone": "America/Los_Angeles",
            },
        ]

        populate_cities()

        assert City.objects.count() == 1
        la = City.objects.get(geoname_id=5368361)
        assert la.name == "Los Angeles"
        assert la.country == self.country
        assert la.region == self.region
        assert la.population == 3979576


class TestPopulateFlags(TestCase):
    """Tests for populate_flags function."""

    def setUp(self):
        """Set up test data."""
        self.country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            geoname_id=6252001,
            continent="NA",
        )

    @patch("geobank.populators.parse_flags_data")
    def test_populate_flags_updates_countries(self, mock_parse):
        """Test that flag URLs are set on countries."""
        mock_parse.return_value = {
            "US": {
                "png": "https://example.com/us.png",
                "svg": "https://example.com/us.svg",
            }
        }

        populate_flags()

        self.country.refresh_from_db()
        assert self.country.flag_png == "https://example.com/us.png"
        assert self.country.flag_svg == "https://example.com/us.svg"


class TestBuildLanguagesMap(TestCase):
    """Tests for _build_languages_map helper function."""

    def test_builds_map_with_both_codes(self):
        """Test that map includes both 2-letter and 3-letter codes."""
        lang = Language.objects.create(code="eng", code2="en", name="English")

        result = _build_languages_map()

        assert result["eng"] == lang
        assert result["en"] == lang

    def test_handles_missing_code2(self):
        """Test that languages without code2 are still included."""
        lang = Language.objects.create(code="qaa", code2="", name="Custom")

        result = _build_languages_map()

        assert result["qaa"] == lang
        assert "" not in result


class TestParseTranslations(TestCase):
    """Tests for _parse_translations function."""

    def setUp(self):
        """Set up test data."""
        self.country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            geoname_id=6252001,
            continent="NA",
        )
        self.entities = {6252001: self.country}

    def test_parse_translations_from_zip(self):
        """Test parsing translations from zip content."""
        translations_data = {
            "6252001": {
                "es": "Estados Unidos",
                "fr": "États-Unis",
            }
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("country_translations.json", json.dumps(translations_data))
            zf.writestr("region_translations.json", "{}")
            zf.writestr("city_translations.json", "{}")

        result = _parse_translations(zip_buffer.getvalue(), self.entities, ["es", "fr"])

        assert (6252001, "es") in result
        assert result[(6252001, "es")] == "Estados Unidos"
        assert result[(6252001, "fr")] == "États-Unis"

    def test_parse_translations_filters_languages(self):
        """Test that only requested languages are included."""
        translations_data = {
            "6252001": {
                "es": "Estados Unidos",
                "fr": "États-Unis",
                "de": "Vereinigte Staaten",
            }
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("country_translations.json", json.dumps(translations_data))
            zf.writestr("region_translations.json", "{}")
            zf.writestr("city_translations.json", "{}")

        result = _parse_translations(
            zip_buffer.getvalue(),
            self.entities,
            ["es"],  # Only Spanish
        )

        assert (6252001, "es") in result
        assert (6252001, "fr") not in result
        assert (6252001, "de") not in result

    def test_parse_translations_skips_unknown_entities(self):
        """Test that unknown geoname_ids are skipped."""
        translations_data = {
            "9999999": {"es": "Unknown"},  # Not in entities
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("country_translations.json", json.dumps(translations_data))
            zf.writestr("region_translations.json", "{}")
            zf.writestr("city_translations.json", "{}")

        result = _parse_translations(zip_buffer.getvalue(), self.entities, ["es"])

        assert len(result) == 0


class TestApplyTranslations(TestCase):
    """Tests for _apply_translations function."""

    def test_apply_translations_sets_fields(self):
        """Test that translations are applied to entity fields."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            geoname_id=6252001,
            continent="NA",
        )
        entities = {6252001: country}
        translations = {(6252001, "es"): "Estados Unidos"}

        # Mock the field existence
        with patch.object(Country, "name_es", create=True):
            result = _apply_translations(translations, entities)

        assert country in result


class TestTranslateData(TestCase):
    """Tests for translate_data function."""

    def setUp(self):
        """Set up test data."""
        self.country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            geoname_id=6252001,
            continent="NA",
        )

    @patch("geobank.populators._save_translations")
    @patch("geobank.populators._apply_translations")
    @patch("geobank.populators._parse_translations")
    @patch("geobank.populators.download_with_retry")
    def test_translate_data_workflow(self, mock_download, mock_parse, mock_apply, mock_save):
        """Test the complete translation workflow."""
        mock_download.return_value = b"zip content"
        mock_parse.return_value = {(6252001, "es"): "Estados Unidos"}
        mock_apply.return_value = {self.country}

        translate_data(["es"])

        mock_download.assert_called_once()
        mock_parse.assert_called_once()
        mock_apply.assert_called_once()
        mock_save.assert_called_once()

    @patch("geobank.populators.download_with_retry")
    def test_translate_data_handles_download_error(self, mock_download):
        """Test that download errors are handled gracefully."""
        mock_download.side_effect = Exception("Network error")

        # Should not raise
        translate_data(["es"])
