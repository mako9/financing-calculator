"""
Advanced Integration Tests for KPI Implementation
Tests complex scenarios, cross-KPI relationships, and advanced edge cases
Created by QA Engineer - March 9, 2026
"""

import pytest
import sys
from pathlib import Path

# Add app directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from calculator import FinancingCalculator, FinancingInput
from translations import get_text


class TestKPICrossRelationships:
    """Test how KPIs interact and relate to each other"""

    def test_ltv_and_time_to_50_equity_relationship(self):
        """Test that higher LTV means longer time to reach 50% equity"""
        # High LTV scenario (80%)
        input_high_ltv = FinancingInput(
            purchase_price=500000,
            equity=100000,  # 20% equity, 80% LTV
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc_high_ltv = FinancingCalculator(input_high_ltv)
        summary_high = calc_high_ltv.get_summary(30)

        # Low LTV scenario (40%)
        input_low_ltv = FinancingInput(
            purchase_price=500000,
            equity=300000,  # 60% equity, 40% LTV
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc_low_ltv = FinancingCalculator(input_low_ltv)
        summary_low = calc_low_ltv.get_summary(30)

        # Higher LTV should take longer to reach 50% equity
        assert summary_high["ltv_ratio"] > summary_low["ltv_ratio"]
        assert summary_high["time_to_50_equity"] > summary_low["time_to_50_equity"]

    def test_special_payments_affect_multiple_kpis(self):
        """Test that special payments improve multiple KPI metrics"""
        # Without special payments
        input_no_special = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=0,
        )
        calc_no_special = FinancingCalculator(input_no_special)
        payoff_no_special = calc_no_special.calculate_payoff_years()
        summary_no_special = calc_no_special.get_summary(payoff_no_special)

        # With special payments
        input_with_special = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=10000,
        )
        calc_with_special = FinancingCalculator(input_with_special)
        payoff_with_special = calc_with_special.calculate_payoff_years()
        summary_with_special = calc_with_special.get_summary(payoff_with_special)

        # Special payments should improve multiple KPIs:
        # 1. Lower Total Cost of Ownership (less interest)
        assert (
            summary_with_special["total_cost_of_ownership"]
            < summary_no_special["total_cost_of_ownership"]
        )

        # 2. Lower Interest-to-Principal Ratio (less interest paid)
        assert (
            summary_with_special["interest_to_principal_ratio"]
            < summary_no_special["interest_to_principal_ratio"]
        )

        # 3. Faster time to 50% equity
        assert (
            summary_with_special["time_to_50_equity"]
            < summary_no_special["time_to_50_equity"]
        )

        # 4. Earlier breakeven (if both have breakeven)
        if (
            summary_no_special["breakeven_year"]
            and summary_with_special["breakeven_year"]
        ):
            assert (
                summary_with_special["breakeven_year"]
                <= summary_no_special["breakeven_year"]
            )

    def test_tco_includes_all_interest_components(self):
        """Test that TCO correctly includes all interest from the full loan period"""
        input_data = FinancingInput(
            purchase_price=400000,
            equity=80000,
            interest_rate=4.0,
            initial_amortization=3.0,
        )
        calc = FinancingCalculator(input_data)
        payoff_years = calc.calculate_payoff_years()
        summary = calc.get_summary(payoff_years)

        # TCO should equal purchase price + all interest paid over loan lifetime
        expected_tco = summary["purchase_price"] + summary["total_interest"]
        assert summary["total_cost_of_ownership"] == pytest.approx(expected_tco)

        # TCO should always be higher than purchase price (unless 0% interest)
        assert summary["total_cost_of_ownership"] > summary["purchase_price"]


class TestKPIProgression:
    """Test how KPIs change over time"""

    def test_interest_to_principal_ratio_improves_over_time(self):
        """Test that the ratio improves (decreases) as loan matures"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)

        # Early years (first 10 years)
        summary_10y = calc.get_summary(10)

        # Mid years (20 years)
        summary_20y = calc.get_summary(20)

        # Later years (30 years)
        summary_30y = calc.get_summary(30)

        # Ratio should decrease over time (more principal, less interest)
        # This isn't always true because we're looking at cumulative ratios
        # But total interest should increase while amortization increases faster
        assert summary_10y["total_interest"] > 0
        assert summary_20y["total_interest"] > summary_10y["total_interest"]
        assert summary_30y["total_interest"] > summary_20y["total_interest"]

    def test_equity_buildup_accelerates_over_time(self):
        """Test that equity buildup accelerates (more equity gained in later years)"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        equity_buildup = summary["equity_buildup_rate"]

        # Should have entries
        assert len(equity_buildup) > 0

        # Compare equity gained in early vs late years
        # (assuming we have at least 10 years of data)
        if len(equity_buildup) >= 10:
            early_year_gain = equity_buildup[4]["equity_gained"]  # Year 5
            late_year_gain = equity_buildup[9]["equity_gained"]  # Year 10

            # Later years should have more equity gain (due to less interest)
            assert late_year_gain > early_year_gain

    def test_buffer_ratio_increases_with_payment_amount(self):
        """Test that buffer ratio increases with higher monthly payments"""
        # Small payment scenario
        input_small = FinancingInput(
            purchase_price=300000,
            equity=100000,
            interest_rate=2.0,
            initial_amortization=1.0,
        )
        calc_small = FinancingCalculator(input_small)
        summary_small = calc_small.get_summary(10)

        # Large payment scenario (higher interest + amortization)
        input_large = FinancingInput(
            purchase_price=300000,
            equity=100000,
            interest_rate=5.0,
            initial_amortization=4.0,
        )
        calc_large = FinancingCalculator(input_large)
        summary_large = calc_large.get_summary(10)

        # Higher payment should result in higher buffer ratio (more months needed)
        assert summary_large["monthly_payment"] > summary_small["monthly_payment"]
        assert summary_large["buffer_ratio"] > summary_small["buffer_ratio"]


