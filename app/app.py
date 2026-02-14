"""
Financing Calculator Dashboard
Main application entry point

This module initializes the Dash app and registers all callbacks.
Business logic, UI components, charts, and callbacks are organized in separate modules
for better maintainability and code organization.

Modules:
- calculator.py: Core financial calculation engine
- components.py: Reusable UI components (cards, tables, metric boxes)
- charts.py: Chart generation functions
- layout.py: Main dashboard layout structure
- callbacks.py: All Dash callbacks
- translations.py: Multi-language support (German, English)
"""

import dash
from layout import create_layout
from callbacks import register_callbacks


def create_app():
    """Initialize and configure the Dash application"""
    app = dash.Dash(__name__)
    app.title = "Financing Calculator"

    # Set initial layout
    app.layout = create_layout("en")

    # Register all callbacks
    register_callbacks(app)

    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
