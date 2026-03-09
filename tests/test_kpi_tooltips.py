"""
Comprehensive Tests for KPI Tooltip Functionality
Tests tooltip existence, bilingual support, content structure, and UI integration
"""

import pytest
import sys
from pathlib import Path

# Add app directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from translations import TRANSLATIONS, get_text


class TestTooltipExistence:
    """Test that all KPIs have corresponding tooltips in translations"""

    # Define all KPIs that should have tooltips
    KPI_KEYS = [
        # High-priority KPIs
        "total_cost_of_ownership",
        "interest_to_principal_ratio",
        "ltv_ratio",
        "interest_savings",
        # Medium-priority KPIs
        "breakeven_year",
        "equity_buildup",
        "housing_expense_ratio",
        # Low-priority KPIs
        "buffer_ratio",
        "time_to_50_equity",
        "rate_sensitivity_score",
    ]

    @pytest.mark.parametrize("kpi_key", KPI_KEYS)
    def test_english_tooltip_exists(self, kpi_key):
        """Verify each KPI has an English tooltip"""
        tooltip_key = f"{kpi_key}_tooltip"
        assert (
            tooltip_key in TRANSLATIONS["en"]
        ), f"Missing English tooltip for {kpi_key}"

    @pytest.mark.parametrize("kpi_key", KPI_KEYS)
    def test_german_tooltip_exists(self, kpi_key):
        """Verify each KPI has a German tooltip"""
        tooltip_key = f"{kpi_key}_tooltip"
        assert (
            tooltip_key in TRANSLATIONS["de"]
        ), f"Missing German tooltip for {kpi_key}"

    def test_all_tooltips_have_pairs(self):
        """Ensure every English tooltip has a corresponding German tooltip"""
        en_tooltips = {
            key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")
        }
        de_tooltips = {
            key for key in TRANSLATIONS["de"].keys() if key.endswith("_tooltip")
        }

        # Check both sets are equal
        assert (
            en_tooltips == de_tooltips
        ), f"Tooltip mismatch: EN has {en_tooltips - de_tooltips}, DE has {de_tooltips - en_tooltips}"


