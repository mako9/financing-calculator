"""
Application Configuration
Centralized configuration for themes, colors, and other app settings
"""

# Color themes
THEMES = {
    "light": {
        "primary": "#007bff",
        "success": "#4ecdc4",
        "danger": "#ff6b6b",
        "warning": "#ffd93d",
        "dark": "#2f3542",
        "light": "#f1f2f6",
        "gray": "#57606f",
    },
    "dark": {
        "primary": "#0d6efd",
        "success": "#198754",
        "danger": "#dc3545",
        "warning": "#ffc107",
        "dark": "#212529",
        "light": "#dee2e6",
        "gray": "#adb5bd",
    },
}

# Default theme
DEFAULT_THEME = "light"
COLORS = THEMES[DEFAULT_THEME]

# UI Settings
SIDEBAR_WIDTH = "300px"
CHART_HEIGHT = 400
BORDER_RADIUS = "8px"
BOX_SHADOW = "0 2px 8px rgba(0, 0, 0, 0.1)"
TABLE_FONT_SIZE = "0.95rem"

# Default financing input values.  These may be overridden with
# environment variables (e.g. export DEFAULT_PURCHASE_PRICE=500000) which
# makes the app easier to configure in different deployments.
import os


def _env_float(key: str, default: float) -> float:
    val = os.getenv(key)
    if val is None:
        return default
    try:
        return float(val)
    except ValueError:
        return default


def _env_int(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        return default


DEFAULT_PURCHASE_PRICE = _env_float("DEFAULT_PURCHASE_PRICE", 500000)
DEFAULT_EQUITY = _env_float("DEFAULT_EQUITY", 50000)
DEFAULT_INTEREST_RATE = _env_float("DEFAULT_INTEREST_RATE", 4.0)  # percent p.a.
DEFAULT_INITIAL_AMORTIZATION = _env_float(
    "DEFAULT_INITIAL_AMORTIZATION", 2.0
)  # percent p.a.
DEFAULT_INTEREST_BINDING_YEARS = _env_int("DEFAULT_INTEREST_BINDING_YEARS", 10)
DEFAULT_ANNUAL_SPECIAL_PAYMENT = _env_float("DEFAULT_ANNUAL_SPECIAL_PAYMENT", 0.0)
DEFAULT_HOUSEHOLD_INCOME = _env_float("DEFAULT_HOUSEHOLD_INCOME", 6000)

# Font settings
PRIMARY_FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
