"""
Comprehensive Integration Tests for All KPIs
Tests high-priority, medium-priority, and low-priority KPIs together
Validates edge cases, bilingual support, and UI integration
"""

import pytest
import sys
from pathlib import Path

# Add app directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from calculator import FinancingCalculator, FinancingInput
from translations import get_text


class TestHighPriorityKPIs:
    """Integration tests for high-priority KPIs"""

    @pytest.fixture
    def standard_financing(self):
        """Standard financing scenario for testing"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=5000,
        )
        return FinancingCalculator(input_data)

    def test_total_cost_of_ownership_calculation(self, standard_financing):
        """Test Total Cost of Ownership = Purchase Price + Total Interest"""
        summary = standard_financing.get_summary(30)

        expected_tco = summary["purchase_price"] + summary["total_interest"]
        assert summary["total_cost_of_ownership"] == pytest.approx(expected_tco)
        # TCO should always be higher than purchase price (unless 0% interest)
        assert summary["total_cost_of_ownership"] > summary["purchase_price"]

    def test_interest_to_principal_ratio(self, standard_financing):
        """Test Interest-to-Principal Ratio"""
        summary = standard_financing.get_summary(30)

        # Ratio should be total_interest / total_amortization
        expected_ratio = summary["total_interest"] / summary["total_amortization"]
        assert summary["interest_to_principal_ratio"] == pytest.approx(expected_ratio)
        # Ratio should be positive
        assert summary["interest_to_principal_ratio"] > 0

    def test_ltv_ratio_calculation(self, standard_financing):
        """Test LTV (Loan-to-Value) Ratio"""
        summary = standard_financing.get_summary(30)

        # LTV = (Loan Amount / Purchase Price) × 100
        expected_ltv = (
            summary["loan_amount"] / summary["purchase_price"]
        ) * 100
        assert summary["ltv_ratio"] == pytest.approx(expected_ltv)
        # LTV should be between 0 and 100
        assert 0 <= summary["ltv_ratio"] <= 100

    def test_interest_savings_from_special_payments(self, standard_financing):
        """Test Interest Savings calculation with special payments"""
        summary = standard_financing.get_summary(30)

        # Savings should be positive when making special payments
        assert summary["interest_savings"] > 0
        assert summary["time_saved_years"] > 0
        # Interest with special payments should be less than without
        assert summary["interest_with_special"] < summary["interest_without_special"]

    def test_interest_savings_zero_special_payment(self):
        """Test Interest Savings when no special payments are made"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=0,  # No special payment
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # All savings should be zero
        assert summary["interest_savings"] == 0
        assert summary["time_saved_years"] == 0
        assert summary["interest_with_special"] == 0
        assert summary["interest_without_special"] == 0


