"""
Tests for the parsers module.
"""

import io
import json
import zipfile
from unittest.mock import patch

from geobank.parsers import (
    _parse_calling_codes,
    parse_city_data,
    parse_country_data,
    parse_currencies_data,
    parse_flags_data,
    parse_languages_data,
    parse_region_data,
)


class TestParseCallingCodes:
    """Tests for _parse_calling_codes helper function."""

    def test_simple_calling_code(self):
        """Test parsing a simple calling code."""
        result = _parse_calling_codes("+1")
        assert result == ["1"]

    def test_calling_code_with_dash(self):
        """Test parsing a calling code with dashes."""
        result = _parse_calling_codes("+1-809")
        assert result == ["1809"]

    def test_multiple_calling_codes(self):
        """Test parsing multiple calling codes with 'and'."""
        result = _parse_calling_codes("+1-809 and 1-829")
        assert result == ["1809", "1829"]

    def test_empty_calling_code(self):
        """Test parsing empty calling code."""
        result = _parse_calling_codes("")
        assert result == []

    def test_calling_code_with_whitespace(self):
        """Test parsing calling code with whitespace."""
        result = _parse_calling_codes("  +44  ")
        assert result == ["44"]


class TestParseCountryData:
    """Tests for parse_country_data function."""

    @patch("geobank.parsers.download_with_retry")
    def test_parse_country_data_success(self, mock_download):
        """Test successful parsing of country data."""
        tsv_content = (
            "# Comment line\n"
            "US\tUSA\t840\tUS\tUnited States\tWashington\t9833520\t331002651\tNA\t.us\tUSD\tDollar\t1\t#####-####\t^\\d{5}(-\\d{4})?$\ten\t6252001\tCA,MX\t\n"
            "CA\tCAN\t124\tCA\tCanada\tOttawa\t9984670\t37742154\tNA\t.ca\tCAD\tDollar\t1\tA#A #A#\t^[a-zA-Z]\\d[a-zA-Z]\\s?\\d[a-zA-Z]\\d$\ten,fr\t6251999\tUS\t\n"
        )
        mock_download.return_value = tsv_content.encode("utf-8")

        result = parse_country_data()

        assert len(result) == 2

        us = result[0]
        assert us["code2"] == "US"
        assert us["code3"] == "USA"
        assert us["name"] == "United States"
        assert us["population"] == "331002651"
        assert us["continent"] == "NA"
        assert us["currency_code"] == "USD"
        assert us["geoname_id"] == 6252001
        assert us["neighbors"] == "CA,MX"
        assert us["calling_codes"] == ["1"]

    @patch("geobank.parsers.download_with_retry")
    def test_parse_country_data_skips_invalid_lines(self, mock_download):
        """Test that invalid lines are skipped."""
        tsv_content = (
            "# Comment\n"
            "Invalid line with not enough fields\n"
            "US\tUSA\t840\tUS\tUnited States\tWashington\t9833520\t331002651\tNA\t.us\tUSD\tDollar\t1\t#####\t^\\d{5}$\ten\t6252001\tCA\t\n"
        )
        mock_download.return_value = tsv_content.encode("utf-8")

        result = parse_country_data()

        assert len(result) == 1
        assert result[0]["code2"] == "US"

    @patch("geobank.parsers.download_with_retry")
    def test_parse_country_data_handles_error(self, mock_download):
        """Test that errors are handled gracefully."""
        mock_download.side_effect = Exception("Network error")

        result = parse_country_data()

        assert result == []


class TestParseRegionData:
    """Tests for parse_region_data function."""

    @patch("geobank.parsers.download_with_retry")
    def test_parse_region_data_success(self, mock_download):
        """Test successful parsing of region data."""
        tsv_content = "US.CA\tCalifornia\tCalifornia\t5332921\nUS.NY\tNew York\tNew York\t5128638\n"
        mock_download.return_value = tsv_content.encode("utf-8")

        result = parse_region_data()

        assert len(result) == 2

        ca = result[0]
        assert ca["country_code"] == "US"
        assert ca["region_code"] == "CA"
        assert ca["name"] == "California"
        assert ca["name_ascii"] == "California"
        assert ca["geoname_id"] == 5332921

    @patch("geobank.parsers.download_with_retry")
    def test_parse_region_data_skips_invalid(self, mock_download):
        """Test that invalid region lines are skipped."""
        tsv_content = (
            "INVALID\tName\tAscii\t12345\n"  # No dot in code
            "US.CA\tCalifornia\tCalifornia\t5332921\n"
        )
        mock_download.return_value = tsv_content.encode("utf-8")

        result = parse_region_data()

        assert len(result) == 1


