"""
Test that the header (app title and subtitle) can be translated correctly
"""

import pytest
from translations import get_text


class TestHeaderTranslations:
    """Test header translation functionality"""

    def test_app_title_english(self):
        """Test that English app title is correct"""
        title = get_text("en", "app_title")
        assert title == "Financing Calculator"
        assert len(title) > 0

    def test_app_title_german(self):
        """Test that German app title is correct"""
        title = get_text("de", "app_title")
        assert title == "Baufinanzierung Rechner"
        assert len(title) > 0

    def test_app_subtitle_english(self):
        """Test that English app subtitle is correct"""
        subtitle = get_text("en", "app_subtitle")
        assert subtitle == "Interactive analysis of property financing with detailed interest curve diagrams"
        assert len(subtitle) > 0
        assert "financing" in subtitle.lower()

    def test_app_subtitle_german(self):
        """Test that German app subtitle is correct"""
        subtitle = get_text("de", "app_subtitle")
        assert subtitle == "Interaktive Analyse von Immobilienfinanzierungen mit detaillierten Zinsverlauf-Diagrammen"
        assert len(subtitle) > 0
        assert "finanzierung" in subtitle.lower() or "analyse" in subtitle.lower()

    def test_app_title_and_subtitle_exist_in_both_languages(self):
        """Test that both title and subtitle exist in both languages"""
        for lang in ["en", "de"]:
            title = get_text(lang, "app_title")
            subtitle = get_text(lang, "app_subtitle")

            assert title is not None
            assert subtitle is not None
            assert len(title) > 0
            assert len(subtitle) > 0

    def test_app_title_different_across_languages(self):
        """Test that title is different in English and German"""
        en_title = get_text("en", "app_title")
        de_title = get_text("de", "app_title")

        assert en_title != de_title

    def test_app_subtitle_different_across_languages(self):
        """Test that subtitle is different in English and German"""
        en_subtitle = get_text("en", "app_subtitle")
        de_subtitle = get_text("de", "app_subtitle")

        assert en_subtitle != de_subtitle

    def test_language_label_translation(self):
        """Test that language label exists in both languages"""
        en_label = get_text("en", "language")
        de_label = get_text("de", "language")

        assert en_label == "Language"
        assert de_label == "Sprache"