class TestMediumPriorityKPIs:
    """Integration tests for medium-priority KPIs"""

    @pytest.fixture
    def standard_financing(self):
        """Standard financing scenario for testing"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        return FinancingCalculator(input_data)

    def test_breakeven_point_calculation(self, standard_financing):
        """Test Breakeven Point - when cumulative amortization > cumulative interest"""
        summary = standard_financing.get_summary(40)

        # Breakeven year should be present and reasonable
        assert summary["breakeven_year"] is not None
        assert summary["breakeven_year"] > 0
        # Should occur within the loan period
        payoff_years = standard_financing.calculate_payoff_years()
        assert summary["breakeven_year"] <= payoff_years

    def test_breakeven_point_never_reached(self):
        """Test breakeven point when it's never reached (very low amortization)"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=5.0,
            initial_amortization=0.5,  # Very low amortization
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(10)  # Look at only first 10 years

        # Breakeven might not be reached in 10 years with such low amortization
        # If not reached, breakeven_year will be None
        if summary["breakeven_year"] is None:
            assert summary["cumulative_amortization_at_breakeven"] > 0
            assert summary["cumulative_interest_at_breakeven"] > 0

    def test_equity_buildup_rate_progression(self, standard_financing):
        """Test Equity Buildup Rate - year-by-year equity progression"""
        summary = standard_financing.get_summary(30)

        equity_buildup = summary["equity_buildup_rate"]

        # Should have entries for each year
        assert len(equity_buildup) > 0

        # Verify structure of each entry
        for entry in equity_buildup:
            assert "year" in entry
            assert "equity_gained" in entry
            assert "equity_percentage" in entry
            assert "cumulative_equity" in entry
            # All values should be positive
            assert entry["equity_gained"] >= 0
            assert entry["equity_percentage"] >= 0
            assert entry["cumulative_equity"] >= 0

        # Equity percentage should be increasing
        percentages = [e["equity_percentage"] for e in equity_buildup]
        assert percentages == sorted(percentages)

    def test_equity_buildup_reaches_100_percent(self):
        """Test that equity buildup eventually reaches 100%"""
        input_data = FinancingInput(
            purchase_price=200000,
            equity=50000,
            interest_rate=4.0,
            initial_amortization=5.0,  # High amortization for faster payoff
        )
        calc = FinancingCalculator(input_data)
        payoff_years = calc.calculate_payoff_years()
        summary = calc.get_summary(payoff_years)

        equity_buildup = summary["equity_buildup_rate"]

        # Last entry should be close to 100%
        if equity_buildup:
            final_equity_pct = equity_buildup[-1]["equity_percentage"]
            assert final_equity_pct >= 99  # Allow small rounding tolerance


