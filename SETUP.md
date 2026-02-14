# Financing Calculator - Setup Guide

## Requirements
- Python 3.8 or higher
- pip (Python Package Manager)

## Installation

### 1. Create Virtual Environment (recommended)
```bash
cd /Users/mario/Projekte/Private/financing-calculator
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or for Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Direct Start with Python
```bash
cd app
python app.py
```

The application will automatically open in your browser at `http://localhost:8050`

## Usage

### Input Parameters (left sidebar):
- **Purchase Price** - Total cost of the property
- **Equity** - Available down payment
- **Interest Rate p.a.** - Annual interest rate in %
- **Initial Amortization** - Initial amortization ratio in %
- **Interest Period** - Duration of interest rate lock-in (years)
- **Special Payment** - Additional annual payment

### Tabs (main area):

1. **📊 Overview**
   - Key metrics (loan amount, monthly payment, total interest)
   - Detailed input and result values

2. **📈 Amortization Schedule**
   - Table showing the payment plan
   - Year-by-year breakdown

3. **📉 Charts** ⭐ (Highlight!)
   - **Remaining Debt Development**: Visual progression of decreasing debt
   - **Interest vs. Amortization**: Comparison of yearly payment components
   - **Cost Distribution**: Pie chart of total amounts
   - **Interest Curve**: Dedicated interest decline visualization (focus!)
   - **Cumulative Progress**: Total interest vs. total amortization over time

4. **⬇️ Export**
   - CSV export for Excel/spreadsheets
   - JSON export for further processing

## Features

The calculator computes:
- ✅ Loan amount (purchase price - equity)
- ✅ Monthly and annual payments
- ✅ Interest portion for each year
- ✅ Amortization portion for each year
- ✅ Remaining debt after each year
- ✅ **Interest curves and progression** (primary focus!)
- ✅ Total interest and total amortization
- ✅ Cumulative interest progression
- ✅ CSV and JSON export

## Project Structure

```
financing-calculator/
├── app/
│   ├── calculator.py       # Core business logic
│   ├── app.py             # Application entry point
│   ├── layout.py          # Dashboard layout structure
│   ├── callbacks.py       # Dash callbacks
│   ├── components.py      # Reusable UI components
│   ├── charts.py          # Chart generation
│   ├── config.py          # Configuration & colors
│   └── translations.py    # Multi-language support (DE/EN)
├── Baufinanzierung_Vorbereitung.csv
├── requirements.txt
├── SETUP.md
└── README.md
```

## Technology Stack

- **Framework**: Dash (Plotly-based for interactive dashboards)
- **Visualization**: Plotly (professional, interactive charts)
- **Data Processing**: Pandas
- **Python Version**: 3.8+

## Why Dash?

Dash was chosen because it's ideal for financing calculators:

- ✨ **Reactive Callbacks**: Changes automatically trigger recalculations
- 📊 **Plotly Charts**: Professional, interactive financial diagrams
- 🎯 **Interest Curves**: Perfect for complex interest rate visualizations
- 🚀 **Python-only**: No JavaScript required, everything in Python
- 📱 **Responsive**: Mobile-friendly design
- 🔄 **Live Updates**: Real-time calculations on parameter changes

## Multi-Language Support

The application supports:
- 🇩🇪 **Deutsch** (German)
- 🇬🇧 **English**

Switch languages using the buttons in the header. All UI elements, charts, and exports adapt to the selected language.

## Tips

- Adjust input parameters → immediate recalculation
- Interact with charts: hover for details, zoom, panning
- Use "Years to Show" slider for flexible scenarios
- Use export function to save data for documentation and further processing
- Language switcher in header for German/English interface

## Architecture

The application follows a modular architecture for maintainability:

- **calculator.py** - Core financial calculations (independent of UI)
- **layout.py** - Dashboard structure and input forms
- **callbacks.py** - Dash callback handlers for user interactions
- **components.py** - Reusable UI building blocks
- **charts.py** - Plotly figure generation
- **config.py** - Centralized configuration (colors, themes, settings)
- **translations.py** - Localization strings (EN/DE)

## Troubleshooting

**Port 8050 already in use:**
```bash
lsof -ti:8050 | xargs kill -9
```

**Module import errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Python version issues:**
Ensure you're using Python 3.8 or higher:
```bash
python --version
```