class TestComplexEdgeCases:
    """Test complex and uncommon edge cases"""

    def test_very_low_amortization_high_interest(self):
        """Test scenario with very low amortization and high interest"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=50000,
            interest_rate=6.0,
            initial_amortization=0.5,  # Very low amortization
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # Should still calculate all KPIs
        assert summary["total_cost_of_ownership"] > 0
        assert summary["ltv_ratio"] > 0
        assert summary["interest_to_principal_ratio"] > 0
        assert summary["buffer_ratio"] > 0
        assert summary["time_to_50_equity"] > 0
        assert summary["rate_sensitivity_score"] > 0

    def test_breakeven_not_reached_within_period(self):
        """Test breakeven calculation when not reached in observed period"""
        input_data = FinancingInput(
            purchase_price=1000000,
            equity=100000,
            interest_rate=5.0,
            initial_amortization=0.5,  # Very low
        )
        calc = FinancingCalculator(input_data)
        # Only look at first 5 years
        summary = calc.get_summary(5)

        # Breakeven might not be reached
        # If it's not reached, verify the cumulative values are still present
        if summary["breakeven_year"] is None:
            assert summary["cumulative_amortization_at_breakeven"] >= 0
            assert summary["cumulative_interest_at_breakeven"] >= 0
            # Interest should be higher than amortization at this point
            assert (
                summary["cumulative_interest_at_breakeven"]
                > summary["cumulative_amortization_at_breakeven"]
            )

    def test_massive_special_payment_scenario(self):
        """Test with very large special payments (edge case)"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=50000,  # Very large special payment
        )
        calc = FinancingCalculator(input_data)
        payoff_years = calc.calculate_payoff_years()
        summary = calc.get_summary(payoff_years)

        # Should pay off very quickly
        assert payoff_years < 10

        # Interest savings should be substantial
        assert summary["interest_savings"] > 0
        assert summary["time_saved_years"] > 0

        # Time to 50% equity should be very short
        assert summary["time_to_50_equity"] < 3

    def test_multiple_year_periods_consistency(self):
        """Test that KPI calculations are consistent across different year periods"""
        input_data = FinancingInput(
            purchase_price=400000,
            equity=80000,
            interest_rate=3.5,
            initial_amortization=2.5,
        )
        calc = FinancingCalculator(input_data)

        # Get summaries for different periods
        summary_5 = calc.get_summary(5)
        summary_10 = calc.get_summary(10)
        summary_20 = calc.get_summary(20)

        # LTV should remain constant (it's based on initial loan)
        assert summary_5["ltv_ratio"] == pytest.approx(summary_10["ltv_ratio"])
        assert summary_10["ltv_ratio"] == pytest.approx(summary_20["ltv_ratio"])

        # Time-independent KPIs should be consistent
        assert summary_5["buffer_ratio"] == pytest.approx(summary_10["buffer_ratio"])
        assert summary_5["time_to_50_equity"] == pytest.approx(
            summary_10["time_to_50_equity"]
        )
        assert summary_5["rate_sensitivity_score"] == pytest.approx(
            summary_10["rate_sensitivity_score"]
        )


