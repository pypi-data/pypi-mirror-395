"""
Tests for the models module.
"""

import pytest
from django.test import TestCase

from geobank.models import (
    CallingCode,
    City,
    Country,
    Currency,
    Language,
    Region,
)


class TestLanguageModel(TestCase):
    """Tests for Language model."""

    def test_create_language(self):
        """Test creating a language."""
        lang = Language.objects.create(
            code="eng",
            code2="en",
            name="English",
        )

        assert lang.code == "eng"
        assert lang.code2 == "en"
        assert lang.name == "English"
        assert lang.is_active is True

    def test_language_str(self):
        """Test language string representation."""
        lang = Language.objects.create(code="eng", name="English")
        assert str(lang) == "English"

    def test_language_code_unique(self):
        """Test that language code is unique."""
        from django.db import IntegrityError

        Language.objects.create(code="eng", name="English")

        with pytest.raises(IntegrityError):
            Language.objects.create(code="eng", name="English 2")


class TestCurrencyModel(TestCase):
    """Tests for Currency model."""

    def test_create_currency(self):
        """Test creating a currency."""
        currency = Currency.objects.create(
            code="USD",
            name="US Dollar",
            symbol="$",
        )

        assert currency.code == "USD"
        assert currency.name == "US Dollar"
        assert currency.symbol == "$"
        assert currency.is_active is True

    def test_currency_str(self):
        """Test currency string representation."""
        currency = Currency.objects.create(
            code="USD",
            name="US Dollar",
            symbol="$",
        )
        assert str(currency) == "US Dollar (USD)"


class TestCountryModel(TestCase):
    """Tests for Country model."""

    def test_create_country(self):
        """Test creating a country."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            name_ascii="United States",
            continent="NA",
            geoname_id=6252001,
        )

        assert country.code2 == "US"
        assert country.code3 == "USA"
        assert country.name == "United States"
        assert country.is_active is True

    def test_country_str(self):
        """Test country string representation."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        assert str(country) == "United States"

    def test_country_with_currency(self):
        """Test country with currency relationship."""
        currency = Currency.objects.create(code="USD", name="US Dollar", symbol="$")
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
            currency=currency,
        )

        assert country.currency == currency
        assert country in currency.countries.all()

    def test_country_with_languages(self):
        """Test country with languages relationship."""
        lang1 = Language.objects.create(code="eng", name="English")
        lang2 = Language.objects.create(code="spa", name="Spanish")
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        country.languages.set([lang1, lang2])

        assert lang1 in country.languages.all()
        assert lang2 in country.languages.all()

    def test_country_neighbors(self):
        """Test country neighbors relationship."""
        usa = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        canada = Country.objects.create(
            code2="CA",
            code3="CAN",
            name="Canada",
            continent="NA",
        )
        usa.neighbors.add(canada)

        assert canada in usa.neighbors.all()
        # ManyToMany with 'self' is symmetrical by default
        assert usa in canada.neighbors.all()


class TestCallingCodeModel(TestCase):
    """Tests for CallingCode model."""

    def test_create_calling_code(self):
        """Test creating a calling code."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        calling_code = CallingCode.objects.create(
            country=country,
            code="1",
        )

        assert calling_code.country == country
        assert calling_code.code == "1"

    def test_calling_code_str(self):
        """Test calling code string representation."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        calling_code = CallingCode.objects.create(country=country, code="1")

        assert str(calling_code) == "United States: 1"

    def test_multiple_calling_codes(self):
        """Test country with multiple calling codes."""
        country = Country.objects.create(
            code2="DO",
            code3="DOM",
            name="Dominican Republic",
            continent="NA",
        )
        CallingCode.objects.create(country=country, code="1809")
        CallingCode.objects.create(country=country, code="1829")
        CallingCode.objects.create(country=country, code="1849")

        assert country.calling_codes.count() == 3


class TestRegionModel(TestCase):
    """Tests for Region model."""

    def test_create_region(self):
        """Test creating a region."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        region = Region.objects.create(
            geoname_id=5332921,
            code="CA",
            name="California",
            name_ascii="California",
            country=country,
        )

        assert region.code == "CA"
        assert region.name == "California"
        assert region.country == country
        assert region.is_active is True

    def test_region_str(self):
        """Test region string representation."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        region = Region.objects.create(
            code="CA",
            name="California",
            country=country,
        )

        assert str(region) == "California (US)"

    def test_region_unique_together(self):
        """Test that country + code is unique."""
        from django.db import IntegrityError

        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        Region.objects.create(code="CA", name="California", country=country)

        with pytest.raises(IntegrityError):
            Region.objects.create(code="CA", name="California 2", country=country)


class TestCityModel(TestCase):
    """Tests for City model."""

    def test_create_city(self):
        """Test creating a city."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        city = City.objects.create(
            geoname_id=5368361,
            name="Los Angeles",
            name_ascii="Los Angeles",
            country=country,
            latitude=34.052235,
            longitude=-118.243683,
            population=3979576,
            timezone="America/Los_Angeles",
        )

        assert city.name == "Los Angeles"
        assert city.country == country
        assert city.population == 3979576
        assert city.is_active is True

    def test_city_str(self):
        """Test city string representation."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        city = City.objects.create(
            name="Los Angeles",
            country=country,
        )

        assert str(city) == "Los Angeles, US"

    def test_city_with_region(self):
        """Test city with region relationship."""
        country = Country.objects.create(
            code2="US",
            code3="USA",
            name="United States",
            continent="NA",
        )
        region = Region.objects.create(
            code="CA",
            name="California",
            country=country,
        )
        city = City.objects.create(
            name="Los Angeles",
            country=country,
            region=region,
        )

        assert city.region == region
        assert city in region.cities.all()
