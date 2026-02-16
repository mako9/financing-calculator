"""
Financing Calculator Module
Calculates loan amortization schedules and financing summaries
"""

from dataclasses import dataclass
from typing import List
import pandas as pd


@dataclass
class FinancingInput:
    """Input parameters for financing calculation"""

    purchase_price: float
    equity: float
    interest_rate: float  # Annual, in percent
    initial_amortization: float  # Initial, in percent
    annual_special_payment: float = 0.0
    interest_binding_years: int = 10


@dataclass
class YearlySchedule:
    """Yearly amortization schedule entry"""

    year: int
    debt_start: float
    annual_payment: float
    interest_payment: float
    amortization: float
    debt_end: float


class FinancingCalculator:
    """Calculator for property financing with amortization schedules"""

    def __init__(self, input_data: FinancingInput):
        self.input = input_data
        self.loan_amount = input_data.purchase_price - input_data.equity
        self.annual_payment = self._calculate_annual_payment()
        self.monthly_payment = self.annual_payment / 12
        self.schedule: List[YearlySchedule] = []

    def _calculate_annual_payment(self) -> float:
        """Calculate annual payment based on initial amortization and interest rate"""
        rate = self.input.interest_rate / 100
        return self.loan_amount * (rate + self.input.initial_amortization / 100)

    def calculate_schedule(self, years: int) -> List[YearlySchedule]:
        """Generate amortization schedule for given number of years"""
        self.schedule = []
        remaining_debt = self.loan_amount

        for year in range(1, years + 1):
            debt_start = remaining_debt
            rate = self.input.interest_rate / 100

            # Interest for this year
            interest = debt_start * rate

            # Amortization = Annual payment - Interest + Special payment
            amortization = (
                self.annual_payment - interest + self.input.annual_special_payment
            )

            # New debt
            debt_end = debt_start - amortization

            schedule_entry = YearlySchedule(
                year=year,
                debt_start=debt_start,
                annual_payment=self.annual_payment,
                interest_payment=interest,
                amortization=amortization,
                debt_end=debt_end,
            )
            self.schedule.append(schedule_entry)
            remaining_debt = debt_end

        return self.schedule

    def get_summary(self, years: int) -> dict:
        """Get summary statistics for the financing"""
        if not self.schedule:
            self.calculate_schedule(years)

        if years > len(self.schedule):
            self.calculate_schedule(years)

        total_interest = sum(item.interest_payment for item in self.schedule[:years])
        total_amortization = sum(item.amortization for item in self.schedule[:years])
        remaining_debt = (
            self.schedule[years - 1].debt_end if years <= len(self.schedule) else 0
        )

        return {
            "purchase_price": self.input.purchase_price,
            "equity": self.input.equity,
            "loan_amount": self.loan_amount,
            "annual_payment": self.annual_payment,
            "monthly_payment": self.monthly_payment,
            "interest_rate": self.input.interest_rate,
            "initial_amortization": self.input.initial_amortization,
            "total_interest": total_interest,
            "total_amortization": total_amortization,
            "remaining_debt": remaining_debt,
            "years": years,
        }

    def schedule_to_dataframe(self) -> pd.DataFrame:
        """Convert schedule to pandas DataFrame for display"""
        if not self.schedule:
            return pd.DataFrame()

        data = {
            "Jahr": [item.year for item in self.schedule],
            "Restschuld Anfang (€)": [item.debt_start for item in self.schedule],
            "Jahresrate (€)": [item.annual_payment for item in self.schedule],
            "Zinsanteil (€)": [item.interest_payment for item in self.schedule],
            "Tilgung (€)": [item.amortization for item in self.schedule],
            "Restschuld Ende (€)": [item.debt_end for item in self.schedule],
        }
        return pd.DataFrame(data)

    def calculate_years_to_payoff(self, affordable_monthly_payment: float) -> dict:
        """
        Calculate how many years needed to pay off loan given an affordable monthly payment.
        This is a reverse calculation for affordability analysis.

        Args:
            affordable_monthly_payment: Maximum affordable monthly payment (€)

        Returns:
            Dictionary with payoff analysis including years needed and total interest
        """
        if affordable_monthly_payment <= 0:
            return {
                "years_to_payoff": 0,
                "total_interest": 0,
                "remaining_debt": self.loan_amount,
                "monthly_payment": 0,
                "feasible": False,
                "error": "Payment must be positive",
            }

        remaining_debt = self.loan_amount
        annual_payment = affordable_monthly_payment * 12
        rate = self.input.interest_rate / 100
        total_interest = 0
        years = 0
        max_years = 500  # Prevent infinite loops

        # Simulate payoff year by year
        while remaining_debt > 0 and years < max_years:
            years += 1
            debt_start = remaining_debt

            # Calculate interest on current debt
            interest = debt_start * rate
            total_interest += interest

            # Annual special payment from input
            special_payment = self.input.annual_special_payment

            # Amortization = Annual payment - Interest + Special payment
            # (Special payment increases principal repayment)
            amortization = annual_payment - interest + special_payment

            # If amortization is not positive, payment doesn't cover interest
            if amortization <= 0:
                return {
                    "years_to_payoff": None,
                    "total_interest": None,
                    "remaining_debt": self.loan_amount,
                    "monthly_payment": affordable_monthly_payment,
                    "feasible": False,
                    "error": f"Monthly payment €{affordable_monthly_payment:.2f} insufficient to cover interest",
                }

            # Ensure we don't amortize more than remaining debt
            if amortization > remaining_debt:
                amortization = remaining_debt

            # New debt after principal repayment
            debt_end = debt_start - amortization

            # Update remaining debt
            remaining_debt = debt_end

            # Stop if debt is essentially paid
            if remaining_debt < 1:
                remaining_debt = 0
                break

        if years >= max_years:
            return {
                "years_to_payoff": None,
                "total_interest": None,
                "remaining_debt": remaining_debt,
                "monthly_payment": affordable_monthly_payment,
                "feasible": False,
                "error": "Loan would take too long to pay off with this payment",
            }

        # Persist the payment used for this payoff calculation so
        # subsequent schedule generation uses the same payment.
        self.annual_payment = annual_payment
        self.monthly_payment = affordable_monthly_payment

        return {
            "years_to_payoff": years,
            "total_interest": total_interest,
            "remaining_debt": max(0, remaining_debt),
            "monthly_payment": affordable_monthly_payment,
            "annual_payment": annual_payment,
            "feasible": True,
            "loan_amount": self.loan_amount,
            "interest_rate": self.input.interest_rate,
        }