class TestParseCityData:
    """Tests for parse_city_data function."""

    @patch("geobank.parsers.download_with_retry")
    def test_parse_city_data_success(self, mock_download):
        """Test successful parsing of city data from zip."""
        # Create a mock zip file with city data
        city_content = (
            "5128581\tNew York City\tNew York City\tNYC,New York\t40.71427\t-74.00597\tP\tPPLA2\tUS\t\tNY\t061\t\t\t8336817\t\t10\tAmerica/New_York\t2019-09-05\n"
            "5368361\tLos Angeles\tLos Angeles\tLA\t34.05223\t-118.24368\tP\tPPLA2\tUS\t\tCA\t037\t\t\t3979576\t\t93\tAmerica/Los_Angeles\t2021-01-01\n"
        )

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("cities15000.txt", city_content)
        mock_download.return_value = zip_buffer.getvalue()

        result = parse_city_data(population_gte=15000)

        assert len(result) == 2

        nyc = result[0]
        assert nyc["geoname_id"] == 5128581
        assert nyc["name"] == "New York City"
        assert nyc["name_ascii"] == "New York City"
        assert nyc["country_code"] == "US"
        assert nyc["region_code"] == "NY"
        assert nyc["population"] == 8336817
        assert nyc["timezone"] == "America/New_York"


class TestParseLanguagesData:
    """Tests for parse_languages_data function."""

    @patch("geobank.parsers.download_with_retry")
    def test_parse_languages_data_success(self, mock_download):
        """Test successful parsing of language data."""
        api_response = [
            {"languages": {"eng": "English", "spa": "Spanish"}},
            {"languages": {"fra": "French", "eng": "English"}},
        ]
        mock_download.return_value = json.dumps(api_response).encode("utf-8")

        result = parse_languages_data()

        assert len(result) == 3
        assert result["eng"] == "English"
        assert result["spa"] == "Spanish"
        assert result["fra"] == "French"

    @patch("geobank.parsers.download_with_retry")
    def test_parse_languages_data_filters_invalid_codes(self, mock_download):
        """Test that invalid language codes are filtered."""
        api_response = [
            {
                "languages": {"eng": "English", "en": "English Short"}
            },  # 'en' is 2-letter, should be skipped
        ]
        mock_download.return_value = json.dumps(api_response).encode("utf-8")

        result = parse_languages_data()

        assert "eng" in result
        assert "en" not in result


class TestParseCurrenciesData:
    """Tests for parse_currencies_data function."""

    @patch("geobank.parsers.download_with_retry")
    def test_parse_currencies_data_success(self, mock_download):
        """Test successful parsing of currency data."""
        api_response = [
            {"currencies": {"USD": {"name": "United States dollar", "symbol": "$"}}},
            {"currencies": {"EUR": {"name": "Euro", "symbol": "€"}}},
        ]
        mock_download.return_value = json.dumps(api_response).encode("utf-8")

        result = parse_currencies_data()

        assert len(result) == 2
        assert result["USD"]["name"] == "United States dollar"
        assert result["USD"]["symbol"] == "$"
        assert result["EUR"]["name"] == "Euro"


class TestParseFlagsData:
    """Tests for parse_flags_data function."""

    @patch("geobank.parsers.download_with_retry")
    def test_parse_flags_data_success(self, mock_download):
        """Test successful parsing of flag data."""
        api_response = [
            {
                "cca2": "US",
                "flags": {"png": "https://example.com/us.png", "svg": "https://example.com/us.svg"},
            },
            {
                "cca2": "CA",
                "flags": {"png": "https://example.com/ca.png", "svg": "https://example.com/ca.svg"},
            },
        ]
        mock_download.return_value = json.dumps(api_response).encode("utf-8")

        result = parse_flags_data()

        assert len(result) == 2
        assert result["US"]["png"] == "https://example.com/us.png"
        assert result["CA"]["svg"] == "https://example.com/ca.svg"