class TestLowPriorityKPIs:
    """Integration tests for low-priority KPIs (already tested, but verify integration)"""

    @pytest.fixture
    def standard_financing(self):
        """Standard financing scenario for testing"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        return FinancingCalculator(input_data)

    def test_all_low_priority_kpis_present(self, standard_financing):
        """Verify all low-priority KPIs are in summary"""
        summary = standard_financing.get_summary(30)

        assert "buffer_ratio" in summary
        assert "time_to_50_equity" in summary
        assert "rate_sensitivity_score" in summary


class TestKPIEdgeCases:
    """Test edge cases across all KPIs"""

    def test_zero_equity_scenario(self):
        """Test all KPIs with zero equity (100% financing)"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=0,  # 100% financing
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # High-priority KPIs
        assert summary["total_cost_of_ownership"] > summary["purchase_price"]
        assert summary["ltv_ratio"] == pytest.approx(100.0)
        assert summary["interest_to_principal_ratio"] > 0

        # Low-priority KPIs
        assert summary["buffer_ratio"] == 0  # Division by zero handled
        assert summary["time_to_50_equity"] > 0
        assert summary["rate_sensitivity_score"] > 0

    def test_full_equity_scenario(self):
        """Test all KPIs with full equity (no loan)"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=500000,  # 100% equity
            interest_rate=4.0,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(1)

        # High-priority KPIs
        assert summary["total_cost_of_ownership"] == summary["purchase_price"]
        assert summary["ltv_ratio"] == 0
        assert summary["interest_to_principal_ratio"] == 0

        # Low-priority KPIs
        assert summary["rate_sensitivity_score"] == 0  # No loan, no sensitivity
        assert summary["time_to_50_equity"] <= 1  # Already above 50%

    def test_very_high_interest_rate(self):
        """Test KPIs with very high interest rate"""
        input_data = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=10.0,  # Very high rate
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # High interest should result in high total cost
        assert summary["total_cost_of_ownership"] > summary["purchase_price"] * 1.5
        # High interest-to-principal ratio
        assert summary["interest_to_principal_ratio"] > 0.5

    def test_zero_interest_rate(self):
        """Test KPIs with zero interest rate"""
        input_data = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=0.0,  # No interest
            initial_amortization=5.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # Zero interest means TCO = purchase price
        assert summary["total_cost_of_ownership"] == pytest.approx(
            summary["purchase_price"]
        )
        assert summary["total_interest"] == pytest.approx(0)
        assert summary["interest_to_principal_ratio"] == 0


class TestBilingualSupport:
    """Test that all KPI translations exist in both languages"""

    def test_all_kpi_translations_english(self):
        """Verify all KPI translation keys exist in English"""
        required_keys = [
            # High-priority KPIs
            "total_cost_of_ownership",
            "interest_to_principal_ratio",
            "ltv_ratio",
            "interest_savings",
            "interest_without_special",
            "interest_with_special",
            "time_saved",
            # Medium-priority KPIs
            "breakeven_year",
            "breakeven_milestone",
            "equity_buildup",
            "equity_buildup_progression",
            # Low-priority KPIs
            "buffer_ratio",
            "buffer_ratio_desc",
            "time_to_50_equity",
            "time_to_50_equity_desc",
            "rate_sensitivity_score",
            "rate_sensitivity_desc",
            # Other related keys
            "kpis",
            "risk_analysis",
            "months",
        ]

        for key in required_keys:
            translation = get_text("en", key)
            assert translation is not None
            # Note: Some keys like "months" return themselves in English, which is valid
            assert len(translation) > 0

    def test_all_kpi_translations_german(self):
        """Verify all KPI translation keys exist in German"""
        required_keys = [
            # High-priority KPIs
            "total_cost_of_ownership",
            "interest_to_principal_ratio",
            "ltv_ratio",
            "interest_savings",
            "interest_without_special",
            "interest_with_special",
            "time_saved",
            # Medium-priority KPIs
            "breakeven_year",
            "breakeven_milestone",
            "equity_buildup",
            "equity_buildup_progression",
            # Low-priority KPIs
            "buffer_ratio",
            "buffer_ratio_desc",
            "time_to_50_equity",
            "time_to_50_equity_desc",
            "rate_sensitivity_score",
            "rate_sensitivity_desc",
            # Other related keys
            "kpis",
            "risk_analysis",
            "months",
        ]

        for key in required_keys:
            translation = get_text("de", key)
            assert translation is not None
            assert translation != key  # Should not return the key itself
            assert len(translation) > 0

    def test_translations_are_different_languages(self):
        """Verify English and German translations are actually different"""
        keys_to_check = [
            "total_cost_of_ownership",
            "interest_to_principal_ratio",
            "ltv_ratio",
            "breakeven_milestone",
            "equity_buildup_progression",
            "buffer_ratio",
            "time_to_50_equity",
            "rate_sensitivity_score",
        ]

        for key in keys_to_check:
            en_text = get_text("en", key)
            de_text = get_text("de", key)
            # Texts should be different (different languages)
            assert en_text != de_text, f"Translation for '{key}' is same in both languages"


class TestUIIntegration:
    """Test that KPIs integrate properly with UI components"""

    def test_kpis_in_summary_dict(self):
        """Verify all KPIs are included in summary dictionary"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=5000,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # High-priority KPIs
        assert "total_cost_of_ownership" in summary
        assert "interest_to_principal_ratio" in summary
        assert "ltv_ratio" in summary
        assert "interest_savings" in summary
        assert "interest_without_special" in summary
        assert "interest_with_special" in summary
        assert "time_saved_years" in summary

        # Medium-priority KPIs
        assert "breakeven_year" in summary
        assert "cumulative_amortization_at_breakeven" in summary
        assert "cumulative_interest_at_breakeven" in summary
        assert "equity_buildup_rate" in summary

        # Low-priority KPIs
        assert "buffer_ratio" in summary
        assert "time_to_50_equity" in summary
        assert "rate_sensitivity_score" in summary

    def test_kpi_values_are_serializable(self):
        """Verify all KPI values can be serialized to JSON (for UI)"""
        import json

        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=5000,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # Remove equity_buildup_rate temporarily for basic serialization test
        equity_buildup = summary.pop("equity_buildup_rate")

        # Should be able to serialize to JSON without errors
        try:
            json_str = json.dumps(summary)
            assert len(json_str) > 0
        except (TypeError, ValueError) as e:
            pytest.fail(f"Summary values are not JSON serializable: {e}")

        # Test equity_buildup_rate separately
        try:
            equity_json = json.dumps(equity_buildup)
            assert len(equity_json) > 0
        except (TypeError, ValueError) as e:
            pytest.fail(f"Equity buildup rate is not JSON serializable: {e}")

    def test_kpi_metric_box_data_format(self):
        """Test that KPI data is formatted correctly for metric boxes"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # Verify numeric KPIs are numbers (not strings)
        assert isinstance(summary["total_cost_of_ownership"], (int, float))
        assert isinstance(summary["interest_to_principal_ratio"], (int, float))
        assert isinstance(summary["ltv_ratio"], (int, float))
        assert isinstance(summary["buffer_ratio"], (int, float))
        assert isinstance(summary["time_to_50_equity"], (int, float))
        assert isinstance(summary["rate_sensitivity_score"], (int, float))


class TestKPICalculationConsistency:
    """Test that KPI calculations are consistent across multiple calls"""

    def test_kpis_deterministic(self):
        """Verify KPIs return same values on repeated calls"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=5000,
        )

        # Calculate multiple times
        calc1 = FinancingCalculator(input_data)
        summary1 = calc1.get_summary(30)

        calc2 = FinancingCalculator(input_data)
        summary2 = calc2.get_summary(30)

        calc3 = FinancingCalculator(input_data)
        summary3 = calc3.get_summary(30)

        # All KPIs should be identical
        assert summary1["total_cost_of_ownership"] == pytest.approx(
            summary2["total_cost_of_ownership"]
        )
        assert summary2["total_cost_of_ownership"] == pytest.approx(
            summary3["total_cost_of_ownership"]
        )

        assert summary1["ltv_ratio"] == pytest.approx(summary2["ltv_ratio"])
        assert summary1["breakeven_year"] == summary2["breakeven_year"]
        assert summary1["buffer_ratio"] == pytest.approx(summary2["buffer_ratio"])

    def test_kpis_recalculate_with_different_years(self):
        """Test that KPIs are recalculated correctly when years parameter changes"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)

        summary_10y = calc.get_summary(10)
        summary_20y = calc.get_summary(20)
        summary_30y = calc.get_summary(30)

        # Total interest should increase with more years
        assert summary_10y["total_interest"] < summary_20y["total_interest"]
        assert summary_20y["total_interest"] < summary_30y["total_interest"]

        # Total cost of ownership should increase with more years
        assert (
            summary_10y["total_cost_of_ownership"]
            < summary_20y["total_cost_of_ownership"]
        )


class TestKPIRealisticValues:
    """Test that KPI values are within realistic bounds"""

    def test_realistic_financing_scenario(self):
        """Test KPIs with realistic German mortgage scenario"""
        input_data = FinancingInput(
            purchase_price=400000,
            equity=50000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=2000,
            interest_binding_years=10,
        )
        calc = FinancingCalculator(input_data)
        payoff_years = calc.calculate_payoff_years()
        summary = calc.get_summary(payoff_years)

        # High-priority KPIs - realistic ranges
        assert 400000 < summary["total_cost_of_ownership"] < 800000
        assert 0 < summary["interest_to_principal_ratio"] < 1.0
        assert 80 < summary["ltv_ratio"] < 90  # 87.5% for this scenario
        assert summary["interest_savings"] > 0

        # Medium-priority KPIs
        assert 5 < summary["breakeven_year"] < payoff_years
        assert len(summary["equity_buildup_rate"]) > 0

        # Low-priority KPIs
        assert 0 < summary["buffer_ratio"] < 10
        assert 5 < summary["time_to_50_equity"] < payoff_years
        assert 50 < summary["rate_sensitivity_score"] < 500