class TestTooltipCompleteness:
    """Test that tooltips are complete and not empty or missing keys"""

    @pytest.fixture
    def all_tooltip_keys(self):
        """Get all tooltip keys from English translations"""
        return [key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")]

    def test_no_empty_tooltips_english(self, all_tooltip_keys):
        """Verify no English tooltips are empty strings"""
        for key in all_tooltip_keys:
            tooltip_text = TRANSLATIONS["en"][key]
            assert (
                tooltip_text and len(tooltip_text.strip()) > 0
            ), f"English tooltip '{key}' is empty"

    def test_no_empty_tooltips_german(self, all_tooltip_keys):
        """Verify no German tooltips are empty strings"""
        for key in all_tooltip_keys:
            tooltip_text = TRANSLATIONS["de"][key]
            assert (
                tooltip_text and len(tooltip_text.strip()) > 0
            ), f"German tooltip '{key}' is empty"

    def test_tooltips_are_different_languages(self, all_tooltip_keys):
        """Ensure English and German tooltips are actually different (not copy-pasted)"""
        # Skip if no tooltips exist yet
        if not all_tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in all_tooltip_keys:
            en_text = TRANSLATIONS["en"][key]
            de_text = TRANSLATIONS["de"][key]

            # Allow for some common technical terms, but texts should differ
            assert (
                en_text != de_text
            ), f"Tooltip '{key}' is identical in EN and DE (likely not translated)"


class TestTooltipStructure:
    """Test that tooltips contain required structural elements"""

    # Define expected structure components for comprehensive tooltips
    EXPECTED_COMPONENTS = {
        "description": [
            # Keywords that suggest a description
            ".",  # Should have at least one sentence
        ],
        "formula": [
            # Mathematical/formula indicators
            "=",
            "×",
            "*",
            "/",
            "%",
            "÷",
            "(",
            "Formula:",
            "Calculation:",
            "Calculated as:",
        ],
        "significance": [
            # Keywords about importance/meaning
            "important",
            "indicates",
            "shows",
            "means",
            "helps",
            "critical",
            "useful",
            "good",
            "bad",
            "high",
            "low",
            "optimal",
            "target",
            "benchmark",
            "should",
            "ideal",
            "typical",
        ],
    }

    @pytest.fixture
    def all_tooltip_keys(self):
        """Get all tooltip keys from English translations"""
        return [key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")]

    def test_tooltips_have_sufficient_length(self, all_tooltip_keys):
        """Verify tooltips are comprehensive (not just single words)"""
        # Skip if no tooltips exist yet
        if not all_tooltip_keys:
            pytest.skip("No tooltips defined yet")

        min_length = 20  # Minimum characters for a useful tooltip
        for key in all_tooltip_keys:
            en_tooltip = TRANSLATIONS["en"][key]
            de_tooltip = TRANSLATIONS["de"][key]

            assert (
                len(en_tooltip) >= min_length
            ), f"English tooltip '{key}' too short ({len(en_tooltip)} chars)"
            assert (
                len(de_tooltip) >= min_length
            ), f"German tooltip '{key}' too short ({len(de_tooltip)} chars)"

    def test_tooltips_contain_formula_or_explanation(self, all_tooltip_keys):
        """Verify tooltips contain calculation formula or clear explanation"""
        # Skip if no tooltips exist yet
        if not all_tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in all_tooltip_keys:
            en_tooltip = TRANSLATIONS["en"][key]

            # Check if tooltip contains any formula indicators
            has_formula = any(
                indicator in en_tooltip
                for indicator in self.EXPECTED_COMPONENTS["formula"]
            )

            # Or contains clear explanation keywords
            has_explanation = any(
                keyword.lower() in en_tooltip.lower()
                for keyword in self.EXPECTED_COMPONENTS["significance"]
            )

            assert (
                has_formula or has_explanation
            ), f"Tooltip '{key}' lacks both formula and clear explanation"

    def test_tooltips_have_multiple_sentences(self, all_tooltip_keys):
        """Verify comprehensive tooltips have multiple sentences"""
        # Skip if no tooltips exist yet
        if not all_tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in all_tooltip_keys:
            en_tooltip = TRANSLATIONS["en"][key]

            # Count sentence-ending punctuation
            sentence_count = (
                en_tooltip.count(".")
                + en_tooltip.count("!")
                + en_tooltip.count("?")
            )

            # Should have at least 2 sentences for comprehensive info
            assert (
                sentence_count >= 2
            ), f"Tooltip '{key}' should have multiple sentences (found {sentence_count})"


class TestTooltipNamingConsistency:
    """Test that tooltip naming conventions are consistent"""

    def test_tooltip_keys_follow_naming_convention(self):
        """Verify all tooltip keys follow the pattern: {kpi_name}_tooltip"""
        all_en_keys = TRANSLATIONS["en"].keys()
        tooltip_keys = [key for key in all_en_keys if key.endswith("_tooltip")]

        # Skip if no tooltips exist yet
        if not tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in tooltip_keys:
            # Should end with _tooltip
            assert key.endswith(
                "_tooltip"
            ), f"Tooltip key '{key}' doesn't follow naming convention"

            # Should have corresponding base key (without _tooltip)
            base_key = key.replace("_tooltip", "")

            # Note: Not all tooltips need a base key (e.g., complex explanations)
            # but we check if base exists, it should be valid
            if base_key in TRANSLATIONS["en"]:
                assert isinstance(
                    TRANSLATIONS["en"][base_key], str
                ), f"Base key '{base_key}' is not a string"

    def test_no_duplicate_tooltip_content(self):
        """Ensure tooltips don't have duplicate content (copy-paste errors)"""
        en_tooltips = {
            key: value
            for key, value in TRANSLATIONS["en"].items()
            if key.endswith("_tooltip")
        }

        # Skip if no tooltips exist yet
        if not en_tooltips:
            pytest.skip("No tooltips defined yet")

        # Check for duplicate values
        seen_values = {}
        for key, value in en_tooltips.items():
            if value in seen_values:
                pytest.fail(
                    f"Duplicate tooltip content found: '{key}' and '{seen_values[value]}' have identical text"
                )
            seen_values[value] = key


class TestTooltipContentQuality:
    """Test the quality and usefulness of tooltip content"""

    @pytest.fixture
    def high_priority_kpis(self):
        """KPIs that must have high-quality, detailed tooltips"""
        return [
            "total_cost_of_ownership",
            "interest_to_principal_ratio",
            "ltv_ratio",
            "interest_savings",
        ]

    def test_high_priority_tooltips_are_comprehensive(self, high_priority_kpis):
        """Verify high-priority KPIs have detailed, comprehensive tooltips"""
        min_length = 100  # High-priority tooltips should be substantial

        for kpi in high_priority_kpis:
            tooltip_key = f"{kpi}_tooltip"

            # Skip if tooltip doesn't exist yet
            if tooltip_key not in TRANSLATIONS["en"]:
                pytest.skip(f"Tooltip {tooltip_key} not defined yet")

            en_tooltip = TRANSLATIONS["en"][tooltip_key]

            assert (
                len(en_tooltip) >= min_length
            ), f"High-priority tooltip '{tooltip_key}' should be at least {min_length} chars (found {len(en_tooltip)})"

    def test_tooltips_provide_actionable_insights(self):
        """Verify tooltips include actionable insights or benchmarks"""
        actionable_keywords = [
            "should",
            "target",
            "ideal",
            "optimal",
            "good",
            "acceptable",
            "benchmark",
            "typical",
            "recommended",
            "aim for",
            "below",
            "above",
            "better",
            "worse",
            "higher",
            "lower",
        ]

        tooltip_keys = [
            key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")
        ]

        # Skip if no tooltips exist yet
        if not tooltip_keys:
            pytest.skip("No tooltips defined yet")

        # At least some tooltips should provide actionable insights
        tooltips_with_insights = 0

        for key in tooltip_keys:
            en_tooltip = TRANSLATIONS["en"][key].lower()

            if any(keyword in en_tooltip for keyword in actionable_keywords):
                tooltips_with_insights += 1

        # At least 50% of tooltips should provide actionable insights
        min_required = len(tooltip_keys) // 2
        assert (
            tooltips_with_insights >= min_required
        ), f"Only {tooltips_with_insights}/{len(tooltip_keys)} tooltips provide actionable insights (expected at least {min_required})"


class TestTooltipUIIntegration:
    """Test tooltip integration with UI components (conceptual tests)"""

    def test_tooltip_keys_match_kpi_display_keys(self):
        """Ensure tooltip keys align with KPI display keys in translations"""
        # Get all KPI-related keys (non-tooltip)
        kpi_keys = [
            "total_cost_of_ownership",
            "interest_to_principal_ratio",
            "ltv_ratio",
            "buffer_ratio",
            "time_to_50_equity",
            "rate_sensitivity_score",
            "breakeven_year",
            "equity_buildup",
            "housing_expense_ratio",
        ]

        for kpi_key in kpi_keys:
            # Check if base key exists in translations
            if kpi_key in TRANSLATIONS["en"]:
                # If base exists, tooltip should exist
                tooltip_key = f"{kpi_key}_tooltip"
                assert (
                    tooltip_key in TRANSLATIONS["en"]
                ), f"KPI '{kpi_key}' exists but missing tooltip '{tooltip_key}'"

    def test_tooltip_format_for_html_rendering(self):
        """Verify tooltips don't contain problematic characters for HTML rendering"""
        problematic_chars = ["<script>", "</script>", "<iframe>", "javascript:"]

        tooltip_keys = [
            key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")
        ]

        # Skip if no tooltips exist yet
        if not tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in tooltip_keys:
            en_tooltip = TRANSLATIONS["en"][key]
            de_tooltip = TRANSLATIONS["de"][key]

            for char in problematic_chars:
                assert (
                    char.lower() not in en_tooltip.lower()
                ), f"Tooltip '{key}' contains problematic HTML: {char}"
                assert (
                    char.lower() not in de_tooltip.lower()
                ), f"Tooltip '{key}' contains problematic HTML: {char}"


class TestTooltipAccessibility:
    """Test tooltip accessibility features"""

    def test_tooltips_use_plain_language(self):
        """Verify tooltips avoid overly technical jargon"""
        # Technical jargon that should be explained if used
        technical_terms = [
            "amortization",
            "principal",
            "LTV",
            "equity",
            "refinancing",
        ]

        tooltip_keys = [
            key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")
        ]

        # Skip if no tooltips exist yet
        if not tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in tooltip_keys:
            en_tooltip = TRANSLATIONS["en"][key].lower()

            # If technical term is used, tooltip should provide explanation
            for term in technical_terms:
                if term.lower() in en_tooltip:
                    # Should have some explanatory text around it
                    # This is a heuristic: check tooltip is long enough to include explanation
                    assert (
                        len(en_tooltip) > 50
                    ), f"Tooltip '{key}' uses technical term '{term}' but seems too short to explain it"

    def test_tooltips_are_screen_reader_friendly(self):
        """Verify tooltips don't use special characters that confuse screen readers"""
        # Characters that might cause issues with screen readers
        # We allow mathematical symbols but they should be used appropriately
        tooltip_keys = [
            key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")
        ]

        # Skip if no tooltips exist yet
        if not tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in tooltip_keys:
            en_tooltip = TRANSLATIONS["en"][key]

            # Should not start or end with special characters
            assert en_tooltip[0].isalnum() or en_tooltip[
                0
            ] in "\"'", f"Tooltip '{key}' starts with problematic character"
            # Should end with proper punctuation
            assert en_tooltip[-1] in ".!?", f"Tooltip '{key}' should end with punctuation"


class TestTooltipSpecificKPIs:
    """Test tooltips for specific critical KPIs"""

    def test_ltv_ratio_tooltip_mentions_percentage(self):
        """LTV ratio tooltip should explain it's a percentage"""
        tooltip_key = "ltv_ratio_tooltip"

        # Skip if tooltip doesn't exist yet
        if tooltip_key not in TRANSLATIONS["en"]:
            pytest.skip(f"Tooltip {tooltip_key} not defined yet")

        en_tooltip = TRANSLATIONS["en"][tooltip_key].lower()

        # Should mention percentage or %
        assert "%" in TRANSLATIONS["en"][tooltip_key] or "percent" in en_tooltip, \
            "LTV tooltip should mention it's expressed as a percentage"

    def test_buffer_ratio_tooltip_mentions_months(self):
        """Buffer ratio tooltip should explain months of emergency fund"""
        tooltip_key = "buffer_ratio_tooltip"

        # Skip if tooltip doesn't exist yet
        if tooltip_key not in TRANSLATIONS["en"]:
            pytest.skip(f"Tooltip {tooltip_key} not defined yet")

        en_tooltip = TRANSLATIONS["en"][tooltip_key].lower()

        # Should mention months
        assert "month" in en_tooltip, \
            "Buffer ratio tooltip should mention months"

    def test_interest_to_principal_ratio_tooltip_explains_interpretation(self):
        """Interest-to-principal ratio tooltip should explain what high/low means"""
        tooltip_key = "interest_to_principal_ratio_tooltip"

        # Skip if tooltip doesn't exist yet
        if tooltip_key not in TRANSLATIONS["en"]:
            pytest.skip(f"Tooltip {tooltip_key} not defined yet")

        en_tooltip = TRANSLATIONS["en"][tooltip_key].lower()

        # Should provide interpretation guidance
        interpretation_keywords = ["high", "low", "good", "better", "worse", "ratio"]
        assert any(
            keyword in en_tooltip for keyword in interpretation_keywords
        ), "Interest-to-principal tooltip should explain interpretation"

    def test_rate_sensitivity_tooltip_mentions_risk(self):
        """Rate sensitivity tooltip should mention refinancing risk"""
        tooltip_key = "rate_sensitivity_score_tooltip"

        # Skip if tooltip doesn't exist yet
        if tooltip_key not in TRANSLATIONS["en"]:
            pytest.skip(f"Tooltip {tooltip_key} not defined yet")

        en_tooltip = TRANSLATIONS["en"][tooltip_key].lower()

        # Should mention risk or refinancing
        risk_keywords = ["risk", "refinanc", "binding", "period", "critical"]
        assert any(
            keyword in en_tooltip for keyword in risk_keywords
        ), "Rate sensitivity tooltip should mention refinancing risk"


class TestTooltipBilingualConsistency:
    """Test that English and German tooltips convey the same information"""

    def test_tooltip_sentence_count_similar_across_languages(self):
        """Verify EN and DE tooltips have similar sentence counts (content parity)"""
        tooltip_keys = [
            key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")
        ]

        # Skip if no tooltips exist yet
        if not tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in tooltip_keys:
            en_tooltip = TRANSLATIONS["en"][key]
            de_tooltip = TRANSLATIONS["de"][key]

            en_sentences = en_tooltip.count(".") + en_tooltip.count("!") + en_tooltip.count("?")
            de_sentences = de_tooltip.count(".") + de_tooltip.count("!") + de_tooltip.count("?")

            # Sentence counts should be within 1 of each other (accounting for language differences)
            assert (
                abs(en_sentences - de_sentences) <= 1
            ), f"Tooltip '{key}' has different sentence counts (EN: {en_sentences}, DE: {de_sentences})"

    def test_tooltip_length_ratio_reasonable(self):
        """Verify EN and DE tooltip lengths are reasonably similar"""
        tooltip_keys = [
            key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")
        ]

        # Skip if no tooltips exist yet
        if not tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in tooltip_keys:
            en_tooltip = TRANSLATIONS["en"][key]
            de_tooltip = TRANSLATIONS["de"][key]

            # German is typically 10-30% longer than English
            # Ratio should be between 0.7 and 1.5
            if len(en_tooltip) > 0:
                ratio = len(de_tooltip) / len(en_tooltip)
                assert (
                    0.6 <= ratio <= 1.6
                ), f"Tooltip '{key}' has unusual length ratio (EN: {len(en_tooltip)}, DE: {len(de_tooltip)}, ratio: {ratio:.2f})"


class TestTooltipIntegrationWithGetText:
    """Test tooltip retrieval using get_text function"""

    def test_get_text_retrieves_tooltips_correctly(self):
        """Verify get_text function works for tooltip keys"""
        tooltip_keys = [
            key for key in TRANSLATIONS["en"].keys() if key.endswith("_tooltip")
        ]

        # Skip if no tooltips exist yet
        if not tooltip_keys:
            pytest.skip("No tooltips defined yet")

        for key in tooltip_keys:
            # Test English
            en_result = get_text("en", key)
            assert en_result == TRANSLATIONS["en"][key], \
                f"get_text returned wrong value for EN '{key}'"

            # Test German
            de_result = get_text("de", key)
            assert de_result == TRANSLATIONS["de"][key], \
                f"get_text returned wrong value for DE '{key}'"

    def test_get_text_fallback_for_missing_tooltips(self):
        """Verify get_text handles missing tooltip keys gracefully"""
        fake_tooltip_key = "nonexistent_kpi_tooltip"

        # Should fall back to returning the key itself
        result = get_text("en", fake_tooltip_key)
        assert result == fake_tooltip_key, \
            "get_text should return key when tooltip doesn't exist"


# Pytest configuration for running these tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
