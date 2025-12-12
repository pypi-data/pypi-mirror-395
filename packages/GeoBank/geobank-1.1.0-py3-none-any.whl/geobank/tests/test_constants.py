"""
Tests for the constants module.
"""

from geobank.constants import ISO_639_1_TO_2, ISO_639_2_TO_1


class TestISOLanguageCodeMappings:
    """Tests for ISO language code mappings."""

    def test_iso_639_1_to_2_has_common_languages(self):
        """Test that common language codes are present."""
        # Check some common languages
        assert ISO_639_1_TO_2["en"] == "eng"
        assert ISO_639_1_TO_2["es"] == "spa"
        assert ISO_639_1_TO_2["fr"] == "fra"
        assert ISO_639_1_TO_2["de"] == "deu"
        assert ISO_639_1_TO_2["zh"] == "zho"
        assert ISO_639_1_TO_2["ar"] == "ara"
        assert ISO_639_1_TO_2["ru"] == "rus"
        assert ISO_639_1_TO_2["ja"] == "jpn"
        assert ISO_639_1_TO_2["pt"] == "por"
        assert ISO_639_1_TO_2["it"] == "ita"

    def test_iso_639_2_to_1_is_reverse_mapping(self):
        """Test that ISO_639_2_TO_1 is correct reverse of ISO_639_1_TO_2."""
        for code_1, code_2 in ISO_639_1_TO_2.items():
            assert ISO_639_2_TO_1[code_2] == code_1

    def test_iso_639_2_to_1_has_common_languages(self):
        """Test that common 3-letter codes map correctly."""
        assert ISO_639_2_TO_1["eng"] == "en"
        assert ISO_639_2_TO_1["spa"] == "es"
        assert ISO_639_2_TO_1["fra"] == "fr"
        assert ISO_639_2_TO_1["deu"] == "de"

    def test_mappings_have_same_length(self):
        """Test that both mappings have the same number of entries."""
        assert len(ISO_639_1_TO_2) == len(ISO_639_2_TO_1)

    def test_all_codes_are_correct_length(self):
        """Test that all codes have correct lengths."""
        for code_1, code_2 in ISO_639_1_TO_2.items():
            assert len(code_1) == 2, f"2-letter code '{code_1}' has wrong length"
            assert len(code_2) == 3, f"3-letter code '{code_2}' has wrong length"
