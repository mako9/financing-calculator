"""
Callbacks for Financing Calculator
Handles all Dash callbacks for user interactions and data updates
"""

from dash import Input, Output, State, dcc, html
from calculator import FinancingCalculator, FinancingInput
from components import create_card, create_metric_box, create_table
from config import COLORS
from translations import get_text
from charts import (
    create_debt_development_chart,
    create_interest_vs_amortization_chart,
    create_cost_distribution_pie_chart,
    create_interest_curve_chart,
    create_cumulative_progress_chart,
)


def register_callbacks(app):
    """Register all Dash callbacks with the app"""

    @app.callback(
        Output("language-store", "data"),
        [Input("lang-de-btn", "n_clicks"), Input("lang-en-btn", "n_clicks")],
        prevent_initial_call=False,
    )
    def switch_language(de_clicks, en_clicks):
        """Handle language toggle button clicks"""
        if de_clicks > en_clicks:
            return "de"
        else:
            return "en"

    @app.callback(
        [
            Output("lang-de-btn", "style"),
            Output("lang-en-btn", "style"),
        ],
        Input("language-store", "data"),
    )
    def update_language_button_styles(lang):
        """Update button styles to show which language is selected"""
        de_style = {
            "padding": "0.5rem 1rem",
            "backgroundColor": COLORS["primary"] if lang == "de" else "white",
            "color": "white" if lang == "de" else COLORS["primary"],
            "border": f"2px solid {COLORS['primary']}",
            "borderRadius": "6px",
            "cursor": "pointer",
            "marginRight": "0.5rem",
            "fontWeight": "600",
        }
        en_style = {
            "padding": "0.5rem 1rem",
            "backgroundColor": COLORS["primary"] if lang == "en" else "white",
            "color": "white" if lang == "en" else COLORS["primary"],
            "border": f"2px solid {COLORS['primary']}",
            "borderRadius": "6px",
            "cursor": "pointer",
            "fontWeight": "600",
        }
        return de_style, en_style

    @app.callback(
        [
            Output("purchase-price-label", "children"),
            Output("equity-label", "children"),
            Output("interest-rate-label", "children"),
            Output("initial-amort-label", "children"),
            Output("interest-binding-label", "children"),
            Output("special-payment-label", "children"),
            Output("input-params-title", "children"),
        ],
        Input("language-store", "data"),
    )
    def update_input_labels(lang):
        """Update all input parameter labels when language changes"""
        t = lambda key: get_text(lang, key)
        return (
            t("purchase_price"),
            t("equity"),
            t("interest_rate"),
            t("initial_amortization"),
            t("interest_binding"),
            t("special_payment"),
            f"📋 {t('input_params')}",
        )

    @app.callback(
        Output("years_value", "children"),
        Input("years_to_show", "value"),
    )
    def update_years_display(years):
        """Update the displayed years value from the slider"""
        return str(years)

    @app.callback(
        [
            Output("summary_cards", "children"),
            Output("key_metrics", "children"),
            Output("table_container", "children"),
            Output("debt_chart", "figure"),
            Output("interest_amortization_chart", "figure"),
            Output("pie_chart", "figure"),
            Output("interest_curve_chart", "figure"),
            Output("interest_development_chart", "figure"),
        ],
        [
            Input("purchase_price", "value"),
            Input("equity", "value"),
            Input("interest_rate", "value"),
            Input("initial_amortization", "value"),
            Input("interest_binding_years", "value"),
            Input("annual_special_payment", "value"),
            Input("years_to_show", "value"),
            Input("language-store", "data"),
        ],
    )
    def update_calculations(
        purchase_price,
        equity,
        interest_rate,
        initial_amortization,
        interest_binding_years,
        annual_special_payment,
        years_to_show,
        lang,
    ):
        """Main calculation callback - updates all visualizations and summary data"""
        t = lambda key: get_text(lang, key)

        try:
            # Create input data object
            input_data = FinancingInput(
                purchase_price=purchase_price or 0,
                equity=equity or 0,
                interest_rate=interest_rate or 0,
                initial_amortization=initial_amortization or 0,
                annual_special_payment=annual_special_payment or 0,
                interest_binding_years=interest_binding_years or 10,
            )

            # Perform calculations
            calculator = FinancingCalculator(input_data)
            schedule = calculator.calculate_schedule(years_to_show or 10)
            summary = calculator.get_summary(years_to_show or 10)
            df = calculator.schedule_to_dataframe()

            # Rename columns based on language
            if lang == "de":
                df.columns = [
                    "Jahr",
                    "Restschuld Anfang (€)",
                    "Jahresrate (€)",
                    "Zinsanteil (€)",
                    "Tilgung (€)",
                    "Restschuld Ende (€)",
                ]
            else:
                df.columns = [
                    "Year",
                    "Beginning Debt (€)",
                    "Annual Rate (€)",
                    "Interest (€)",
                    "Amortization (€)",
                    "Ending Debt (€)",
                ]

            # Create summary cards
            summary_cards = [
                create_card(
                    t("loan_amount"),
                    f"€ {summary['loan_amount']:,.2f}",
                    COLORS["primary"],
                ),
                create_card(
                    t("monthly_rate"),
                    f"€ {summary['monthly_payment']:,.2f}",
                    COLORS["primary"],
                ),
                create_card(
                    t("total_interest"),
                    f"€ {summary['total_interest']:,.2f}",
                    COLORS["danger"],
                ),
                create_card(
                    f"{t('remaining_debt')} {summary['years']} {t('years_short')}",
                    f"€ {summary['remaining_debt']:,.2f}",
                    COLORS["success"],
                ),
            ]

            # Create key metrics boxes
            key_metrics = [
                create_metric_box(
                    t("input"),
                    {
                        t(
                            "purchase_price_label"
                        ): f"€ {summary['purchase_price']:,.2f}",
                        t("equity_label"): f"€ {summary['equity']:,.2f}",
                        t("interest_rate_label"): f"{summary['interest_rate']:.2f}%",
                    },
                ),
                create_metric_box(
                    t("rates"),
                    {
                        t("annual_rate"): f"€ {summary['annual_payment']:,.2f}",
                        t("monthly_rate"): f"€ {summary['monthly_payment']:,.2f}",
                        t(
                            "total_amortization"
                        ): f"€ {summary['total_amortization']:,.2f}",
                    },
                ),
                create_metric_box(
                    t("totals"),
                    {
                        t(
                            "total_paid"
                        ): f"€ {summary['total_amortization'] + summary['total_interest']:,.2f}",
                        t("interest_costs"): f"€ {summary['total_interest']:,.2f}",
                        f"{t('remaining_debt')} {int(summary['years'])} {t('years_short')}": f"€ {summary['remaining_debt']:,.2f}",
                    },
                ),
            ]

            # Create table
            table = create_table(df)

            # Create charts using the chart generation module
            debt_fig = create_debt_development_chart(df, t)
            interest_chart = create_interest_vs_amortization_chart(df, t)
            pie_fig = create_cost_distribution_pie_chart(summary, t)
            interest_curve_fig = create_interest_curve_chart(df, t)
            interest_dev_fig = create_cumulative_progress_chart(df, t)

            return (
                summary_cards,
                key_metrics,
                table,
                debt_fig,
                interest_chart,
                pie_fig,
                interest_curve_fig,
                interest_dev_fig,
            )

        except Exception as e:
            print(f"Error: {e}")
            error_msg = get_text(lang, "error_calculation")
            error_div = html.Div(
                f"{error_msg}: {str(e)}",
                style={"color": "red", "padding": "1rem"},
            )
            return [error_div], [error_div], error_div, {}, {}, {}, {}, {}

    @app.callback(
        Output("download_csv", "data"),
        Input("download_csv_btn", "n_clicks"),
        [
            State("purchase_price", "value"),
            State("equity", "value"),
            State("interest_rate", "value"),
            State("initial_amortization", "value"),
            State("interest_binding_years", "value"),
            State("annual_special_payment", "value"),
            State("years_to_show", "value"),
            State("language-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def download_csv(
        n_clicks,
        purchase_price,
        equity,
        interest_rate,
        initial_amortization,
        interest_binding_years,
        annual_special_payment,
        years_to_show,
        lang,
    ):
        """Handle CSV export button click"""
        input_data = FinancingInput(
            purchase_price=purchase_price or 0,
            equity=equity or 0,
            interest_rate=interest_rate or 0,
            initial_amortization=initial_amortization or 0,
            annual_special_payment=annual_special_payment or 0,
            interest_binding_years=interest_binding_years or 10,
        )
        calculator = FinancingCalculator(input_data)
        calculator.calculate_schedule(years_to_show or 10)
        df = calculator.schedule_to_dataframe()
        filename = get_text(lang, "export_csv_filename")
        return dcc.send_data_frame(df.to_csv, filename)

    @app.callback(
        Output("download_json", "data"),
        Input("download_json_btn", "n_clicks"),
        [
            State("purchase_price", "value"),
            State("equity", "value"),
            State("interest_rate", "value"),
            State("initial_amortization", "value"),
            State("interest_binding_years", "value"),
            State("annual_special_payment", "value"),
            State("years_to_show", "value"),
            State("language-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def download_json(
        n_clicks,
        purchase_price,
        equity,
        interest_rate,
        initial_amortization,
        interest_binding_years,
        annual_special_payment,
        years_to_show,
        lang,
    ):
        """Handle JSON export button click"""
        input_data = FinancingInput(
            purchase_price=purchase_price or 0,
            equity=equity or 0,
            interest_rate=interest_rate or 0,
            initial_amortization=initial_amortization or 0,
            annual_special_payment=annual_special_payment or 0,
            interest_binding_years=interest_binding_years or 10,
        )
        calculator = FinancingCalculator(input_data)
        schedule = calculator.calculate_schedule(years_to_show or 10)
        summary = calculator.get_summary(years_to_show or 10)

        data = {
            "summary": summary,
            "schedule": [
                {
                    "year": s.year,
                    "debt_start": s.debt_start,
                    "annual_payment": s.annual_payment,
                    "interest_payment": s.interest_payment,
                    "amortization": s.amortization,
                    "debt_end": s.debt_end,
                }
                for s in schedule
            ],
        }

        filename = get_text(lang, "export_json_filename")
        return dcc.send_json(data, filename)

    @app.callback(
        Output("affordability_results", "children"),
        [
            Input("household_income_input", "value"),
            Input("income_percentage_slider", "value"),
            Input("language-store", "data"),
        ],
        [
            State("purchase_price", "value"),
            State("equity", "value"),
            State("interest_rate", "value"),
            State("initial_amortization", "value"),
            State("annual_special_payment", "value"),
            State("interest_binding_years", "value"),
        ],
        prevent_initial_call=False,
    )
    def calculate_affordability(
        household_income,
        income_percentage,
        lang,
        purchase_price,
        equity,
        interest_rate,
        initial_amortization,
        annual_special_payment,
        interest_binding,
    ):
        """Calculate years to payoff based on household income and affordable percentage"""
        t = lambda key: get_text(lang, key)

        # Validate inputs
        if not household_income or household_income <= 0:
            return html.Div(
                html.P(
                    t("error_calculation"),
                    style={"color": COLORS["danger"], "fontSize": "1rem"},
                )
            )

        if not income_percentage or income_percentage < 5 or income_percentage > 40:
            return html.Div(
                html.P(
                    t("error_calculation"),
                    style={"color": COLORS["danger"], "fontSize": "1rem"},
                )
            )

        # Validate financing parameters
        if (
            not purchase_price
            or not equity
            or not interest_rate
            or not initial_amortization
        ):
            return html.Div(
                html.P(
                    f"{t('error_calculation')} - {t('input_params')}",
                    style={"color": COLORS["danger"], "fontSize": "1rem"},
                )
            )

        # Calculate affordable monthly payment
        affordable_monthly_payment = (household_income * income_percentage) / 100

        # Create calculator and calculate payoff
        try:
            input_data = FinancingInput(
                purchase_price=purchase_price,
                equity=equity,
                interest_rate=interest_rate,
                initial_amortization=initial_amortization,
                annual_special_payment=annual_special_payment or 0,
                interest_binding_years=interest_binding or 10,
            )
            calculator = FinancingCalculator(input_data)
            affordability = calculator.calculate_years_to_payoff(
                affordable_monthly_payment
            )

            # Build result display
            if not affordability["feasible"]:
                return html.Div(
                    [
                        html.H4(
                            "⚠️ " + t("payoff_summary"),
                            style={"color": COLORS["danger"], "marginBottom": "1rem"},
                        ),
                        html.P(
                            affordability.get("error", t("error_calculation")),
                            style={"color": COLORS["danger"], "fontSize": "1rem"},
                        ),
                    ]
                )

            # Build results
            return html.Div(
                [
                    html.H4(
                        "✅ " + t("payoff_summary"),
                        style={"marginBottom": "2rem", "color": COLORS["success"]},
                    ),
                    # Results cards in grid
                    html.Div(
                        [
                            create_card(
                                t("household_income"),
                                f"€{household_income:,.0f}",
                                COLORS["primary"],
                            ),
                            create_card(
                                t("affordable_monthly_payment"),
                                f"€{affordable_monthly_payment:,.0f}",
                                COLORS["primary"],
                            ),
                            create_card(
                                t("years_to_payoff"),
                                f"{affordability['years_to_payoff']} {t('years_short')}",
                                COLORS["success"],
                            ),
                            create_card(
                                t("total_interest_by_payoff"),
                                f"€{affordability['total_interest']:,.0f}",
                                COLORS["danger"],
                            ),
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                            "gap": "1.5rem",
                            "marginBottom": "2rem",
                        },
                    ),
                    # Detailed metrics
                    create_metric_box(
                        t("payoff_summary"),
                        {
                            t("loan_amount"): f"€{calculator.loan_amount:,.2f}",
                            t(
                                "monthly_payment_affordable"
                            ): f"€{affordable_monthly_payment:,.2f}",
                            t(
                                "annual_rate"
                            ): f"€{affordability['annual_payment']:,.2f}",
                            t(
                                "years_needed"
                            ): f"{affordability['years_to_payoff']} {t('years_short')}",
                            t(
                                "total_interest_by_payoff"
                            ): f"€{affordability['total_interest']:,.2f}",
                            t(
                                "interest_rate_label"
                            ): f"{calculator.input.interest_rate}%",
                            t(
                                "final_remaining_debt"
                            ): f"€{max(0, affordability['remaining_debt']):,.2f}",
                        },
                    ),
                ]
            )

        except Exception as e:
            return html.Div(
                html.P(
                    f"{t('error_calculation')}: {str(e)}",
                    style={"color": COLORS["danger"], "fontSize": "1rem"},
                )
            )
