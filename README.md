# 🏠 Financing Calculator

An interactive Python-based application for calculating and visualizing property financing with detailed interest curve diagrams and amortization schedules.

## 📋 Overview

The Financing Calculator is a professional tool for analyzing loan financing for property purchases. With interactive input fields and comprehensive visualizations, financial planners can model realistic scenarios and understand how interest and amortization develop over the credit period.

## ✨ Key Features

### 🎯 Core Calculations
- **Loan Amount**: Automatically calculated from purchase price minus equity
- **Monthly & Annual Rates**: Based on initial amortization and interest rate
- **Interest Calculations**: Year-by-year breakdown of interest charges
- **Amortization Schedule**: Detailed tracking of debt reduction
- **Remaining Debt**: Calculation after any number of years

### 📊 Visualizations

The application provides 5 specialized diagrams for comprehensive financial analysis:

1. **Remaining Debt Development**: Shows the progression of decreasing debt as an area chart
2. **Interest vs. Amortization**: Grouped bar chart showing yearly split between interest and principal
3. **Cost Distribution**: Pie chart visualizing the ratio of total amortization to total interest
4. **⭐ Interest Curve**: Specialized diagram showing how annual interest charges decrease over time
5. **Cumulative Development**: Shows cumulative progression of amortization and interest over the years

### 📈 Tables & Data

- **Detailed Amortization Schedule**: Year-by-year table with all relevant metrics
- **Overview Cards**: Quick view of the most important metrics
- **Metric Boxes**: Grouped presentation of input, rate, and total information

### ⬇️ Export
- **CSV Export**: Amortization schedule for Excel and other spreadsheet applications
- **JSON Export**: Structured data for programmatic processing

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- pip (Python Package Manager)

### Step-by-Step Installation

