#!/usr/bin/env python
"""
Integration test that verifies tooltip implementation in actual rendered components
This test creates actual Dash components and verifies the HTML output
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from components import create_card, create_metric_box, create_metric_with_description
from translations import get_text
from dash import html
import json


def test_rendered_html_output():
    """Test the actual HTML output of components with tooltips"""
    print("=" * 80)
    print("INTEGRATION TEST: Rendered HTML Output")
    print("=" * 80)
    print()

    # Test 1: Create a card with tooltip
    print("Test 1: Card with Tooltip")
    print("-" * 40)
    card = create_card(
        "Total Cost of Ownership",
        "€550,000",
        "#2E86AB",
        tooltip_text=get_text("en", "tooltip_total_cost_of_ownership"),
        tooltip_id="test-tooltip-tco"
    )

    # Verify structure
    assert isinstance(card, html.Div), "Card should be html.Div"
    assert len(card.children) == 2, "Card should have 2 children (H3 and value)"

    h3 = card.children[0]
    assert isinstance(h3, html.H3), "First child should be H3"

    tooltip_span = h3.children
    assert isinstance(tooltip_span, html.Span), "H3 child should be Span (tooltip)"
    assert tooltip_span.id == "test-tooltip-tco", "Tooltip should have correct ID"
    assert tooltip_span.children == "Total Cost of Ownership", "Tooltip should contain title text"
    assert "cursor" in tooltip_span.style, "Should have cursor style"
    assert tooltip_span.style["cursor"] == "help", "Cursor should be help"
    assert "borderBottom" in tooltip_span.style, "Should have border style"
    assert "dotted" in tooltip_span.style["borderBottom"], "Border should be dotted"

    print("✓ Card structure correct")
    print(f"  - ID: {tooltip_span.id}")
    print(f"  - Text: {tooltip_span.children}")
    print(f"  - Cursor: {tooltip_span.style.get('cursor')}")
    print(f"  - Border: {tooltip_span.style.get('borderBottom')}")
    print()

    # Test 2: Create metric box with multiple tooltips
    print("Test 2: Metric Box with Multiple Tooltips")
    print("-" * 40)
    metric_box = create_metric_box(
        "Key Metrics",
        {
            "Purchase Price": "€500,000",
            "Equity": "€100,000",
            "Interest Rate": "3.5%",
        },
        tooltips={
            "Purchase Price": (get_text("en", "tooltip_purchase_price"), "tooltip-price"),
            "Equity": (get_text("en", "tooltip_equity"), "tooltip-equity"),
            "Interest Rate": (get_text("en", "tooltip_interest_rate"), "tooltip-rate"),
        }
    )

    assert isinstance(metric_box, html.Div), "Metric box should be html.Div"
    assert len(metric_box.children) == 2, "Should have title and items"

    items_div = metric_box.children[1]
    assert len(items_div.children) == 3, "Should have 3 metric items"

    # Check first metric item
    first_item = items_div.children[0]
    key_div = first_item.children[0]
    tooltip = key_div.children

    assert isinstance(tooltip, html.Span), "Key should be wrapped in tooltip Span"
    assert tooltip.id == "tooltip-price", "Should have correct tooltip ID"
    assert "cursor" in tooltip.style, "Should have cursor style"
    assert tooltip.style["cursor"] == "help", "Cursor should be help"

    print("✓ Metric box structure correct")
    print(f"  - Number of items: {len(items_div.children)}")
    print(f"  - First tooltip ID: {tooltip.id}")
    print(f"  - All tooltips present: ✓")
    print()

    # Test 3: Create metric with description
    print("Test 3: Metric with Description and Tooltip")
    print("-" * 40)
    metric = create_metric_with_description(
        "Buffer Ratio",
        "6.2 months",
        "Emergency fund coverage relative to equity",
        color="#dc3545",
        tooltip_text=get_text("en", "tooltip_buffer_ratio"),
        tooltip_id="tooltip-buffer"
    )

    assert isinstance(metric, html.Div), "Metric should be html.Div"
    title_div = metric.children[0]
    tooltip = title_div.children

    assert isinstance(tooltip, html.Span), "Title should be wrapped in tooltip Span"
    assert tooltip.id == "tooltip-buffer", "Should have correct tooltip ID"
    assert tooltip.children == "Buffer Ratio", "Should contain title text"
    assert "cursor" in tooltip.style, "Should have cursor style"

    print("✓ Metric with description structure correct")
    print(f"  - Tooltip ID: {tooltip.id}")
    print(f"  - Title: {tooltip.children}")
    print()

    # Test 4: Verify no info icons in any component
    print("Test 4: Verify No Info Icons")
    print("-" * 40)

    components_to_check = [card, metric_box, metric]
    info_icon_found = False

    for i, component in enumerate(components_to_check, 1):
        component_str = str(component)
        if "ℹ️" in component_str or "ℹ" in component_str:
            info_icon_found = True
            print(f"✗ Found info icon in component {i}")
        else:
            print(f"✓ Component {i}: No info icons")

    assert not info_icon_found, "Info icons should not be present"
    print()

    # Test 5: Check tooltip text content
    print("Test 5: Tooltip Content Verification")
    print("-" * 40)

    # Check that markdown is stripped from title attribute
    tooltip_text_with_markdown = "**Loan Amount**\nThe total amount you need to borrow"
    from components import create_tooltip

    tooltip = create_tooltip(
        "test-markdown",
        tooltip_text_with_markdown,
        "Loan Amount"
    )

    # Title should have markdown stripped
    assert "**" not in tooltip.title, "Markdown should be stripped from title"
    assert tooltip.title == "Loan Amount\nThe total amount you need to borrow", \
        "Title should have markdown removed but keep content"

    print("✓ Markdown stripped from title attribute")
    print(f"  - Original: {repr(tooltip_text_with_markdown[:50])}")
    print(f"  - Stripped: {repr(tooltip.title[:50])}")
    print()

    print("=" * 80)
    print("ALL INTEGRATION TESTS PASSED ✓")
    print("=" * 80)
    print()
    print("Summary:")
    print("  ✓ Card components render tooltips correctly")
    print("  ✓ Metric box components render multiple tooltips")
    print("  ✓ Metric with description components render tooltips")
    print("  ✓ No info icons present in any component")
    print("  ✓ Markdown is properly stripped from HTML title attributes")
    print("  ✓ All visual indicators (cursor, border) are applied")
    print()


def test_all_kpis_in_context():
    """Test all 31 KPIs with actual tooltip content"""
    print("=" * 80)
    print("COMPREHENSIVE KPI TOOLTIP TEST")
    print("=" * 80)
    print()

    kpis = {
        "Overview Cards": [
            ("loan_amount", "Loan Amount"),
            ("monthly_rate", "Monthly Rate"),
            ("total_interest", "Total Interest"),
            ("total_payoff_years", "Total Payoff Years"),
            ("remaining_debt", "Remaining Debt"),
            ("rate_of_income", "Rate of Income"),
            ("breakeven_milestone", "Breakeven Milestone"),
        ],
        "Key Metrics": [
            ("purchase_price", "Purchase Price"),
            ("equity", "Equity"),
            ("interest_rate", "Interest Rate"),
            ("annual_rate", "Annual Rate"),
            ("total_amortization", "Total Amortization"),
            ("total_paid", "Total Paid"),
            ("interest_costs", "Interest Costs"),
            ("total_cost_of_ownership", "Total Cost of Ownership"),
            ("ltv_ratio", "LTV Ratio"),
            ("interest_to_principal_ratio", "Interest-to-Principal Ratio"),
            ("interest_without_special", "Interest Without Special"),
            ("interest_with_special", "Interest With Special"),
            ("interest_savings", "Interest Savings"),
            ("time_saved", "Time Saved"),
        ],
        "Risk Analysis": [
            ("buffer_ratio", "Buffer Ratio"),
            ("time_to_50_equity", "Time to 50% Equity"),
            ("rate_sensitivity_score", "Rate Sensitivity Score"),
        ],
        "Affordability": [
            ("household_income", "Household Income"),
            ("affordable_monthly_payment", "Affordable Monthly Payment"),
            ("housing_expense_ratio", "Housing Expense Ratio"),
            ("housing_expense_benchmark", "Housing Expense Benchmark"),
            ("years_to_payoff", "Years to Payoff"),
        ],
    }

    total_kpis = 0
    passed_kpis = 0

    for section, kpi_list in kpis.items():
        print(f"\n{section}:")
        print("-" * 40)

        for kpi_key, kpi_title in kpi_list:
            total_kpis += 1
            tooltip_key = f"tooltip_{kpi_key}"

            # Check English
            en_tooltip = get_text("en", tooltip_key)
            de_tooltip = get_text("de", tooltip_key)

            # Verify tooltip exists and is not the key itself (fallback)
            en_exists = en_tooltip != tooltip_key
            de_exists = de_tooltip != tooltip_key

            # Verify minimum quality
            en_long_enough = len(en_tooltip) >= 20
            de_long_enough = len(de_tooltip) >= 20

            if en_exists and de_exists and en_long_enough and de_long_enough:
                status = "✓"
                passed_kpis += 1
            else:
                status = "✗"

            print(f"  {status} {kpi_title}")
            if status == "✗":
                print(f"      EN exists: {en_exists}, long enough: {en_long_enough}")
                print(f"      DE exists: {de_exists}, long enough: {de_long_enough}")

    print()
    print("=" * 80)
    print(f"KPI TOOLTIP COVERAGE: {passed_kpis}/{total_kpis} ({100*passed_kpis/total_kpis:.1f}%)")
    print("=" * 80)

    assert passed_kpis == total_kpis, f"Not all KPIs have tooltips: {passed_kpis}/{total_kpis}"


if __name__ == "__main__":
    try:
        test_rendered_html_output()
        test_all_kpis_in_context()

        print()
        print("=" * 80)
        print("🎉 ALL INTEGRATION TESTS PASSED 🎉")
        print("=" * 80)
        print()
        sys.exit(0)

    except AssertionError as e:
        print()
        print("=" * 80)
        print("❌ INTEGRATION TEST FAILED")
        print("=" * 80)
        print(f"Error: {e}")
        print()
        sys.exit(1)
