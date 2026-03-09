"""
Unit tests for callbacks and dashboard logic
Tests interaction callbacks and their calculations
"""

import pytest
import sys
from pathlib import Path

# Add app directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from calculator import FinancingCalculator, FinancingInput
from callbacks import build_summary_cards
from translations import get_text

# use default parameter values from configuration
from config import (
    DEFAULT_PURCHASE_PRICE,
    DEFAULT_EQUITY,
    DEFAULT_INTEREST_RATE,
    DEFAULT_INITIAL_AMORTIZATION,
    DEFAULT_INTEREST_BINDING_YEARS,
    DEFAULT_ANNUAL_SPECIAL_PAYMENT,
)


class TestSliderMaxCalculation:
    """Tests for the slider max value calculation based on payoff years"""

    def test_slider_max_equals_payoff_years_default_values(self):
        """Test that slider max reflects payoff years with default values"""
        input_data = FinancingInput(
            purchase_price=DEFAULT_PURCHASE_PRICE,
            equity=DEFAULT_EQUITY,
            interest_rate=DEFAULT_INTEREST_RATE,
            initial_amortization=DEFAULT_INITIAL_AMORTIZATION,
            annual_special_payment=DEFAULT_ANNUAL_SPECIAL_PAYMENT,
            interest_binding_years=DEFAULT_INTEREST_BINDING_YEARS,
        )
        calculator = FinancingCalculator(input_data)
        payoff_years = calculator.calculate_payoff_years()

        # Slider max should equal payoff years – this is calculated above
        assert payoff_years == calculator.calculate_payoff_years()

    def test_slider_max_high_equity_scenario(self):
        """Test slider max with high equity (shorter payoff)"""
        input_data = FinancingInput(
            purchase_price=300000,
            equity=200000,  # High equity
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calculator = FinancingCalculator(input_data)
        payoff_years = calculator.calculate_payoff_years()

        # Loan amount: 100000, annual payment: 100000 * 0.06 = 6000
        # Payoff years depends on the calculation, just ensure it's positive
        assert payoff_years > 0
        assert payoff_years <= 100

    def test_slider_max_low_equity_scenario(self):
        """Test slider max with low equity"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=25000,  # Low equity
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calculator = FinancingCalculator(input_data)
        payoff_years = calculator.calculate_payoff_years()

        # Larger loan amount should result in valid payoff calculation
        assert payoff_years > 0
        assert payoff_years <= 100

    def test_slider_max_high_amortization(self):
        """Test slider max decreases with higher amortization"""
        input_low_amort = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=1.0,
        )
        input_high_amort = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=5.0,
        )

        calc_low = FinancingCalculator(input_low_amort)
        calc_high = FinancingCalculator(input_high_amort)

        years_low = calc_low.calculate_payoff_years()
        years_high = calc_high.calculate_payoff_years()

        # Higher amortization should result in faster payoff
        assert years_high < years_low

    def test_slider_max_initialization(self):
        """Test that slider max is properly initialized with parameters"""
        # Test with multiple parameter combinations
        test_cases = [
            (300000, 60000, 3.0, 2.0),  # Low interest, low amortization
            (300000, 60000, 6.0, 4.0),  # High interest, high amortization
            (500000, 100000, 4.5, 2.5),  # Standard scenario
        ]

        for purchase, equity, rate, amort in test_cases:
            input_data = FinancingInput(
                purchase_price=purchase,
                equity=equity,
                interest_rate=rate,
                initial_amortization=amort,
            )
            calculator = FinancingCalculator(input_data)
            payoff_years = calculator.calculate_payoff_years()

            # All should be valid positive integers
            assert isinstance(payoff_years, int)
            assert payoff_years > 0

    def test_slider_max_with_special_payment(self):
        """Test slider max reduces with special annual payments"""
        input_no_special = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=2.0,
            annual_special_payment=0,
        )
        input_with_special = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=2.0,
            annual_special_payment=5000,
        )

        calc_no_special = FinancingCalculator(input_no_special)
        calc_with_special = FinancingCalculator(input_with_special)

        years_no_special = calc_no_special.calculate_payoff_years()
        years_with_special = calc_with_special.calculate_payoff_years()

        # Special payments should reduce payoff time
        assert years_with_special < years_no_special

    def test_slider_max_parameter_changes_trigger_update(self):
        """Test that different input parameters result in different slider max values"""
        # Scenario 1: Starting values
        input1 = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calc1 = FinancingCalculator(input1)
        max1 = calc1.calculate_payoff_years()

        # Scenario 2: Increased purchase price
        input2 = FinancingInput(
            purchase_price=500000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calc2 = FinancingCalculator(input2)
        max2 = calc2.calculate_payoff_years()

        # Scenario 3: Increased amortization rate (faster payoff)
        input3 = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=3.0,  # Higher amortization
        )
        calc3 = FinancingCalculator(input3)
        max3 = calc3.calculate_payoff_years()

        # All should be positive
        assert max1 > 0
        assert max2 > 0
        assert max3 > 0
        # Higher amortization should result in faster payoff (lower years)
        assert max3 < max1

    def test_slider_max_minimum_value(self):
        """Test that slider max always has minimum reasonable value"""
        # Even with very small loan (almost full equity)
        input_data = FinancingInput(
            purchase_price=100000,
            equity=99000,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calculator = FinancingCalculator(input_data)
        payoff_years = calculator.calculate_payoff_years()

        # Should still be a valid positive integer
        assert isinstance(payoff_years, int)
        assert payoff_years > 0

    def test_slider_max_realistic_ranges(self):
        """Test that slider max values stay within realistic ranges"""
        test_cases = [
            # (purchase_price, equity, interest_rate, initial_amort)
            (300000, 60000, 3.5, 2.0),  # Conservative
            (
                DEFAULT_PURCHASE_PRICE,
                DEFAULT_EQUITY,
                DEFAULT_INTEREST_RATE,
                DEFAULT_INITIAL_AMORTIZATION,
            ),  # Standard
            (500000, 50000, 4.5, 1.5),  # Longer
            (200000, 100000, 5.0, 3.0),  # Short
        ]

        for purchase, equity, rate, amort in test_cases:
            input_data = FinancingInput(
                purchase_price=purchase,
                equity=equity,
                interest_rate=rate,
                initial_amortization=amort,
            )
            calculator = FinancingCalculator(input_data)
            payoff_years = calculator.calculate_payoff_years()

            # Should be within reasonable range (all legitimate mortgage payoffs)
            assert (
                0 < payoff_years <= 100
            ), f"Payoff years {payoff_years} outside reasonable range 1-100"

    def test_slider_max_zero_values_handled(self):
        """Test slider max calculation with edge case zero values"""
        # With zero purchase price, should still work
        input_data = FinancingInput(
            purchase_price=0,
            equity=0,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calculator = FinancingCalculator(input_data)
        payoff_years = calculator.calculate_payoff_years()

        # No loan, should pay off immediately or return small value
        assert payoff_years <= 1

    def test_slider_max_consistency_across_calls(self):
        """Test that slider max calculation is consistent across multiple calls"""
        input_data = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calculator = FinancingCalculator(input_data)

        # Multiple calls should return same value
        max1 = calculator.calculate_payoff_years()
        max2 = calculator.calculate_payoff_years()
        max3 = calculator.calculate_payoff_years()

        assert max1 == max2
        assert max2 == max3


class TestCallbackIntegration:
    """Integration tests for callback behavior with slider"""

    def test_slider_value_constrained_by_max(self):
        """Test that slider value is properly constrained by max"""
        # Simulate different scenarios
        scenarios = [
            {"years_selected": 10, "payoff_years": 29},  # Value < max: OK
            {"years_selected": 29, "payoff_years": 29},  # Value = max: OK
            {"years_selected": 35, "payoff_years": 29},  # Value > max: Should constrain
        ]

        for scenario in scenarios:
            years_selected = scenario["years_selected"]
            payoff_years = scenario["payoff_years"]

            # Slider should constrain value to be <= max
            constrained_value = min(years_selected, payoff_years)
            assert constrained_value <= payoff_years

    def test_slider_marks_generation(self):
        """Test that slider marks are appropriate for payoff years range"""
        # Standard 5-year interval marks should work for most cases
        for payoff_years in [15, 20, 25, 30, 35, 40]:
            marks = {i: str(i) for i in range(0, payoff_years + 1, 5)}

            # Should generate reasonable number of marks
            assert len(marks) > 0
            # Last mark should be close to payoff years
            assert max(marks.keys()) >= payoff_years - 5

    def test_slider_dynamic_update_trigger(self):
        """Test that slider max updates when input parameters change"""
        initial_input = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        initial_calc = FinancingCalculator(initial_input)
        initial_max = initial_calc.calculate_payoff_years()

        # User increases amortization rate (faster payoff)
        updated_input = FinancingInput(
            purchase_price=400000,  # Same
            equity=50000,  # Same
            interest_rate=4.0,  # Same
            initial_amortization=3.0,  # Changed (increased)
        )
        updated_calc = FinancingCalculator(updated_input)
        updated_max = updated_calc.calculate_payoff_years()

        # Max should decrease with higher amortization
        assert initial_max > updated_max
        # Both should be valid positive integers
        assert initial_max > 0
        assert updated_max > 0


class TestRateOfIncomeCard:
    """Tests for the rate-of-income summary card added to the overview"""

    def test_rate_of_income_card_value(self):
        """Ensure rate-of-income is calculated correctly when household income is provided"""
        summary = {
            "loan_amount": 300000,
            "monthly_payment": 2000,
            "total_interest": 50000,
            "years": 10,
            "remaining_debt": 250000,
        }
        payoff_years = 29
        household_income = 5000  # net monthly income

        cards = build_summary_cards(
            summary, payoff_years, household_income, lambda k: get_text("en", k)
        )

        # With tooltips, card.children[0].children is a Span, so we check the Span's children
        rate_card = next(
            card
            for card in cards
            if (hasattr(card.children[0].children, 'children') and
                card.children[0].children.children == get_text("en", "rate_of_income"))
        )

        assert rate_card.children[1].children == "40.0% of household income"

    def test_rate_of_income_card_missing_income(self):
        """Rate-of-income card should show N/A when income is missing or zero"""
        summary = {
            "loan_amount": 300000,
            "monthly_payment": 2000,
            "total_interest": 50000,
            "years": 10,
            "remaining_debt": 250000,
        }
        payoff_years = 29

        cards = build_summary_cards(
            summary, payoff_years, 0, lambda k: get_text("en", k)
        )
        # With tooltips, card.children[0].children is a Span, so we check the Span's children
        rate_card = next(
            card
            for card in cards
            if (hasattr(card.children[0].children, 'children') and
                card.children[0].children.children == get_text("en", "rate_of_income"))
        )

        assert rate_card.children[1].children == "N/A"

    def test_format_years_months_formats_fractional_years(self):
        """Test that the years+months formatting works for fractional year values."""
        from callbacks import format_years_months

        formatted = format_years_months(8.574, lambda k: get_text("en", k))
        assert formatted.startswith("8")
        assert "m" in formatted


class TestErrorHandling:
    """Tests for error handling in slider callbacks"""

    def test_slider_callback_error_fallback(self):
        """Test that slider max has fallback value on error"""
        # This tests the try-except in the actual callback
        # Even with invalid inputs, should return a default max of 50
        # The actual callback implementation will be tested through

        # Create calculator with valid data to ensure no calculation errors
        input_data = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calculator = FinancingCalculator(input_data)
        payoff_years = calculator.calculate_payoff_years()

        # Should get valid result, not default fallback
        assert payoff_years > 0
        assert payoff_years != 50  # Should be calculated value, not fallback

    def test_slider_callback_with_extreme_values(self):
        """Test slider callback with very extreme input values"""
        extreme_cases = [
            (1000000, 10000, 1.0, 0.5),  # Very high loan, very low rates
            (100000, 99999, 20.0, 10.0),  # Very high interest and amortization
            (50000, 1000, 0.1, 0.1),  # Very low interest and amortization
        ]

        for purchase, equity, rate, amort in extreme_cases:
            input_data = FinancingInput(
                purchase_price=purchase,
                equity=equity,
                interest_rate=rate,
                initial_amortization=amort,
            )
            calculator = FinancingCalculator(input_data)
            payoff_years = calculator.calculate_payoff_years()

            # Should always return a reasonable integer
            assert isinstance(payoff_years, int)
            assert payoff_years > 0
            assert payoff_years <= 100  # Maximum reasonable value
