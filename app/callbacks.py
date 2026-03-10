"""
Callbacks for Financing Calculator
Handles all Dash callbacks for user interactions and data updates
"""

from dash import Input, Output, State, dcc, html
from calculator import FinancingCalculator, FinancingInput
from components import create_card, create_metric_box, create_table, create_metric_with_description
from config import COLORS, DEFAULT_INTEREST_BINDING_YEARS
from translations import get_text
from charts import (
    create_debt_development_chart,
    create_interest_vs_amortization_chart,
    create_cost_distribution_pie_chart,
    create_interest_curve_chart,
    create_cumulative_progress_chart,
    create_rate_change_comparison_chart,
    create_equity_buildup_chart,
)


def format_years_months(years: float, t) -> str:
    """Format a fractional year value as years + months."""

    whole_years = int(years)
    fraction = years - whole_years

    # Always show months if there is any fractional part to help avoid
    # misleading integer rounding (e.g., 28.01 years should show 28y 1m).
    months = int(fraction * 12)
    if fraction > 0 and months == 0:
        months = 1

    # If we round up to 12 months, roll over to the next year
    if months >= 12:
        whole_years += 1
        months = 0

    if months == 0:
        return f"{whole_years} {t('years_short')}"

    return f"{whole_years} {t('years_short')} {months}m"


def build_summary_cards(summary, payoff_years, household_income, t):
    """Build the summary cards shown on the overview tab.

    This is extracted into a helper so the formatting logic can be unit tested.
    """

    remaining_debt = summary["remaining_debt"]
    rate_of_income_value = "N/A"
    if household_income and household_income > 0:
        rate_pct = (summary["monthly_payment"] / household_income) * 100
        rate_of_income_value = f"{rate_pct:.1f}% {t('of_household_income')}"

    remaining_label = format_years_months(payoff_years, t)

    # Breakeven year display
    breakeven_year = summary.get("breakeven_year")
    if breakeven_year:
        breakeven_display = f"{t('year_breakeven')} {breakeven_year}"
        breakeven_color = COLORS["success"]
    else:
        breakeven_display = t("not_reached")
        breakeven_color = COLORS["warning"]

    cards = [
        create_card(
            t("loan_amount"),
            f"€ {summary['loan_amount']:,.2f}",
            COLORS["primary"],
            tooltip_text=t("tooltip_loan_amount"),
            tooltip_id="tooltip-loan-amount",
        ),
        create_card(
            t("monthly_rate"),
            f"€ {summary['monthly_payment']:,.2f}",
            COLORS["primary"],
            tooltip_text=t("tooltip_monthly_rate"),
            tooltip_id="tooltip-monthly-rate",
        ),
        create_card(
            t("total_interest"),
            f"€ {summary['total_interest']:,.2f}",
            COLORS["danger"],
            tooltip_text=t("tooltip_total_interest"),
            tooltip_id="tooltip-total-interest",
        ),
        create_card(
            t("total_payoff_years"),
            remaining_label,
            COLORS["warning"],
            tooltip_text=t("tooltip_total_payoff_years"),
            tooltip_id="tooltip-total-payoff-years",
        ),
        create_card(
            f"{t('remaining_debt')} {remaining_label}",
            f"€ {remaining_debt:,.2f}",
            COLORS["success"],
            tooltip_text=t("tooltip_remaining_debt"),
            tooltip_id="tooltip-remaining-debt",
        ),
        create_card(
            t("rate_of_income"),
            rate_of_income_value,
            COLORS["success"],
            tooltip_text=t("tooltip_rate_of_income"),
            tooltip_id="tooltip-rate-of-income",
        ),
        create_card(
            t("breakeven_milestone"),
            breakeven_display,
            breakeven_color,
            tooltip_text=t("tooltip_breakeven_milestone"),
            tooltip_id="tooltip-breakeven-milestone",
        ),
    ]

    return cards


