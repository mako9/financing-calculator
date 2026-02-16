"""
Unit tests for the FinancingCalculator module
Tests core calculation logic and financial formula accuracy
"""

import pytest
import sys
from pathlib import Path

# Add app directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from calculator import FinancingInput, YearlySchedule, FinancingCalculator


class TestFinancingInput:
    """Tests for FinancingInput dataclass"""

    def test_basic_input_creation(self):
        """Test creating a basic financing input"""
        input_data = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=4.5,
            initial_amortization=3.0,
        )
        assert input_data.purchase_price == 300000
        assert input_data.equity == 60000
        assert input_data.interest_rate == 4.5
        assert input_data.initial_amortization == 3.0
        assert input_data.annual_special_payment == 0.0
        assert input_data.interest_binding_years == 10

    def test_input_with_special_payment(self):
        """Test input with special annual payment"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=3.5,
            initial_amortization=2.0,
            annual_special_payment=5000,
            interest_binding_years=15,
        )
        assert input_data.annual_special_payment == 5000
        assert input_data.interest_binding_years == 15


class TestYearlySchedule:
    """Tests for YearlySchedule dataclass"""

    def test_schedule_entry_creation(self):
        """Test creating a yearly schedule entry"""
        schedule = YearlySchedule(
            year=1,
            debt_start=240000,
            annual_payment=18000,
            interest_payment=10800,
            amortization=7200,
            debt_end=232800,
        )
        assert schedule.year == 1
        assert schedule.debt_start == 240000
        assert schedule.annual_payment == 18000
        assert schedule.interest_payment == 10800
        assert schedule.amortization == 7200
        assert schedule.debt_end == 232800


class TestFinancingCalculator:
    """Tests for FinancingCalculator main class"""

    @pytest.fixture
    def basic_financing(self):
        """Fixture: Basic financing scenario"""
        input_data = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=4.5,
            initial_amortization=3.0,
        )
        return FinancingCalculator(input_data)

    @pytest.fixture
    def high_equity_financing(self):
        """Fixture: High equity scenario"""
        input_data = FinancingInput(
            purchase_price=400000,
            equity=160000,
            interest_rate=3.5,
            initial_amortization=2.5,
        )
        return FinancingCalculator(input_data)

    def test_loan_amount_calculation(self, basic_financing):
        """Test loan amount = purchase_price - equity"""
        assert basic_financing.loan_amount == 240000

    def test_annual_payment_calculation(self, basic_financing):
        """Test annual payment formula: loan * (interest_rate + amortization)"""
        # Expected: 240000 * (0.045 + 0.03) = 240000 * 0.075 = 18000
        assert basic_financing.annual_payment == 18000

    def test_monthly_payment_calculation(self, basic_financing):
        """Test monthly payment = annual_payment / 12"""
        expected_monthly = 18000 / 12
        assert basic_financing.monthly_payment == pytest.approx(expected_monthly)

    def test_schedule_generation_single_year(self, basic_financing):
        """Test amortization schedule for first year"""
        schedule = basic_financing.calculate_schedule(1)
        assert len(schedule) == 1

        first_year = schedule[0]
        assert first_year.year == 1
        assert first_year.debt_start == 240000

        # Interest = 240000 * 0.045 = 10800
        assert first_year.interest_payment == pytest.approx(10800)

        # Amortization = 18000 - 10800 = 7200
        assert first_year.amortization == pytest.approx(7200)

        # Debt end = 240000 - 7200 = 232800
        assert first_year.debt_end == pytest.approx(232800)

    def test_schedule_generation_multiple_years(self, basic_financing):
        """Test amortization schedule for multiple years"""
        schedule = basic_financing.calculate_schedule(5)
        assert len(schedule) == 5

        # Verify debt decreases each year
        debt_values = [entry.debt_end for entry in schedule]
        assert debt_values == sorted(debt_values, reverse=True)

        # Verify each year's calculations are consistent
        for i, entry in enumerate(schedule):
            assert entry.year == i + 1
            assert entry.annual_payment == pytest.approx(18000)

    def test_schedule_debt_progression(self, basic_financing):
        """Test that remaining debt decreases over time"""
        schedule = basic_financing.calculate_schedule(3)

        prev_debt = schedule[0].debt_end
        for entry in schedule[1:]:
            assert entry.debt_end < prev_debt
            prev_debt = entry.debt_end

    def test_schedule_with_special_payment(self):
        """Test schedule calculation with special annual payments"""
        input_data = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=4.5,
            initial_amortization=3.0,
            annual_special_payment=5000,
        )
        calc = FinancingCalculator(input_data)
        schedule = calc.calculate_schedule(2)

        # With special payment, debt should decrease faster
        assert schedule[0].amortization == pytest.approx(7200 + 5000)
        assert schedule[0].debt_end == pytest.approx(240000 - 12200)

    def test_get_summary_basic(self, basic_financing):
        """Test summary calculation"""
        summary = basic_financing.get_summary(10)

        assert summary["purchase_price"] == 300000
        assert summary["equity"] == 60000
        assert summary["loan_amount"] == 240000
        assert summary["annual_payment"] == 18000
        assert summary["monthly_payment"] == pytest.approx(1500)
        assert summary["interest_rate"] == 4.5
        assert summary["initial_amortization"] == 3.0
        assert summary["years"] == 10

    def test_summary_interest_calculation(self, basic_financing):
        """Test that total interest in summary matches schedule"""
        summary = basic_financing.get_summary(5)
        schedule = basic_financing.calculate_schedule(5)

        total_interest_from_schedule = sum(entry.interest_payment for entry in schedule)
        assert summary["total_interest"] == pytest.approx(total_interest_from_schedule)

    def test_summary_amortization_calculation(self, basic_financing):
        """Test that total amortization in summary matches schedule"""
        summary = basic_financing.get_summary(5)
        schedule = basic_financing.calculate_schedule(5)

        total_amort_from_schedule = sum(entry.amortization for entry in schedule)
        assert summary["total_amortization"] == pytest.approx(total_amort_from_schedule)

    def test_schedule_to_dataframe(self, basic_financing):
        """Test conversion of schedule to pandas DataFrame"""
        schedule = basic_financing.calculate_schedule(2)
        df = basic_financing.schedule_to_dataframe()

        assert len(df) == 2
        assert "Jahr" in df.columns
        assert "Restschuld Anfang (€)" in df.columns
        assert "Zinsanteil (€)" in df.columns
        assert "Tilgung (€)" in df.columns
        assert "Restschuld Ende (€)" in df.columns

    def test_dataframe_values_match_schedule(self, basic_financing):
        """Test that DataFrame values match schedule entries"""
        schedule = basic_financing.calculate_schedule(3)
        df = basic_financing.schedule_to_dataframe()

        for idx, entry in enumerate(schedule):
            assert df.iloc[idx]["Jahr"] == entry.year
            assert df.iloc[idx]["Restschuld Anfang (€)"] == pytest.approx(
                entry.debt_start
            )
            assert df.iloc[idx]["Zinsanteil (€)"] == pytest.approx(
                entry.interest_payment
            )

    def test_high_equity_lower_loan(self, high_equity_financing):
        """Test financing with high equity"""
        assert high_equity_financing.loan_amount == 240000  # 400000 - 160000

    def test_lower_interest_rate_less_interest(self, high_equity_financing):
        """Test that lower interest rates result in less interest payment"""
        schedule = high_equity_financing.calculate_schedule(1)

        # At 3.5% interest on 240000: 240000 * 0.035 = 8400
        assert schedule[0].interest_payment == pytest.approx(8400)

    def test_schedule_multiple_calls_consistency(self, basic_financing):
        """Test that multiple calls to calculate_schedule are consistent"""
        schedule1 = basic_financing.calculate_schedule(5)
        summary1 = basic_financing.get_summary(5)

        # Call again with different years
        basic_financing.calculate_schedule(3)
        schedule2 = basic_financing.calculate_schedule(5)
        summary2 = basic_financing.get_summary(5)

        # Results should be identical
        assert len(schedule1) == len(schedule2)
        assert summary1["total_interest"] == pytest.approx(summary2["total_interest"])


class TestFinancialAccuracy:
    """Integration tests for financial calculation accuracy"""

    def test_payment_matching_annual_payments(self):
        """
        Test that total principal equals sum of amortization payments
        purchase_price = equity + total_amortization + total_interest
        """
        input_data = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=4.5,
            initial_amortization=3.0,
        )
        calc = FinancingCalculator(input_data)
        summary = calc.get_summary(30)

        # After 30 years with 3% amortization + 4.5% interest, loan should be mostly paid
        # Check that remaining debt is less than initial loan amount
        assert summary["remaining_debt"] < summary["loan_amount"]
        # Total payments should equal loan + all interest paid
        total_paid = summary["years"] * summary["annual_payment"]
        assert total_paid > summary["loan_amount"]  # Should pay more due to interest

    def test_annual_rate_calculation_consistency(self):
        """Test that interest rate is consistently applied"""
        input_data = FinancingInput(
            purchase_price=500000,
            equity=100000,
            interest_rate=5.0,
            initial_amortization=2.0,
        )
        calc = FinancingCalculator(input_data)
        schedule = calc.calculate_schedule(1)

        loan = 400000
        interest_rate = 0.05

        # Year 1 interest should be: loan_amount * rate
        expected_interest = loan * interest_rate
        assert schedule[0].interest_payment == pytest.approx(expected_interest)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def test_zero_interest_rate(self):
        """Test calculation with 0% interest rate"""
        input_data = FinancingInput(
            purchase_price=100000,
            equity=20000,
            interest_rate=0.0,
            initial_amortization=5.0,
        )
        calc = FinancingCalculator(input_data)
        schedule = calc.calculate_schedule(5)

        # With 0% interest, all payments go to amortization
        for entry in schedule:
            assert entry.interest_payment == pytest.approx(0)
            assert entry.amortization > 0

    def test_high_interest_rate(self):
        """Test calculation with high interest rate"""
        input_data = FinancingInput(
            purchase_price=200000,
            equity=40000,
            interest_rate=10.0,
            initial_amortization=1.0,
        )
        calc = FinancingCalculator(input_data)
        schedule = calc.calculate_schedule(1)

        # High interest rate should result in high interest payment
        expected_interest = 160000 * 0.10
        assert schedule[0].interest_payment == pytest.approx(expected_interest)

    def test_full_equity_no_loan(self):
        """Test scenario where purchase price equals equity (no loan)"""
        input_data = FinancingInput(
            purchase_price=100000,
            equity=100000,
            interest_rate=4.5,
            initial_amortization=3.0,
        )
        calc = FinancingCalculator(input_data)

        assert calc.loan_amount == 0
        assert calc.annual_payment == 0
        assert calc.monthly_payment == 0

    def test_small_loan_amount(self):
        """Test very small loan amount"""
        input_data = FinancingInput(
            purchase_price=10000,
            equity=9000,
            interest_rate=4.5,
            initial_amortization=3.0,
        )
        calc = FinancingCalculator(input_data)
        schedule = calc.calculate_schedule(5)

        # Should still calculate correctly
        assert len(schedule) == 5
        assert schedule[0].interest_payment > 0


class TestCalculateYearsToPayoff:
    """Tests for the calculate_years_to_payoff reverse calculation method"""

    @pytest.fixture
    def basic_financing(self):
        """Fixture: Basic financing scenario"""
        input_data = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=4.5,
            initial_amortization=3.0,
        )
        return FinancingCalculator(input_data)

    def test_years_to_payoff_reasonable_payment(self, basic_financing):
        """Test payoff calculation with reasonable monthly payment"""
        result = basic_financing.calculate_years_to_payoff(2000)  # €2000/month

        assert result["feasible"] is True
        assert result["years_to_payoff"] is not None
        assert result["years_to_payoff"] > 0
        assert result["total_interest"] is not None
        assert result["total_interest"] >= 0
        assert result["monthly_payment"] == 2000
        assert result["remaining_debt"] == pytest.approx(0, abs=1)

    def test_years_to_payoff_high_payment(self, basic_financing):
        """Test payoff with very high monthly payment"""
        result = basic_financing.calculate_years_to_payoff(5000)

        assert result["feasible"] is True
        assert result["years_to_payoff"] is not None
        assert result["years_to_payoff"] > 0
        # Higher payment should result in fewer years
        assert result["years_to_payoff"] < 10

    def test_years_to_payoff_zero_payment(self, basic_financing):
        """Test that zero payment is rejected"""
        result = basic_financing.calculate_years_to_payoff(0)

        assert result["feasible"] is False
        assert result["years_to_payoff"] == 0
        assert result["error"] == "Payment must be positive"
        assert result["remaining_debt"] == 240000

    def test_years_to_payoff_negative_payment(self, basic_financing):
        """Test that negative payment is rejected"""
        result = basic_financing.calculate_years_to_payoff(-1000)

        assert result["feasible"] is False
        assert result["years_to_payoff"] == 0
        assert result["error"] == "Payment must be positive"

    def test_years_to_payoff_insufficient_payment(self, basic_financing):
        """Test payment that doesn't cover interest"""
        # At 4.5% interest on 240000, monthly interest is ~900
        # So paying 500/month is insufficient
        result = basic_financing.calculate_years_to_payoff(500)

        assert result["feasible"] is False
        assert result["years_to_payoff"] is None
        assert "insufficient to cover interest" in result["error"]

    def test_years_to_payoff_barely_sufficient_payment(self, basic_financing):
        """Test payment barely sufficient to cover interest"""
        # Loan: 240000 at 4.5% annual = 10800 annual = 900/month interest
        result = basic_financing.calculate_years_to_payoff(901)

        assert result["feasible"] is True
        assert result["years_to_payoff"] is not None
        assert result["years_to_payoff"] > 0

    def test_years_to_payoff_return_contains_required_fields(self, basic_financing):
        """Test that return dict contains all required fields when feasible"""
        result = basic_financing.calculate_years_to_payoff(2000)

        required_fields = [
            "years_to_payoff",
            "total_interest",
            "remaining_debt",
            "monthly_payment",
            "annual_payment",
            "feasible",
            "loan_amount",
            "interest_rate",
        ]
        for field in required_fields:
            assert field in result

    def test_years_to_payoff_consistency_with_schedule(self, basic_financing):
        """Test that calculated payoff is consistent with actual schedule"""
        monthly_payment = 2000
        result = basic_financing.calculate_years_to_payoff(monthly_payment)
        years_calculated = result["years_to_payoff"]

        # Generate schedule for the calculated years
        schedule = basic_financing.calculate_schedule(years_calculated)
        final_debt = schedule[-1].debt_end

        # Remaining debt should be very small (nearly paid off)
        assert final_debt < 100  # Less than €100 remaining

    def test_years_to_payoff_different_interest_rates(self):
        """Test payoff calculation with different interest rates"""
        # Lower interest rate
        input_low = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=2.0,
            initial_amortization=3.0,
        )
        calc_low = FinancingCalculator(input_low)
        result_low = calc_low.calculate_years_to_payoff(2000)

        # Higher interest rate
        input_high = FinancingInput(
            purchase_price=300000,
            equity=60000,
            interest_rate=6.0,
            initial_amortization=3.0,
        )
        calc_high = FinancingCalculator(input_high)
        result_high = calc_high.calculate_years_to_payoff(2000)

        # Higher interest rate should require more years to pay off
        assert result_high["years_to_payoff"] > result_low["years_to_payoff"]
        assert result_high["total_interest"] > result_low["total_interest"]

    def test_years_to_payoff_small_loan(self):
        """Test payoff calculation for small loan"""
        input_data = FinancingInput(
            purchase_price=50000,
            equity=40000,
            interest_rate=4.5,
            initial_amortization=3.0,
        )
        calc = FinancingCalculator(input_data)
        result = calc.calculate_years_to_payoff(500)

        assert result["feasible"] is True
        assert result["years_to_payoff"] is not None
        assert result["years_to_payoff"] > 0
        assert result["loan_amount"] == 10000

    def test_years_to_payoff_large_loan(self):
        """Test payoff calculation for large loan"""
        input_data = FinancingInput(
            purchase_price=1000000,
            equity=100000,
            interest_rate=4.5,
            initial_amortization=3.0,
        )
        calc = FinancingCalculator(input_data)
        result = calc.calculate_years_to_payoff(6000)

        assert result["feasible"] is True
        assert result["years_to_payoff"] is not None
        assert result["loan_amount"] == 900000

    def test_years_to_payoff_fractional_months(self, basic_financing):
        """Test that payoff handles cases requiring multiple years"""
        # Small payment relative to loan
        result = basic_financing.calculate_years_to_payoff(1500)

        assert result["feasible"] is True
        assert result["years_to_payoff"] > 10
        assert isinstance(result["years_to_payoff"], int)

    def test_years_to_payoff_debt_decreasing(self, basic_financing):
        """Test that decreasing monthly payment reduces years needed"""
        result_high = basic_financing.calculate_years_to_payoff(2500)
        result_low = basic_financing.calculate_years_to_payoff(1500)

        assert result_high["feasible"] is True
        assert result_low["feasible"] is True
        # Higher payment should result in fewer years
        assert result_high["years_to_payoff"] < result_low["years_to_payoff"]

    def test_years_to_payoff_with_zero_interest(self):
        """Test payoff with 0% interest rate"""
        input_data = FinancingInput(
            purchase_price=100000,
            equity=20000,
            interest_rate=0.0,
            initial_amortization=5.0,
        )
        calc = FinancingCalculator(input_data)
        result = calc.calculate_years_to_payoff(1000)

        # With 0% interest, 80000 / 12000 annual = ~6.67 years = 7 years
        assert result["feasible"] is True
        assert result["total_interest"] == pytest.approx(0)
        assert result["years_to_payoff"] == 7

    def test_years_to_payoff_exact_annual_payment(self, basic_financing):
        """Test payoff with exact annual payment as monthly"""
        # Basic financing annual payment is 18000
        # So monthly is 1500
        result = basic_financing.calculate_years_to_payoff(1500)

        assert result["feasible"] is True
        assert result["years_to_payoff"] is not None

    def test_years_to_payoff_error_field_when_infeasible(self, basic_financing):
        """Test that error field exists when calculation is infeasible"""
        result = basic_financing.calculate_years_to_payoff(500)

        assert result["feasible"] is False
        assert "error" in result
        assert len(result["error"]) > 0
