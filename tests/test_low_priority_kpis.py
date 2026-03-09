"""
Tests for Low-Priority KPIs
Tests the buffer ratio, time to 50% equity, and rate sensitivity score
"""

import pytest
import sys
from pathlib import Path

# Add app directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from calculator import FinancingCalculator, FinancingInput


class TestBufferRatio:
    """Test Buffer Ratio KPI - Emergency fund buffer relative to equity"""

    def test_buffer_ratio_basic(self):
        """Test buffer ratio calculation with standard inputs"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # Buffer ratio = (Monthly Payment × 6) / Current Equity
        expected_buffer = (calc.monthly_payment * 6) / input_data.equity
        assert abs(summary["buffer_ratio"] - expected_buffer) < 0.01

    def test_buffer_ratio_zero_equity(self):
        """Test buffer ratio with zero equity (edge case)"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=0,  # Zero equity
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # Should return 0 to avoid division by zero
        assert summary["buffer_ratio"] == 0

    def test_buffer_ratio_high_equity(self):
        """Test buffer ratio with high equity (lower ratio)"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=400000,  # 80% equity
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # Higher equity should result in lower buffer ratio
        assert summary["buffer_ratio"] > 0
        assert summary["buffer_ratio"] < 0.1  # Should be quite low


class TestTimeTo50Equity:
    """Test Time to 50% Equity KPI - Years until owning half the property"""

    def test_time_to_50_equity_basic(self):
        """Test time to 50% equity with standard inputs"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,  # Starting at 20%
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # Should return a positive number of years
        assert summary["time_to_50_equity"] > 0
        # Should be less than total payoff time
        payoff_years = calc.calculate_payoff_years()
        assert summary["time_to_50_equity"] < payoff_years

    def test_time_to_50_equity_already_above_50(self):
        """Test time to 50% equity when already above 50%"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=300000,  # Already at 60%
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # Should be 0 or very close to 0 since already above 50%
        assert summary["time_to_50_equity"] < 1

    def test_time_to_50_equity_with_special_payment(self):
        """Test time to 50% equity with special payments (should be faster)"""
        input_data_no_special = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=0,
        )
        input_data_with_special = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=5000,
        )

        calc_no_special = FinancingCalculator(input_data_no_special)
        calc_with_special = FinancingCalculator(input_data_with_special)

        summary_no_special = calc_no_special.get_summary(30)
        summary_with_special = calc_with_special.get_summary(30)

        # With special payments, should reach 50% equity faster
        assert (
            summary_with_special["time_to_50_equity"]
            < summary_no_special["time_to_50_equity"]
        )


class TestRateSensitivity:
    """Test Rate Sensitivity Score - Payment increase if rates rise by 1%"""

    def test_rate_sensitivity_basic(self):
        """Test rate sensitivity calculation with standard inputs"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # Should be positive
        assert summary["rate_sensitivity_score"] > 0

        # Calculate expected sensitivity manually
        loan_amount = input_data.purchase_price - input_data.equity
        current_rate = input_data.interest_rate / 100
        new_rate = (input_data.interest_rate + 1) / 100
        amort_rate = input_data.initial_amortization / 100

        current_annual = loan_amount * (current_rate + amort_rate)
        new_annual = loan_amount * (new_rate + amort_rate)

        expected_sensitivity = (new_annual - current_annual) / 12

        assert abs(summary["rate_sensitivity_score"] - expected_sensitivity) < 0.01

    def test_rate_sensitivity_large_loan(self):
        """Test rate sensitivity with large loan (higher sensitivity)"""
        input_data = FinancingInput(
            purchase_price=1000000,
            equity=100000,  # Large loan
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # Larger loan should have higher rate sensitivity
        assert summary["rate_sensitivity_score"] > 500

    def test_rate_sensitivity_small_loan(self):
        """Test rate sensitivity with small loan (lower sensitivity)"""
        input_data = FinancingInput(
            purchase_price=300000,
            equity=200000,  # Small loan
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # Smaller loan should have lower rate sensitivity
        assert summary["rate_sensitivity_score"] < 200

    def test_rate_sensitivity_zero_loan(self):
        """Test rate sensitivity with no loan (zero sensitivity)"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=500000,  # Full equity, no loan
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # No loan means no rate sensitivity
        assert summary["rate_sensitivity_score"] == 0


class TestKPIsIntegration:
    """Test that all low-priority KPIs are included in summary"""

    def test_all_kpis_in_summary(self):
        """Test that all low-priority KPIs are present in summary"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # Check all low-priority KPIs are present
        assert "buffer_ratio" in summary
        assert "time_to_50_equity" in summary
        assert "rate_sensitivity_score" in summary

    def test_kpis_are_numeric(self):
        """Test that all KPIs return numeric values"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # All should be numeric
        assert isinstance(summary["buffer_ratio"], (int, float))
        assert isinstance(summary["time_to_50_equity"], (int, float))
        assert isinstance(summary["rate_sensitivity_score"], (int, float))

    def test_kpis_realistic_values(self):
        """Test that KPIs return realistic values"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # Buffer ratio should be reasonable (typically less than 12 months)
        assert 0 <= summary["buffer_ratio"] < 12

        # Time to 50% equity should be within payoff period
        payoff_years = calc.calculate_payoff_years()
        assert 0 <= summary["time_to_50_equity"] <= payoff_years

        # Rate sensitivity should be positive and reasonable
        assert 0 <= summary["rate_sensitivity_score"] < summary["monthly_payment"]
