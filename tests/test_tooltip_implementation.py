#!/usr/bin/env python
"""
Comprehensive Test Script for KPI Tooltip Implementation
Tests the fixed tooltip implementation to ensure it works correctly.
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from components import create_card, create_metric_box, create_metric_with_description, create_tooltip
from translations import TRANSLATIONS, get_text
from dash import html


def test_tooltip_component():
    """Test 1: Verify tooltip component structure and styling"""
    print("=" * 80)
    print("TEST 1: Tooltip Component Structure")
    print("=" * 80)

    tooltip = create_tooltip(
        "test-tooltip",
        "This is a test tooltip with **bold** and *italic* text.",
        "Test Title"
    )

    # Check it returns html.Span
    assert isinstance(tooltip, html.Span), "Tooltip should be an html.Span component"

    # Check it has the correct ID
    assert tooltip.id == "test-tooltip", f"Expected ID 'test-tooltip', got '{tooltip.id}'"

    # Check it has the title attribute (stripped of markdown)
    expected_title = "This is a test tooltip with bold and italic text."
    assert tooltip.title == expected_title, f"Title attribute not stripped correctly"

    # Check styling
    assert "cursor" in tooltip.style, "Missing cursor style"
    assert tooltip.style["cursor"] == "help", "Cursor should be 'help'"
    assert "borderBottom" in tooltip.style, "Missing borderBottom style"
    assert "dotted" in tooltip.style["borderBottom"], "Border should be dotted"

    # Check children (text content)
    assert tooltip.children == "Test Title", "Text content should match input"

    print("✓ Tooltip component structure is correct")
    print(f"  - Returns html.Span: ✓")
    print(f"  - Has correct ID: ✓")
    print(f"  - Title attribute stripped of markdown: ✓")
    print(f"  - Has cursor:help style: ✓")
    print(f"  - Has dotted border: ✓")
    print(f"  - Contains correct text: ✓")
    print()


def test_no_info_icons():
    """Test 2: Verify no ℹ️ icons are present"""
    print("=" * 80)
    print("TEST 2: No Info Icons Present")
    print("=" * 80)

    # Test create_card
    card = create_card(
        "Test KPI",
        "€1,000",
        "#2E86AB",
        tooltip_text="Test tooltip",
        tooltip_id="test-card-tooltip"
    )

    # Convert to string and check for info icon
    card_str = str(card)
    assert "ℹ️" not in card_str, "Found ℹ️ icon in create_card output!"
    assert "ℹ" not in card_str, "Found info icon unicode in create_card output!"

    # Test create_metric_box
    metric_box = create_metric_box(
        "Test Metrics",
        {"KPI 1": "€500", "KPI 2": "€1000"},
        tooltips={
            "KPI 1": ("Tooltip for KPI 1", "tooltip-kpi1"),
            "KPI 2": ("Tooltip for KPI 2", "tooltip-kpi2"),
        }
    )

    metric_box_str = str(metric_box)
    assert "ℹ️" not in metric_box_str, "Found ℹ️ icon in create_metric_box output!"
    assert "ℹ" not in metric_box_str, "Found info icon unicode in create_metric_box output!"

    # Test create_metric_with_description
    metric_desc = create_metric_with_description(
        "Test Metric",
        "€2,000",
        "This is a description",
        tooltip_text="Test tooltip",
        tooltip_id="test-metric-desc-tooltip"
    )

    metric_desc_str = str(metric_desc)
    assert "ℹ️" not in metric_desc_str, "Found ℹ️ icon in create_metric_with_description output!"
    assert "ℹ" not in metric_desc_str, "Found info icon unicode in create_metric_with_description output!"

    print("✓ No info icons found in any component")
    print(f"  - create_card: ✓")
    print(f"  - create_metric_box: ✓")
    print(f"  - create_metric_with_description: ✓")
    print()


def test_visual_indicators():
    """Test 3: Verify tooltips have proper visual indicators"""
    print("=" * 80)
    print("TEST 3: Visual Indicators Present")
    print("=" * 80)

    tooltip = create_tooltip(
        "visual-test",
        "Test tooltip",
        "Hover Me"
    )

    # Check for cursor:help
    assert tooltip.style.get("cursor") == "help", "Missing cursor:help style"

    # Check for underline/border indicator
    border = tooltip.style.get("borderBottom", "")
    assert "dotted" in border, f"Expected dotted border, got: {border}"
    assert "currentColor" in border, "Border should use currentColor"

    # Verify no text decoration that would interfere
    assert tooltip.style.get("textDecoration") == "none", "Should not have text-decoration"

    print("✓ Visual indicators are correctly applied")
    print(f"  - cursor: help ✓")
    print(f"  - borderBottom: 1px dotted currentColor ✓")
    print(f"  - textDecoration: none ✓")
    print()


def test_all_kpi_tooltips_exist():
    """Test 4: Verify all KPIs have tooltips in both languages"""
    print("=" * 80)
    print("TEST 4: All KPI Tooltips Exist")
    print("=" * 80)

    kpis = [
        # Overview cards (7 KPIs)
        "loan_amount",
        "monthly_rate",
        "total_interest",
        "total_payoff_years",
        "remaining_debt",
        "rate_of_income",
        "breakeven_milestone",
        # Key Metrics boxes (15 KPIs)
        "purchase_price",
        "equity",
        "interest_rate",
        "annual_rate",
        "total_amortization",
        "total_paid",
        "interest_costs",
        "total_cost_of_ownership",
        "ltv_ratio",
        "interest_to_principal_ratio",
        "interest_without_special",
        "interest_with_special",
        "interest_savings",
        "time_saved",
        # Risk Analysis (3 KPIs)
        "buffer_ratio",
        "time_to_50_equity",
        "rate_sensitivity_score",
        # Affordability (6 KPIs)
        "household_income",
        "affordable_monthly_payment",
        "housing_expense_ratio",
        "housing_expense_benchmark",
        "years_to_payoff",
    ]

    missing_en = []
    missing_de = []

    for kpi in kpis:
        tooltip_key = f"tooltip_{kpi}"

        if tooltip_key not in TRANSLATIONS["en"]:
            missing_en.append(kpi)
        if tooltip_key not in TRANSLATIONS["de"]:
            missing_de.append(kpi)

    if missing_en:
        print(f"✗ Missing English tooltips for: {', '.join(missing_en)}")
    else:
        print(f"✓ All {len(kpis)} KPIs have English tooltips")

    if missing_de:
        print(f"✗ Missing German tooltips for: {', '.join(missing_de)}")
    else:
        print(f"✓ All {len(kpis)} KPIs have German tooltips")

    assert not missing_en, f"Missing English tooltips: {missing_en}"
    assert not missing_de, f"Missing German tooltips: {missing_de}"
    print()


def test_tooltip_content_quality():
    """Test 5: Verify tooltip content is comprehensive"""
    print("=" * 80)
    print("TEST 5: Tooltip Content Quality")
    print("=" * 80)

    # Test a few key tooltips for quality
    tooltips_to_check = [
        "tooltip_total_cost_of_ownership",
        "tooltip_ltv_ratio",
        "tooltip_buffer_ratio",
        "tooltip_rate_sensitivity_score",
    ]

    min_length = 100  # Comprehensive tooltips should be substantial

    for tooltip_key in tooltips_to_check:
        en_text = TRANSLATIONS["en"].get(tooltip_key, "")
        de_text = TRANSLATIONS["de"].get(tooltip_key, "")

        # Check length
        assert len(en_text) >= min_length, \
            f"{tooltip_key} English text too short: {len(en_text)} chars"
        assert len(de_text) >= min_length, \
            f"{tooltip_key} German text too short: {len(de_text)} chars"

        # Check for calculation/formula info
        has_calc = any(word in en_text.lower() for word in [
            "calculation:", "formula:", "calculated", "="
        ])

        # Check for significance/interpretation
        has_significance = any(word in en_text.lower() for word in [
            "significance:", "important", "shows", "indicates", "good", "better"
        ])

        assert has_calc or has_significance, \
            f"{tooltip_key} lacks calculation or significance explanation"

        print(f"✓ {tooltip_key}")
        print(f"  - English: {len(en_text)} chars")
        print(f"  - German: {len(de_text)} chars")
        print(f"  - Has calculation info: {has_calc}")
        print(f"  - Has significance info: {has_significance}")

    print()


def test_bilingual_support():
    """Test 6: Verify tooltips work in both English and German"""
    print("=" * 80)
    print("TEST 6: Bilingual Support")
    print("=" * 80)

    # Test get_text function
    test_key = "tooltip_ltv_ratio"

    en_text = get_text("en", test_key)
    de_text = get_text("de", test_key)

    assert en_text != de_text, "English and German tooltips should be different"
    assert "Loan-to-Value" in en_text, "English tooltip should contain English terms"
    assert "Beleihungsauslauf" in de_text or "LTV" in de_text, \
        "German tooltip should contain German terms"

    # Verify sentence count is similar
    en_sentences = en_text.count(".") + en_text.count("!") + en_text.count("?")
    de_sentences = de_text.count(".") + de_text.count("!") + de_text.count("?")

    assert abs(en_sentences - de_sentences) <= 1, \
        f"Sentence count differs too much: EN={en_sentences}, DE={de_sentences}"

    print(f"✓ Bilingual support working correctly")
    print(f"  - English and German texts are different: ✓")
    print(f"  - English contains English terms: ✓")
    print(f"  - German contains German terms: ✓")
    print(f"  - Sentence counts similar (EN:{en_sentences}, DE:{de_sentences}): ✓")
    print()


def test_html_structure():
    """Test 7: Verify HTML structure is correct"""
    print("=" * 80)
    print("TEST 7: HTML Structure")
    print("=" * 80)

    # Test that create_card integrates tooltip correctly
    card = create_card(
        "Total Cost",
        "€500,000",
        "#2E86AB",
        tooltip_text="The complete cost including all interest",
        tooltip_id="test-html-structure"
    )

    # The card should have an H3 with a Span child (the tooltip)
    h3 = card.children[0]
    assert isinstance(h3, html.H3), "First child should be H3"

    # The H3's child should be the tooltip Span
    tooltip_span = h3.children
    assert isinstance(tooltip_span, html.Span), "H3 child should be tooltip Span"
    assert tooltip_span.id == "test-html-structure", "Tooltip should have correct ID"
    assert tooltip_span.children == "Total Cost", "Tooltip should contain title text"

    print(f"✓ HTML structure is correct")
    print(f"  - Card contains H3: ✓")
    print(f"  - H3 contains tooltip Span: ✓")
    print(f"  - Tooltip Span has correct ID: ✓")
    print(f"  - Tooltip Span contains title text: ✓")
    print()


def generate_test_report():
    """Generate a comprehensive test report"""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE TOOLTIP IMPLEMENTATION TEST REPORT")
    print("=" * 80)
    print()

    try:
        test_tooltip_component()
        test_no_info_icons()
        test_visual_indicators()
        test_all_kpi_tooltips_exist()
        test_tooltip_content_quality()
        test_bilingual_support()
        test_html_structure()

        print("=" * 80)
        print("ALL TESTS PASSED ✓")
        print("=" * 80)
        print()
        print("SUMMARY:")
        print("  ✓ Tooltip component structure is correct")
        print("  ✓ No ℹ️ icons present anywhere")
        print("  ✓ Visual indicators (cursor, underline) working")
        print("  ✓ All KPIs have tooltips in both languages")
        print("  ✓ Tooltip content is comprehensive and high-quality")
        print("  ✓ Bilingual support working correctly")
        print("  ✓ HTML structure is correct")
        print()
        print("ISSUES FOUND: None")
        print()
        return True

    except AssertionError as e:
        print()
        print("=" * 80)
        print("TEST FAILED ✗")
        print("=" * 80)
        print(f"Error: {e}")
        print()
        return False


if __name__ == "__main__":
    success = generate_test_report()
    sys.exit(0 if success else 1)
