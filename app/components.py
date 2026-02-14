"""
UI Components for Financing Calculator
Reusable Dash components for building the interface
"""

from dash import html
from config import COLORS


def create_card(title, value, color):
    """Create a summary card with title, value, and border color"""
    return html.Div(
        [
            html.H3(
                title,
                style={
                    "fontSize": "0.9rem",
                    "color": COLORS["gray"],
                    "marginBottom": "0.5rem",
                    "textTransform": "uppercase",
                    "letterSpacing": "0.5px",
                },
            ),
            html.Div(
                value, style={"fontSize": "1.8rem", "fontWeight": "700", "color": color}
            ),
        ],
        style={
            "backgroundColor": "white",
            "padding": "1.5rem",
            "borderRadius": "8px",
            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.05)",
            "border": f"2px solid {color}",
        },
    )


def create_metric_box(title, metrics):
    """Create a metrics box with grouped metric displays"""
    return html.Div(
        [
            html.H3(
                title,
                style={
                    "fontSize": "1.1rem",
                    "marginBottom": "1rem",
                    "color": COLORS["dark"],
                },
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                key,
                                style={
                                    "fontSize": "0.9rem",
                                    "color": COLORS["gray"],
                                    "marginBottom": "0.3rem",
                                },
                            ),
                            html.Div(
                                value,
                                style={
                                    "fontSize": "1.2rem",
                                    "fontWeight": "600",
                                    "color": COLORS["primary"],
                                },
                            ),
                        ],
                        style={"marginBottom": "1rem"},
                    )
                    for key, value in metrics.items()
                ]
            ),
        ],
        style={
            "backgroundColor": "white",
            "padding": "1.5rem",
            "borderRadius": "8px",
            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.05)",
        },
    )


def create_table(df):
    """Create an HTML table from DataFrame with styled rows and columns"""
    return html.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th(
                            col,
                            style={
                                "padding": "1rem",
                                "textAlign": "left",
                                "fontWeight": "600",
                                "borderBottom": f"2px solid {COLORS['light']}",
                                "backgroundColor": "#f8f9fa",
                            },
                        )
                        for col in df.columns
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(
                                (
                                    f"{value:,.2f}"
                                    if isinstance(value, (int, float)) and col != "Jahr"
                                    else (
                                        str(int(value)) if col == "Jahr" else str(value)
                                    )
                                ),
                                style={
                                    "padding": "0.8rem 1rem",
                                    "borderBottom": f"1px solid {COLORS['light']}",
                                    "textAlign": "right" if col != "Jahr" else "left",
                                },
                            )
                            for col, value in zip(df.columns, row)
                        ]
                    )
                    for row in df.values
                ]
            ),
        ],
        style={"width": "100%", "borderCollapse": "collapse", "fontSize": "0.95rem"},
    )
