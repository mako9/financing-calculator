"""
Layout for Financing Calculator
Main dashboard layout structure with all tabs and components
"""

from dash import dcc, html
from translations import get_text
from config import (
    COLORS,
    SIDEBAR_WIDTH,
    BORDER_RADIUS,
    BOX_SHADOW,
    PRIMARY_FONT,
    DEFAULT_PURCHASE_PRICE,
    DEFAULT_EQUITY,
    DEFAULT_INTEREST_RATE,
    DEFAULT_INITIAL_AMORTIZATION,
    DEFAULT_INTEREST_BINDING_YEARS,
    DEFAULT_ANNUAL_SPECIAL_PAYMENT,
    DEFAULT_HOUSEHOLD_INCOME,
)

# helper to compute initial years-to-show using the same calculator logic
from calculator import FinancingCalculator, FinancingInput


def calculate_default_years() -> int:
    """Return payoff years for the built-in default parameters."""
    default_input = FinancingInput(
        purchase_price=DEFAULT_PURCHASE_PRICE,
        equity=DEFAULT_EQUITY,
        interest_rate=DEFAULT_INTEREST_RATE,
        initial_amortization=DEFAULT_INITIAL_AMORTIZATION,
        annual_special_payment=DEFAULT_ANNUAL_SPECIAL_PAYMENT,
        interest_binding_years=DEFAULT_INTEREST_BINDING_YEARS,
    )
    calc = FinancingCalculator(default_input)
    return calc.calculate_payoff_years()