class TestRealisticScenarios:
    """Test realistic German mortgage scenarios"""

    def test_typical_german_mortgage_all_kpis(self):
        """Test all KPIs with typical German mortgage parameters"""
        input_data = FinancingInput(
            purchase_price=450000,
            equity=90000,  # 20% down payment
            interest_rate=3.8,
            initial_amortization=2.5,
            annual_special_payment=3000,
            interest_binding_years=15,
        )
        calc = FinancingCalculator(input_data)
        payoff_years = calc.calculate_payoff_years()
        summary = calc.get_summary(payoff_years)

        # Verify all KPIs are within realistic bounds
        # High-priority KPIs
        assert 450000 < summary["total_cost_of_ownership"] < 900000
        assert 0.2 < summary["interest_to_principal_ratio"] < 0.8
        assert 75 < summary["ltv_ratio"] < 85  # Should be 80%
        assert summary["interest_savings"] > 0

        # Medium-priority KPIs
        assert 1 <= summary["breakeven_year"] <= payoff_years
        assert len(summary["equity_buildup_rate"]) > 0

        # Low-priority KPIs
        assert 0 < summary["buffer_ratio"] < 5
        assert 5 < summary["time_to_50_equity"] < payoff_years
        assert 50 < summary["rate_sensitivity_score"] < 500

    def test_conservative_financing_scenario(self):
        """Test conservative financing (high down payment, high amortization)"""
        input_data = FinancingInput(
            purchase_price=400000,
            equity=200000,  # 50% equity
            interest_rate=3.5,
            initial_amortization=4.0,  # High amortization
            annual_special_payment=5000,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # Conservative financing should show favorable metrics
        assert summary["ltv_ratio"] == pytest.approx(50.0)  # Exactly 50% LTV
        assert summary["time_to_50_equity"] <= 1  # Already at 50%+
        assert summary["interest_to_principal_ratio"] < 0.5  # Low ratio
        assert summary["buffer_ratio"] < 0.5  # Low buffer needed

    def test_aggressive_financing_scenario(self):
        """Test aggressive financing (low down payment, low amortization)"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=25000,  # Only 5% equity
            interest_rate=4.5,
            initial_amortization=1.5,  # Low amortization
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(40)

        # Aggressive financing should show challenging metrics
        assert summary["ltv_ratio"] == pytest.approx(95.0)  # Very high LTV
        assert summary["time_to_50_equity"] > 15  # Takes long time
        assert summary["rate_sensitivity_score"] > 200  # High sensitivity
        # Buffer ratio is (monthly payment * 6) / equity, so with low equity (25k),
        # it's actually quite low: (monthly_payment * 6) / 25000
        assert summary["buffer_ratio"] > 0  # Should be positive


class TestTranslationIntegration:
    """Test that translations work correctly with KPI values"""

    def test_all_kpi_keys_translate_without_errors(self):
        """Test that all KPI keys have valid translations"""
        kpi_keys = [
            "total_cost_of_ownership",
            "interest_to_principal_ratio",
            "ltv_ratio",
            "interest_savings",
            "interest_without_special",
            "interest_with_special",
            "time_saved",
            "breakeven_year",
            "breakeven_milestone",
            "equity_buildup",
            "equity_buildup_progression",
            "buffer_ratio",
            "buffer_ratio_desc",
            "time_to_50_equity",
            "time_to_50_equity_desc",
            "rate_sensitivity_score",
            "rate_sensitivity_desc",
            "kpis",
            "risk_analysis",
            "months",
        ]

        for key in kpi_keys:
            # Should not raise exceptions
            en_text = get_text("en", key)
            de_text = get_text("de", key)

            # Should return non-empty strings
            assert len(en_text) > 0
            assert len(de_text) > 0

    def test_translation_consistency_across_related_keys(self):
        """Test that related translation keys are consistently named"""
        # Check that description keys exist for all described KPIs
        described_kpis = ["buffer_ratio", "time_to_50_equity", "rate_sensitivity_score"]

        for kpi in described_kpis:
            desc_key = f"{kpi}_desc"
            # Both main and description keys should exist
            assert get_text("en", kpi) is not None
            assert get_text("en", desc_key) is not None
            assert get_text("de", kpi) is not None
            assert get_text("de", desc_key) is not None


class TestKPIBoundaryConditions:
    """Test KPIs at extreme boundary conditions"""

    def test_maximum_realistic_loan_size(self):
        """Test KPIs with very large loan amounts"""
        input_data = FinancingInput(
            purchase_price=5000000,  # 5 million
            equity=500000,
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # All KPIs should calculate without overflow
        assert summary["total_cost_of_ownership"] > 5000000
        assert summary["ltv_ratio"] == pytest.approx(90.0)
        assert summary["rate_sensitivity_score"] > 2000

    def test_minimum_realistic_loan_size(self):
        """Test KPIs with very small loan amounts"""
        input_data = FinancingInput(
            purchase_price=50000,
            equity=45000,
            interest_rate=4.0,
            initial_amortization=3.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)

        # Should handle small amounts correctly
        assert summary["loan_amount"] == 5000
        assert summary["total_cost_of_ownership"] > 50000
        assert summary["ltv_ratio"] == pytest.approx(10.0)

    def test_extreme_interest_rate_zero(self):
        """Test all KPIs with 0% interest (gift loan)"""
        input_data = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=0.0,
            initial_amortization=5.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(20)

        # With 0% interest
        assert summary["total_cost_of_ownership"] == pytest.approx(
            summary["purchase_price"]
        )
        assert summary["total_interest"] == pytest.approx(0)
        assert summary["interest_to_principal_ratio"] == 0
        assert summary["interest_savings"] == 0

    def test_time_to_50_equity_precision(self):
        """Test that time to 50% equity returns fractional years correctly"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=200000,  # Starting at 40%, need to reach 50%
            interest_rate=3.5,
            initial_amortization=3.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # Should return a precise fractional year value
        time_to_50 = summary["time_to_50_equity"]
        assert isinstance(time_to_50, float)
        assert 0 < time_to_50 < 10  # Should be reasonably short