def register_callbacks(app):
    """Register all Dash callbacks with the app"""

    @app.callback(
        [
            Output("app-title", "children"),
            Output("app-subtitle", "children"),
            Output("language-label", "children"),
        ],
        Input("language-store", "data"),
    )
    def update_header_text(lang):
        """Update app title, subtitle, and language label when language changes"""
        t = lambda key: get_text(lang, key)
        return (
            f"🏠 {t('app_title')}",
            t("app_subtitle"),
            f"{t('language')}:",
        )

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
            Output("household-income-label", "children"),
            Output("input-params-title", "children"),
            Output("years-to-show-label", "children"),
        ],
        [Input("language-store", "data"), Input("years_to_show", "value")],
    )
    def update_input_labels(lang, years_value):
        """Update all input parameter labels when language changes"""
        t = lambda key: get_text(lang, key)

        years_label = [
            f"{t('years_to_show')}: ",
            html.Span(
                str(years_value) if years_value else "10",
                id="years_value",
                style={
                    "fontWeight": "700",
                    "color": COLORS["primary"],
                },
            ),
        ]

        return (
            t("purchase_price"),
            t("equity"),
            t("interest_rate"),
            t("initial_amortization"),
            t("interest_binding"),
            t("special_payment"),
            t("household_income"),
            f"📋 {t('input_params')}",
            years_label,
        )

    # Remove the separate years_value callback as it's now integrated above


    @app.callback(
        Output("income_percentage_value", "children"),
        Input("income_percentage_slider", "value"),
    )
    def update_income_percentage_display(percentage):
        """Update the displayed income percentage value from the slider"""
        return f"{percentage}%"

    @app.callback(
        Output("income-percentage-label", "children"),
        [Input("language-store", "data"), Input("income_percentage_slider", "value")],
    )
    def update_income_percentage_label(lang, percentage):
        """Update income percentage label with translation and current value"""
        t = lambda key: get_text(lang, key)
        return [
            f"{t('income_percentage')}: ",
            html.Span(
                f"{percentage}%",
                id="income_percentage_value",
                style={
                    "fontWeight": "700",
                    "color": COLORS["primary"],
                },
            ),
        ]

    @app.callback(
        [
            Output("rate_change_input_container", "style"),
            Output("new_interest_rate", "disabled"),
            Output("new-interest-rate-label", "children"),
            Output("enable_rate_change", "options"),
        ],
        [
            Input("enable_rate_change", "value"),
            Input("language-store", "data"),
        ],
    )
    def toggle_rate_change_input(enable_rate_change, lang):
        """Toggle visibility of interest rate change input"""
        t = lambda key: get_text(lang, key)
        is_enabled = len(enable_rate_change) > 0

        # Update checklist options with translated label
        options = [
            {
                "label": f" {t('enable_rate_change')}",
                "value": 1,
            }
        ]

        return (
            {"display": "block"} if is_enabled else {"display": "none"},
            not is_enabled,
            t("new_interest_rate"),
            options,
        )

    @app.callback(
        [
            Output("tab-overview", "label"),
            Output("tab-affordability", "label"),
            Output("tab-schedule", "label"),
            Output("tab-charts", "label"),
            Output("tab-export", "label"),
            Output("affordability-title", "children"),
            Output("export-title", "children"),
            Output("household_income_input", "placeholder"),
        ],
        Input("language-store", "data"),
    )
    def update_tab_labels(lang):
        """Update all tab labels and section titles when language changes"""
        t = lambda key: get_text(lang, key)
        return (
            f"📊 {t('overview')}",
            f"💰 {t('affordability')}",
            f"📈 {t('schedule')}",
            f"📉 {t('charts')}",
            f"⬇️ {t('export')}",
            f"💰 {t('affordability')}",
            t("export_data"),
            t("placeholder_currency"),
        )


    # Produces max, current slider value, and store copy of payoff years
    @app.callback(
        [
            Output("years_to_show", "max"),
            Output("years_to_show", "value"),
            Output("payoff_years_store", "data"),
        ],
        [
            Input("purchase_price", "value"),
            Input("equity", "value"),
            Input("interest_rate", "value"),
            Input("initial_amortization", "value"),
            Input("interest_binding_years", "value"),
            Input("annual_special_payment", "value"),
        ],
    )
    def update_slider_max(
        purchase_price,
        equity,
        interest_rate,
        initial_amortization,
        interest_binding_years,
        annual_special_payment,
    ):
        """Update the slider max/value/store with calculated payoff years"""
        try:
            input_data = FinancingInput(
                purchase_price=purchase_price or 0,
                equity=equity or 0,
                interest_rate=interest_rate or 0,
                initial_amortization=initial_amortization or 0,
                annual_special_payment=annual_special_payment or 0,
                interest_binding_years=interest_binding_years
                or DEFAULT_INTEREST_BINDING_YEARS,
            )
            calculator = FinancingCalculator(input_data)
            payoff_years = calculator.calculate_payoff_years()
            return payoff_years, payoff_years, payoff_years
        except:
            return 50, 50, 50

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
            Output("rate_change_comparison_chart", "figure"),
            Output("equity_buildup_chart", "figure"),
        ],
        [
            Input("purchase_price", "value"),
            Input("equity", "value"),
            Input("interest_rate", "value"),
            Input("initial_amortization", "value"),
            Input("interest_binding_years", "value"),
            Input("annual_special_payment", "value"),
            Input("household_income_input", "value"),
            Input("years_to_show", "value"),
            Input("language-store", "data"),
            Input("enable_rate_change", "value"),
            Input("new_interest_rate", "value"),
            Input("payoff_years_store", "data"),
        ],
    )
    def update_calculations(
        purchase_price,
        equity,
        interest_rate,
        initial_amortization,
        interest_binding_years,
        annual_special_payment,
        household_income,
        years_to_show,
        lang,
        enable_rate_change,
        new_interest_rate,
        payoff_years_store,
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
                interest_binding_years=interest_binding_years
                or DEFAULT_INTEREST_BINDING_YEARS,
            )

            # Perform calculations
            calculator = FinancingCalculator(input_data)
            # determine how many years should be shown
            if years_to_show:
                years = years_to_show
            elif payoff_years_store is not None:
                years = payoff_years_store
            else:
                years = calculator.calculate_payoff_years()

            schedule = calculator.calculate_schedule(years)
            summary = calculator.get_summary(years)
            payoff_years = calculator.calculate_payoff_years()
            payoff_years_precise = calculator.calculate_payoff_years_precise()
            df = calculator.schedule_to_dataframe()

            # Rename columns based on language
            df.columns = [
                t("table_year"),
                t("table_beginning_debt"),
                t("table_annual_rate"),
                t("table_interest"),
                t("table_amortization"),
                t("table_ending_debt"),
            ]

            # Create summary cards
            summary_cards = build_summary_cards(
                summary, payoff_years_precise, household_income, t
            )

            # Add rate change comparison cards if enabled
            rate_change_result = None
            if len(enable_rate_change) > 0 and new_interest_rate is not None:
                rate_change_result = calculator.calculate_with_rate_change(
                    new_interest_rate
                )

                summary_cards.extend(
                    [
                        create_card(
                            f"{t('total_interest_with_change')}",
                            f"€ {rate_change_result['new_total_interest']:,.2f}",
                            COLORS["danger"],
                        ),
                        create_card(
                            t("interest_difference"),
                            (
                                f"€ {rate_change_result['interest_difference']:,.2f}"
                                if rate_change_result["interest_difference"] > 0
                                else f"-€ {abs(rate_change_result['interest_difference']):,.2f}"
                            ),
                            (
                                COLORS["success"]
                                if rate_change_result["interest_difference"] <= 0
                                else COLORS["danger"]
                            ),
                        ),
                        create_card(
                            f"{t('payoff_years_with_change')}",
                            f"{rate_change_result['new_payoff_years']} {t('years_short')}",
                            COLORS["warning"],
                        ),
                        create_card(
                            t("years_difference"),
                            f"{rate_change_result['years_difference']:+.0f} {t('years_short')}",
                            (
                                COLORS["success"]
                                if rate_change_result["years_difference"] <= 0
                                else COLORS["danger"]
                            ),
                        ),
                    ]
                )

            # Create key metrics boxes
            key_metrics = [
                create_metric_box(
                    t("input"),
                    {
                        t("purchase_price_label"): f"€ {summary['purchase_price']:,.2f}",
                        t("equity_label"): f"€ {summary['equity']:,.2f}",
                        t("interest_rate_label"): f"{summary['interest_rate']:.2f}%",
                    },
                    tooltips={
                        t("purchase_price_label"): (t("tooltip_purchase_price"), "tooltip-purchase-price"),
                        t("equity_label"): (t("tooltip_equity"), "tooltip-equity"),
                        t("interest_rate_label"): (t("tooltip_interest_rate"), "tooltip-interest-rate"),
                    },
                ),
                create_metric_box(
                    t("rates"),
                    {
                        t("annual_rate"): f"€ {summary['annual_payment']:,.2f}",
                        t("monthly_rate"): f"€ {summary['monthly_payment']:,.2f}",
                        t("total_amortization"): f"€ {summary['total_amortization']:,.2f}",
                    },
                    tooltips={
                        t("annual_rate"): (t("tooltip_annual_rate"), "tooltip-annual-rate"),
                        t("monthly_rate"): (t("tooltip_monthly_rate"), "tooltip-monthly-rate-2"),
                        t("total_amortization"): (t("tooltip_total_amortization"), "tooltip-total-amortization"),
                    },
                ),
                create_metric_box(
                    t("totals"),
                    {
                        t("total_paid"): f"€ {summary['total_amortization'] + summary['total_interest']:,.2f}",
                        t("interest_costs"): f"€ {summary['total_interest']:,.2f}",
                        f"{t('remaining_debt')} {int(summary['years'])} {t('years_short')}": f"€ {summary['remaining_debt']:,.2f}",
                    },
                    tooltips={
                        t("total_paid"): (t("tooltip_total_paid"), "tooltip-total-paid"),
                        t("interest_costs"): (t("tooltip_interest_costs"), "tooltip-interest-costs"),
                        f"{t('remaining_debt')} {int(summary['years'])} {t('years_short')}": (t("tooltip_remaining_debt"), "tooltip-remaining-debt-2"),
                    },
                ),
                # New KPI metrics box
                create_metric_box(
                    t("kpis"),
                    {
                        t("total_cost_of_ownership"): f"€ {summary['total_cost_of_ownership']:,.2f}",
                        t("ltv_ratio"): f"{summary['ltv_ratio']:.2f}%",
                        t("interest_to_principal_ratio"): f"{summary['interest_to_principal_ratio']:.2%}",
                    },
                    tooltips={
                        t("total_cost_of_ownership"): (t("tooltip_total_cost_of_ownership"), "tooltip-total-cost-ownership"),
                        t("ltv_ratio"): (t("tooltip_ltv_ratio"), "tooltip-ltv-ratio"),
                        t("interest_to_principal_ratio"): (t("tooltip_interest_to_principal_ratio"), "tooltip-interest-principal-ratio"),
                    },
                ),
            ]

            # Add interest savings metric box if special payments are being made
            if input_data.annual_special_payment > 0:
                key_metrics.append(
                    create_metric_box(
                        t("interest_savings"),
                        {
                            t("interest_without_special"): f"€ {summary['interest_without_special']:,.2f}",
                            t("interest_with_special"): f"€ {summary['interest_with_special']:,.2f}",
                            t("interest_savings"): f"€ {summary['interest_savings']:,.2f}",
                            t("time_saved"): f"{summary['time_saved_years']} {t('years_short')}",
                        },
                        tooltips={
                            t("interest_without_special"): (t("tooltip_interest_without_special"), "tooltip-interest-without-special"),
                            t("interest_with_special"): (t("tooltip_interest_with_special"), "tooltip-interest-with-special"),
                            t("interest_savings"): (t("tooltip_interest_savings"), "tooltip-interest-savings"),
                            t("time_saved"): (t("tooltip_time_saved"), "tooltip-time-saved"),
                        },
                    )
                )

            # Add Risk Analysis metric box with low-priority KPIs
            # This provides a detailed view with descriptions
            risk_analysis_box = html.Div(
                [
                    html.H3(
                        t("risk_analysis"),
                        style={
                            "fontSize": "1.1rem",
                            "marginBottom": "1rem",
                            "color": COLORS["dark"],
                        },
                    ),
                    create_metric_with_description(
                        t("buffer_ratio"),
                        f"{summary['buffer_ratio']:.2f} {t('months')}",
                        t("buffer_ratio_desc"),
                        COLORS["primary"],
                        tooltip_text=t("tooltip_buffer_ratio"),
                        tooltip_id="tooltip-buffer-ratio",
                    ),
                    create_metric_with_description(
                        t("time_to_50_equity"),
                        f"{summary['time_to_50_equity']:.1f} {t('years_short')}",
                        t("time_to_50_equity_desc"),
                        COLORS["success"],
                        tooltip_text=t("tooltip_time_to_50_equity"),
                        tooltip_id="tooltip-time-50-equity",
                    ),
                    create_metric_with_description(
                        t("rate_sensitivity_score"),
                        f"+€ {summary['rate_sensitivity_score']:,.2f}",
                        t("rate_sensitivity_desc"),
                        COLORS["danger"],
                        tooltip_text=t("tooltip_rate_sensitivity_score"),
                        tooltip_id="tooltip-rate-sensitivity",
                    ),
                ],
                style={
                    "backgroundColor": "white",
                    "padding": "1.5rem",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.05)",
                },
            )
            key_metrics.append(risk_analysis_box)

            # Create table
            table = create_table(df)

            # Create charts using the chart generation module
            debt_fig = create_debt_development_chart(df, t)
            interest_chart = create_interest_vs_amortization_chart(df, t)
            pie_fig = create_cost_distribution_pie_chart(summary, t)
            interest_curve_fig = create_interest_curve_chart(df, t)
            interest_dev_fig = create_cumulative_progress_chart(
                df, t, summary.get("breakeven_year")
            )

            # Create rate change comparison chart if rate change is enabled
            rate_change_fig = create_rate_change_comparison_chart(
                rate_change_result, input_data.interest_binding_years, t
            )

            # Create equity buildup chart
            equity_buildup_fig = create_equity_buildup_chart(
                summary.get("equity_buildup_rate", []), t
            )

            return (
                summary_cards,
                key_metrics,
                table,
                debt_fig,
                interest_chart,
                pie_fig,
                interest_curve_fig,
                interest_dev_fig,
                rate_change_fig,
                equity_buildup_fig,
            )

        except Exception as e:
            print(f"Error: {e}")
            error_msg = get_text(lang, "error_calculation")
            error_div = html.Div(
                f"{error_msg}: {str(e)}",
                style={"color": "red", "padding": "1rem"},
            )
            return [error_div], [error_div], error_div, {}, {}, {}, {}, {}, {}, {}

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
            State("payoff_years_store", "data"),
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
        payoff_years_store,
        lang,
    ):
        """Handle CSV export button click"""
        input_data = FinancingInput(
            purchase_price=purchase_price or 0,
            equity=equity or 0,
            interest_rate=interest_rate or 0,
            initial_amortization=initial_amortization or 0,
            annual_special_payment=annual_special_payment or 0,
            interest_binding_years=interest_binding_years
            or DEFAULT_INTEREST_BINDING_YEARS,
        )
        calculator = FinancingCalculator(input_data)
        years = (
            years_to_show or payoff_years_store or calculator.calculate_payoff_years()
        )
        calculator.calculate_schedule(years)
        df = calculator.schedule_to_dataframe()

        # Rename columns based on language
        t = lambda key: get_text(lang, key)
        df.columns = [
            t("table_year"),
            t("table_beginning_debt"),
            t("table_annual_rate"),
            t("table_interest"),
            t("table_amortization"),
            t("table_ending_debt"),
        ]

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
            State("payoff_years_store", "data"),
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
        payoff_years_store,
        lang,
    ):
        """Handle JSON export button click"""
        input_data = FinancingInput(
            purchase_price=purchase_price or 0,
            equity=equity or 0,
            interest_rate=interest_rate or 0,
            initial_amortization=initial_amortization or 0,
            annual_special_payment=annual_special_payment or 0,
            interest_binding_years=interest_binding_years
            or DEFAULT_INTEREST_BINDING_YEARS,
        )
        calculator = FinancingCalculator(input_data)
        years = (
            years_to_show or payoff_years_store or calculator.calculate_payoff_years()
        )
        schedule = calculator.calculate_schedule(years)
        summary = calculator.get_summary(years)

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
                error_key = affordability.get("error_key", "error_calculation")
                error_msg = t(error_key)

                # For error_payment_insufficient, include the payment amount
                if error_key == "error_payment_insufficient":
                    error_payment = affordability.get("error_payment", 0)
                    error_msg = f"{error_msg}: €{error_payment:.2f}"

                return html.Div(
                    [
                        html.H4(
                            "⚠️ " + t("payoff_summary"),
                            style={"color": COLORS["danger"], "marginBottom": "1rem"},
                        ),
                        html.P(
                            error_msg,
                            style={"color": COLORS["danger"], "fontSize": "1rem"},
                        ),
                    ]
                )

            # Build results
            # Calculate Housing Expense Ratio
            housing_expense_ratio = (affordable_monthly_payment / household_income) * 100

            # Determine color based on benchmark
            if housing_expense_ratio < 28:
                her_color = COLORS["success"]
                her_benchmark = t("good_ratio")
            elif housing_expense_ratio <= 33:
                her_color = COLORS["warning"]
                her_benchmark = t("caution_ratio")
            else:
                her_color = COLORS["danger"]
                her_benchmark = t("risky_ratio")

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
                                tooltip_text=t("tooltip_household_income"),
                                tooltip_id="tooltip-household-income",
                            ),
                            create_card(
                                t("affordable_monthly_payment"),
                                f"€{affordable_monthly_payment:,.0f}",
                                COLORS["primary"],
                                tooltip_text=t("tooltip_affordable_monthly_payment"),
                                tooltip_id="tooltip-affordable-payment",
                            ),
                            create_card(
                                t("housing_expense_ratio"),
                                f"{housing_expense_ratio:.1f}%",
                                her_color,
                                tooltip_text=t("tooltip_housing_expense_ratio"),
                                tooltip_id="tooltip-housing-expense-ratio",
                            ),
                            create_card(
                                t("housing_expense_benchmark"),
                                her_benchmark,
                                her_color,
                                tooltip_text=t("tooltip_housing_expense_benchmark"),
                                tooltip_id="tooltip-housing-benchmark",
                            ),
                            create_card(
                                t("years_to_payoff"),
                                f"{affordability['years_to_payoff']} {t('years_short')}",
                                COLORS["success"],
                                tooltip_text=t("tooltip_years_to_payoff"),
                                tooltip_id="tooltip-years-payoff",
                            ),
                            create_card(
                                t("total_interest_by_payoff"),
                                f"€{affordability['total_interest']:,.0f}",
                                COLORS["danger"],
                                tooltip_text=t("tooltip_total_interest"),
                                tooltip_id="tooltip-total-interest-payoff",
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
