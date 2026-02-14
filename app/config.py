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

# Font settings
PRIMARY_FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