def create_layout(lang="en"):
    """Create the main app layout with translations"""
    t = lambda key: get_text(lang, key)

    return html.Div(
        [
            dcc.Store(id="language-store", data=lang),
            dcc.Store(id="payoff_years_store", data=None),  # cached payoff years
            # Header with Language Selector
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(
                                f"🏠 {t('app_title')}", style={"marginBottom": "0.5rem"}
                            ),
                            html.P(
                                t("app_subtitle"),
                                style={"color": COLORS["gray"], "marginBottom": "0"},
                            ),
                        ],
                        style={"flex": "1"},
                    ),
                    html.Div(
                        [
                            html.Label(
                                f"{t('language')}:",
                                style={"fontWeight": "600", "marginRight": "0.5rem"},
                            ),
                            html.Button(
                                "🇩🇪 Deutsch",
                                id="lang-de-btn",
                                n_clicks=0,
                                style={
                                    "padding": "0.5rem 1rem",
                                    "backgroundColor": (
                                        COLORS["primary"] if lang == "de" else "white"
                                    ),
                                    "color": (
                                        "white" if lang == "de" else COLORS["primary"]
                                    ),
                                    "border": f"2px solid {COLORS['primary']}",
                                    "borderRadius": "6px",
                                    "cursor": "pointer",
                                    "marginRight": "0.5rem",
                                    "fontWeight": "600",
                                },
                            ),
                            html.Button(
                                "🇬🇧 English",
                                id="lang-en-btn",
                                n_clicks=0,
                                style={
                                    "padding": "0.5rem 1rem",
                                    "backgroundColor": (
                                        COLORS["primary"] if lang == "en" else "white"
                                    ),
                                    "color": (
                                        "white" if lang == "en" else COLORS["primary"]
                                    ),
                                    "border": f"2px solid {COLORS['primary']}",
                                    "borderRadius": "6px",
                                    "cursor": "pointer",
                                    "fontWeight": "600",
                                },
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center"},
                    ),
                ],
                style={
                    "backgroundColor": "white",
                    "padding": "2rem",
                    "marginBottom": "2rem",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                },
            ),
            # Main container
            html.Div(
                [
                    # Sidebar - Input Parameters
                    html.Div(
                        [
                            html.H2(
                                f"📋 {t('input_params')}",
                                id="input-params-title",
                                style={"fontSize": "1.3rem", "marginBottom": "1.5rem"},
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Label(
                                                t("purchase_price"),
                                                id="purchase-price-label",
                                                style={
                                                    "fontWeight": "600",
                                                    "marginBottom": "0.4rem",
                                                },
                                            ),
                                            dcc.Input(
                                                id="purchase_price",
                                                type="number",
                                                value=DEFAULT_PURCHASE_PRICE,
                                                step=10000,
                                                style={
                                                    "width": "100%",
                                                    "padding": "0.7rem",
                                                    "border": f"1px solid {COLORS['light']}",
                                                    "borderRadius": "6px",
                                                    "fontSize": "1rem",
                                                    "marginBottom": "1rem",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                t("equity"),
                                                id="equity-label",
                                                style={
                                                    "fontWeight": "600",
                                                    "marginBottom": "0.4rem",
                                                },
                                            ),
                                            dcc.Input(
                                                id="equity",
                                                type="number",
                                                value=DEFAULT_EQUITY,
                                                step=5000,
                                                style={
                                                    "width": "100%",
                                                    "padding": "0.7rem",
                                                    "border": f"1px solid {COLORS['light']}",
                                                    "borderRadius": "6px",
                                                    "fontSize": "1rem",
                                                    "marginBottom": "1rem",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                t("interest_rate"),
                                                id="interest-rate-label",
                                                style={
                                                    "fontWeight": "600",
                                                    "marginBottom": "0.4rem",
                                                },
                                            ),
                                            dcc.Input(
                                                id="interest_rate",
                                                type="number",
                                                value=DEFAULT_INTEREST_RATE,
                                                step=0.1,
                                                min=0,
                                                max=20,
                                                style={
                                                    "width": "100%",
                                                    "padding": "0.7rem",
                                                    "border": f"1px solid {COLORS['light']}",
                                                    "borderRadius": "6px",
                                                    "fontSize": "1rem",
                                                    "marginBottom": "1rem",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                t("initial_amortization"),
                                                id="initial-amort-label",
                                                style={
                                                    "fontWeight": "600",
                                                    "marginBottom": "0.4rem",
                                                },
                                            ),
                                            dcc.Input(
                                                id="initial_amortization",
                                                type="number",
                                                value=DEFAULT_INITIAL_AMORTIZATION,
                                                step=0.1,
                                                min=0,
                                                max=10,
                                                style={
                                                    "width": "100%",
                                                    "padding": "0.7rem",
                                                    "border": f"1px solid {COLORS['light']}",
                                                    "borderRadius": "6px",
                                                    "fontSize": "1rem",
                                                    "marginBottom": "1rem",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                t("interest_binding"),
                                                id="interest-binding-label",
                                                style={
                                                    "fontWeight": "600",
                                                    "marginBottom": "0.4rem",
                                                },
                                            ),
                                            dcc.Input(
                                                id="interest_binding_years",
                                                type="number",
                                                value=DEFAULT_INTEREST_BINDING_YEARS,
                                                step=1,
                                                min=1,
                                                max=50,
                                                style={
                                                    "width": "100%",
                                                    "padding": "0.7rem",
                                                    "border": f"1px solid {COLORS['light']}",
                                                    "borderRadius": "6px",
                                                    "fontSize": "1rem",
                                                    "marginBottom": "1rem",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                t("special_payment"),
                                                id="special-payment-label",
                                                style={
                                                    "fontWeight": "600",
                                                    "marginBottom": "0.4rem",
                                                },
                                            ),
                                            dcc.Input(
                                                id="annual_special_payment",
                                                type="number",
                                                value=DEFAULT_ANNUAL_SPECIAL_PAYMENT,
                                                step=1000,
                                                min=0,
                                                style={
                                                    "width": "100%",
                                                    "padding": "0.7rem",
                                                    "border": f"1px solid {COLORS['light']}",
                                                    "borderRadius": "6px",
                                                    "fontSize": "1rem",
                                                    "marginBottom": "1rem",
                                                },
                                            ),
                                        ]
                                    ),
                                    # Household income section
                                    html.Div(
                                        [
                                            html.Label(
                                                t("household_income"),
                                                id="household-income-label",
                                                style={
                                                    "fontWeight": "600",
                                                    "marginBottom": "0.4rem",
                                                },
                                            ),
                                            dcc.Input(
                                                id="household_income_input",
                                                type="number",
                                                value=DEFAULT_HOUSEHOLD_INCOME,
                                                placeholder="€",
                                                min=0,
                                                step=100,
                                                style={
                                                    "width": "100%",
                                                    "padding": "0.7rem",
                                                    "border": f"1px solid {COLORS['light']}",
                                                    "borderRadius": "6px",
                                                    "fontSize": "1rem",
                                                    "marginBottom": "1rem",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                [
                                                    f"{t('income_percentage')}: ",
                                                    html.Span(
                                                        "30%",
                                                        id="income_percentage_value",
                                                        style={
                                                            "fontWeight": "700",
                                                            "color": COLORS["primary"],
                                                        },
                                                    ),
                                                ],
                                                id="income-percentage-label",
                                                style={
                                                    "fontWeight": "600",
                                                    "marginBottom": "0.5rem",
                                                    "display": "block",
                                                },
                                            ),
                                            dcc.Slider(
                                                id="income_percentage_slider",
                                                min=5,
                                                max=40,
                                                step=1,
                                                value=30,
                                                marks={
                                                    i: f"{i}%" for i in range(5, 41, 5)
                                                },
                                                tooltip={
                                                    "placement": "bottom",
                                                    "always_visible": True,
                                                },
                                            ),
                                        ],
                                        style={"marginBottom": "1.5rem"},
                                    ),
                                    # Interest rate change section
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Checklist(
                                                        id="enable_rate_change",
                                                        options=[
                                                            {
                                                                "label": f" {t('enable_rate_change')}",
                                                                "value": 1,
                                                            }
                                                        ],
                                                        value=[],
                                                        style={
                                                            "marginBottom": "1rem",
                                                            "fontWeight": "600",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "padding": "1rem",
                                                    "backgroundColor": "#e8f4f8",
                                                    "borderRadius": "6px",
                                                    "borderLeft": f"4px solid {COLORS['primary']}",
                                                },
                                            ),
                                            html.Div(
                                                [
                                                    html.Label(
                                                        t("new_interest_rate"),
                                                        id="new-interest-rate-label",
                                                        style={
                                                            "fontWeight": "600",
                                                            "marginBottom": "0.4rem",
                                                            "display": "block",
                                                        },
                                                    ),
                                                    dcc.Input(
                                                        id="new_interest_rate",
                                                        type="number",
                                                        value=4.0,
                                                        step=0.1,
                                                        min=0,
                                                        max=20,
                                                        disabled=True,
                                                        style={
                                                            "width": "100%",
                                                            "padding": "0.7rem",
                                                            "border": f"1px solid {COLORS['light']}",
                                                            "borderRadius": "6px",
                                                            "fontSize": "1rem",
                                                            "marginBottom": "1rem",
                                                        },
                                                    ),
                                                ],
                                                id="rate_change_input_container",
                                                style={"display": "none"},
                                            ),
                                        ],
                                        style={"marginBottom": "1.5rem"},
                                    ),
                                ],
                                style={"marginBottom": "1.5rem"},
                            ),
                            # Years slider
                            html.Div(
                                [
                                    html.Label(
                                        [
                                            f"{t('years_to_show')}: ",
                                            html.Span(
                                                "10",
                                                id="years_value",
                                                style={
                                                    "fontWeight": "700",
                                                    "color": COLORS["primary"],
                                                },
                                            ),
                                        ],
                                        style={
                                            "fontWeight": "600",
                                            "marginBottom": "0.5rem",
                                            "display": "block",
                                        },
                                    ),
                                    dcc.Slider(
                                        id="years_to_show",
                                        min=1,
                                        max=50,
                                        step=1,
                                        # default shows entire payoff horizon
                                        value=calculate_default_years(),
                                        marks={i: str(i) for i in range(0, 51, 5)},
                                        tooltip={
                                            "placement": "bottom",
                                            "always_visible": True,
                                        },
                                    ),
                                ],
                                style={"marginBottom": "1.5rem"},
                            ),
                        ],
                        style={
                            "width": SIDEBAR_WIDTH,
                            "backgroundColor": "#f8f9fa",
                            "padding": "2rem",
                            "borderRadius": BORDER_RADIUS,
                            "boxShadow": BOX_SHADOW,
                            "marginRight": "2rem",
                        },
                    ),
                    # Content area with tabs
                    html.Div(
                        [
                            dcc.Tabs(
                                id="tabs",
                                value="overview",
                                children=[
                                    # Overview Tab
                                    dcc.Tab(
                                        label=f"📊 {t('overview')}",
                                        value="overview",
                                        children=[
                                            html.Div(
                                                id="summary_cards",
                                                style={
                                                    "display": "grid",
                                                    "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                                                    "gap": "1.5rem",
                                                    "marginBottom": "2rem",
                                                },
                                            ),
                                            html.Div(
                                                id="key_metrics",
                                                style={
                                                    "display": "grid",
                                                    "gridTemplateColumns": "repeat(auto-fit, minmax(300px, 1fr))",
                                                    "gap": "1.5rem",
                                                    "marginBottom": "2rem",
                                                },
                                            ),
                                        ],
                                    ),
                                    # Affordability Tab
                                    dcc.Tab(
                                        label=f"💰 {t('affordability')}",
                                        value="affordability",
                                        children=[
                                            html.Div(
                                                [
                                                    html.H3(
                                                        f"💰 {t('affordability')}",
                                                        style={"marginBottom": "1rem"},
                                                    ),
                                                    html.Div(
                                                        id="affordability_results",
                                                        style={
                                                            "backgroundColor": "white",
                                                            "padding": "2rem",
                                                            "borderRadius": "8px",
                                                            "boxShadow": BOX_SHADOW,
                                                        },
                                                    ),
                                                ],
                                                style={"marginTop": "2rem"},
                                            ),
                                        ],
                                    ),
                                    # Table Tab
                                    dcc.Tab(
                                        label=f"📈 {t('schedule')}",
                                        value="table",
                                        children=[
                                            html.Div(
                                                id="table_container",
                                                style={
                                                    "backgroundColor": "white",
                                                    "padding": "1.5rem",
                                                    "borderRadius": "8px",
                                                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                                                    "overflowX": "auto",
                                                },
                                            ),
                                        ],
                                    ),
                                    # Charts Tab
                                    dcc.Tab(
                                        label=f"📉 {t('charts')}",
                                        value="charts",
                                        children=[
                                            html.Div(
                                                dcc.Graph(id="debt_chart"),
                                                style={
                                                    "backgroundColor": "white",
                                                    "padding": "1.5rem",
                                                    "borderRadius": "8px",
                                                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                                                    "marginBottom": "2rem",
                                                },
                                            ),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        dcc.Graph(
                                                            id="interest_amortization_chart"
                                                        ),
                                                        style={
                                                            "flex": "1",
                                                            "marginRight": "1rem",
                                                        },
                                                    ),
                                                    html.Div(
                                                        dcc.Graph(id="pie_chart"),
                                                        style={"flex": "1"},
                                                    ),
                                                ],
                                                style={
                                                    "display": "flex",
                                                    "gap": "1.5rem",
                                                    "marginBottom": "2rem",
                                                },
                                            ),
                                            html.Div(
                                                dcc.Graph(id="interest_curve_chart"),
                                                style={
                                                    "backgroundColor": "white",
                                                    "padding": "1.5rem",
                                                    "borderRadius": "8px",
                                                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                                                    "marginBottom": "2rem",
                                                },
                                            ),
                                            html.Div(
                                                dcc.Graph(
                                                    id="interest_development_chart"
                                                ),
                                                style={
                                                    "backgroundColor": "white",
                                                    "padding": "1.5rem",
                                                    "borderRadius": "8px",
                                                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                                                    "marginBottom": "2rem",
                                                },
                                            ),
                                            html.Div(
                                                dcc.Graph(
                                                    id="rate_change_comparison_chart"
                                                ),
                                                style={
                                                    "backgroundColor": "white",
                                                    "padding": "1.5rem",
                                                    "borderRadius": "8px",
                                                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                                                    "marginBottom": "2rem",
                                                },
                                            ),
                                            html.Div(
                                                dcc.Graph(
                                                    id="equity_buildup_chart"
                                                ),
                                                style={
                                                    "backgroundColor": "white",
                                                    "padding": "1.5rem",
                                                    "borderRadius": "8px",
                                                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                                                },
                                            ),
                                        ],
                                    ),
                                    # Export Tab
                                    dcc.Tab(
                                        label=f"⬇️ {t('export')}",
                                        value="export",
                                        children=[
                                            html.Div(
                                                [
                                                    html.H3(
                                                        t("export_data"),
                                                        style={
                                                            "marginBottom": "1.5rem"
                                                        },
                                                    ),
                                                    html.Button(
                                                        t("download_csv"),
                                                        id="download_csv_btn",
                                                        n_clicks=0,
                                                        style={
                                                            "padding": "0.8rem 1.5rem",
                                                            "backgroundColor": COLORS[
                                                                "primary"
                                                            ],
                                                            "color": "white",
                                                            "border": "none",
                                                            "borderRadius": "6px",
                                                            "cursor": "pointer",
                                                            "fontSize": "1rem",
                                                            "fontWeight": "600",
                                                            "marginRight": "1rem",
                                                            "marginBottom": "1rem",
                                                        },
                                                    ),
                                                    html.Button(
                                                        t("download_json"),
                                                        id="download_json_btn",
                                                        n_clicks=0,
                                                        style={
                                                            "padding": "0.8rem 1.5rem",
                                                            "backgroundColor": COLORS[
                                                                "success"
                                                            ],
                                                            "color": "white",
                                                            "border": "none",
                                                            "borderRadius": "6px",
                                                            "cursor": "pointer",
                                                            "fontSize": "1rem",
                                                            "fontWeight": "600",
                                                            "marginBottom": "1rem",
                                                        },
                                                    ),
                                                    dcc.Download(id="download_csv"),
                                                    dcc.Download(id="download_json"),
                                                ],
                                                style={
                                                    "backgroundColor": "white",
                                                    "padding": "2rem",
                                                    "borderRadius": "8px",
                                                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                                                },
                                            ),
                                        ],
                                    ),
                                ],
                                style={
                                    "backgroundColor": "white",
                                    "borderRadius": "8px",
                                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                                },
                            ),
                        ],
                        style={"flex": "1"},
                    ),
                ],
                style={"display": "flex", "gap": "0"},
            ),
        ],
        style={
            "padding": "2rem",
            "backgroundColor": "#f5f6fa",
            "minHeight": "100vh",
            "fontFamily": PRIMARY_FONT,
        },
    )