#### 1. Create Virtual Environment (recommended)
```bash
cd /Users/mario/Projekte/Private/financing-calculator
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or for Windows: venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- **dash** (2.14.1) - Interactive dashboard framework
- **plotly** (5.18.0) - Professional visualizations
- **pandas** (2.1.3) - Data processing

## 💻 Usage

### Starting the Application

```bash
cd app
python app.py
```

The application will be available at: **http://localhost:8050**

### Interactive Operation

#### Input Parameters (left side)
Adjust the following parameters and observe real-time calculations:

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Purchase Price | €400,000 | €0+ | Total purchase price of the property |
| Equity | €50,000 | €0+ | Available equity capital |
| Interest Rate p.a. | 4.0% | 0-20% | Annual interest rate |
| Initial Amortization | 2.0% | 0-10% | Initial amortization rate |
| Interest Binding | 10 years | 1-50 | Duration of interest rate binding |
| Special Payment | €0 | €0+ | Additional annual payments |
| Years to Show | 10 | 1-50 | Slider for planning horizon |

#### Tabs (Main Area)

**📊 Overview**
- Four overview cards with the most important metrics
- Three metric boxes with detailed input, rate, and total information

**📈 Amortization Schedule**
- Tabular presentation of the amortization
- Year-by-year breakdown with remaining debt, interest portion, amortization, etc.

**📉 Charts**
- 5 interactive Plotly diagrams
- Hover over data points for details
- Zoom and pan functions available
- Download button in top right of each chart

**⬇️ Export**
- CSV Button: Saves the amortization schedule as .csv file
- JSON Button: Saves all calculation data as .json file

## 📁 Project Structure

```
financing-calculator/
├── app/
│   ├── calculator.py       # Calculation logic and data models
│   └── app.py             # Dash Dashboard application
├── Baufinanzierung_Vorbereitung.csv  # Sample input data
├── requirements.txt        # Python dependencies
├── run.sh                 # Start script
├── SETUP.md              # Detailed setup guide
├── README.md             # This file
└── venv/                 # Python Virtual Environment (after installation)
```

## 🔧 Technology Stack

### Backend
- **Dash** (2.14.1): Modern Interactive Python Dashboard Framework
  - Based on Flask for web server
  - Reactive callbacks for real-time updates
  - No JavaScript required
  
- **Plotly** (5.18.0): Professional, interactive visualizations
  - Hover tooltips
  - Zoom/pan functionality
  - Download buttons
  - Responsive design

- **Pandas** (2.1.3): Data processing and table management

### Why Python-Only?

✅ **Easy to maintain**: Everything in one language  
✅ **Rapid development**: No frontend complexity  
✅ **Professional UI**: Plotly & Dash provide production-ready interface  
✅ **Interactive**: Real-time callbacks for responsive UX  
✅ **Scalable**: Dash apps can be easily extended  

## 🧪 Testing

### Running Tests

The project includes a comprehensive test suite for the calculator module:

```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html
```

### Test Suite

**Location**: `tests/test_calculator.py`

**Coverage**: 24 unit tests organized into 5 test classes

| Test Class | Purpose |
|-----------|---------|
| `TestFinancingInput` | Validate input parameter dataclass |
| `TestYearlySchedule` | Verify schedule entry structure |
| `TestFinancingCalculator` | Core calculation logic and formulas |
| `TestFinancialAccuracy` | Financial calculation verification |
| `TestEdgeCases` | Boundary conditions and edge cases |

### Continuous Integration

The project uses **GitHub Actions** for automated testing:
- Tests run automatically on every commit to `main` branch
- Python 3.10 environment on Ubuntu
- All dependencies installed from `requirements.txt`
- Linting with flake8
- Results visible in pull requests

## 💡 Example Scenarios

### Scenario 1: Standard Financing
```
Purchase Price: €400,000
Equity: €50,000
Interest Rate: 4.0%
Amortization: 2.0%
Result: Monthly Rate €1,750 | Remaining Debt after 10 Years: €265,957
```

### Scenario 2: With Special Payments
```
Purchase Price: €500,000
Equity: €100,000
Interest Rate: 3.5%
Amortization: 3.0%
Special Payment: €10,000/Year
Result: Faster debt reduction | Significant interest savings visible
```

## 📊 Output Values

### Overview Cards
- **Loan Amount**: Purchase price minus equity
- **Monthly Rate**: Annual rate divided by 12
- **Total Interest**: Sum of all interest portions for selected period
- **Remaining Debt**: Outstanding balance after selected number of years

### Detailed Metrics
- **Annual Rate**: Calculated from (interest rate + amortization) × loan amount
- **Total Amortization**: Sum of all amortization portions
- **Total Payments**: Amortization + interest
- **Cumulative Values**: Running totals after each year

## 🎨 Design & UX

- **Modern Styling**: Gradient header, responsive grid layout
- **Color Coding**:
  - 🔵 Blue: Primary (loan amount, rates)
  - 🟢 Green: Success (amortization, positive metrics)
  - 🔴 Red: Danger (interest, debt)
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Mode ready**: CSS variables for easy theme customization

## 🔄 Workflow

1. **Set Parameters** → Adjust all input fields
2. **Real-Time Calculation** → All values update automatically
3. **Review Visualizations** → Charts show the interest curve progression
4. **Analyze Table** → Detailed year-by-year analysis
5. **Export Data** → CSV or JSON for further processing

## 📌 Special Features

### Interest Curve (Zinsverlauf)
The dedicated "Interest Curve" chart shows one of the most important aspects of financing:
- How annual interest charges decrease as the loan progresses
- The dramatic reduction of interest portions over time
- Perfect visualization of why special payments make sense

### Cumulative Development
Shows the overall progression of paid interest vs. amortization:
- Visualizes the relationship between interest costs and debt reduction
- Helps understand interest load distribution over time
- Valuable decision-making aid for credit terms

## 📚 Additional Resources

- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas DataFrame](https://pandas.pydata.org/docs/reference/frame.html)

## 📝 License

This project is licensed under the MIT License.

## 👤 Support

For questions or issues, contact the developer or open an issue in the repository.

---

**Last Updated**: February 14, 2026  
**Version**: 1.0.0  
**Status**: ✅ Production Ready