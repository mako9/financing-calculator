"""
UI Components for Financing Calculator
Reusable Dash components for building the interface
"""

from dash import html, dcc
from config import COLORS
import uuid


def create_card(title, value, color, tooltip_text=None, tooltip_id=None):
    """Create a summary card with title, value, and border color

    Args:
        title: Card title text
        value: Card value to display
        color: Border and value color
        tooltip_text: Optional tooltip text (markdown supported)
        tooltip_id: Optional unique ID for tooltip
    """
    # Create title with optional tooltip applied directly to the title text
    if tooltip_text and tooltip_id:
        title_content = create_tooltip(tooltip_id, tooltip_text, title)
    else:
        title_content = title

    return html.Div(
        [
            html.H3(
                title_content,
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


def create_metric_box(title, metrics, tooltips=None):
    """Create a metrics box with grouped metric displays

    Args:
        title: Box title
        metrics: Dictionary of {key: value} pairs
        tooltips: Optional dictionary of {key: (tooltip_text, tooltip_id)} pairs
    """
    if tooltips is None:
        tooltips = {}

    metric_items = []
    for key, value in metrics.items():
        # Create key label with optional tooltip applied directly to the key text
        if key in tooltips:
            tooltip_text, tooltip_id = tooltips[key]
            key_content = create_tooltip(tooltip_id, tooltip_text, key)
        else:
            key_content = key

        metric_items.append(
            html.Div(
                [
                    html.Div(
                        key_content,
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
        )

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
            html.Div(metric_items),
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
                                    if isinstance(value, (int, float)) and i > 0
                                    else (
                                        str(int(value)) if i == 0 else str(value)
                                    )
                                ),
                                style={
                                    "padding": "0.8rem 1rem",
                                    "borderBottom": f"1px solid {COLORS['light']}",
                                    "textAlign": "right" if i > 0 else "left",
                                },
                            )
                            for i, (col, value) in enumerate(zip(df.columns, row))
                        ]
                    )
                    for row in df.values
                ]
            ),
        ],
        style={"width": "100%", "borderCollapse": "collapse", "fontSize": "0.95rem"},
    )


def create_metric_with_description(title, value, description, color=None, tooltip_text=None, tooltip_id=None):
    """Create a metric card with title, value, and description text

    Args:
        title: Metric title
        value: Metric value to display
        description: Description text below the value
        color: Optional color for the value
        tooltip_text: Optional tooltip text (markdown supported)
        tooltip_id: Optional unique ID for tooltip
    """
    if color is None:
        color = COLORS["primary"]

    # Create title with optional tooltip applied directly to the title text
    if tooltip_text and tooltip_id:
        title_content = create_tooltip(tooltip_id, tooltip_text, title)
    else:
        title_content = title

    return html.Div(
        [
            html.Div(
                title_content,
                style={
                    "fontSize": "0.9rem",
                    "color": COLORS["dark"],
                    "marginBottom": "0.5rem",
                    "fontWeight": "600",
                },
            ),
            html.Div(
                value,
                style={
                    "fontSize": "1.5rem",
                    "fontWeight": "700",
                    "color": color,
                    "marginBottom": "0.5rem",
                },
            ),
            html.Div(
                description,
                style={
                    "fontSize": "0.8rem",
                    "color": COLORS["gray"],
                    "lineHeight": "1.4",
                },
            ),
        ],
        style={
            "padding": "1rem",
            "borderBottom": f"1px solid {COLORS['light']}",
        },
    )


def create_tooltip(tooltip_id, tooltip_text, text_content):
    """Create a tooltip component applied directly to text

    Args:
        tooltip_id: Unique ID for the tooltip
        tooltip_text: Text content for the tooltip (supports markdown)
        text_content: The text to display with tooltip

    Returns:
        html.Span containing the text with tooltip styling
    """
    return html.Span(
        text_content,
        id=tooltip_id,
        title=tooltip_text.replace("**", "").replace("*", ""),  # Plain text for title attribute
        style={
            "cursor": "help",
            "borderBottom": "1px dotted currentColor",
            "textDecoration": "none",
        },
    )

