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

The application provides 6 specialized diagrams for comprehensive financial analysis:

1. **Remaining Debt Development**: Shows the progression of decreasing debt as an area chart
2. **Interest vs. Amortization**: Grouped bar chart showing yearly split between interest and principal
3. **Cost Distribution**: Pie chart visualizing the ratio of total amortization to total interest
4. **⭐ Interest Curve**: Specialized diagram showing how annual interest charges decrease over time
5. **Cumulative Development**: Shows cumulative progression of amortization and interest over the years with breakeven milestone
6. **Equity Buildup Chart**: Dual-axis visualization showing annual equity gains and cumulative equity percentage over time

### 🎯 Key Performance Indicators (KPIs)

The calculator provides 9 essential KPIs organized by priority to help you make informed financing decisions:

#### High-Priority KPIs (Critical Decision Metrics)

1. **Total Cost of Ownership** - The complete cost of your property including purchase price and all interest paid over the loan period. This shows the true financial commitment beyond the purchase price.

2. **Loan-to-Value (LTV) Ratio** - Percentage of the property financed through the loan. Lower LTV ratios (higher equity) generally mean better loan terms and lower risk.

3. **Interest-to-Principal Ratio** - Shows how much interest you pay relative to the principal amount. Lower ratios indicate better financing efficiency.

4. **Interest Savings from Special Payments** - Calculates how much interest you save and how many years faster you pay off the loan by making special payments. Only displayed when special payments are configured.

#### Medium-Priority KPIs (Progress Tracking)

5. **Breakeven Point** - The milestone year when your cumulative principal payments exceed cumulative interest paid. This psychological milestone shows when you've made significant progress on your loan. Visualized with a marker line in the Cumulative Development chart.

6. **Equity Buildup Rate** - Year-by-year visualization of how your equity grows, showing the accelerating nature of amortization as interest decreases over time. Displayed as both annual gains and cumulative equity percentage.

7. **Housing Expense Ratio** - Your monthly payment as a percentage of household income, with benchmarks (Good: <28%, Caution: 28-33%, Risky: >33%) to assess affordability.

#### Low-Priority KPIs (Risk Analysis)

8. **Emergency Fund Buffer Ratio** - Shows how many months of emergency fund you need relative to your current equity. Helps assess financial security and risk.

9. **Time to 50% Equity** - Years until you own half the property. Important for refinancing opportunities and building substantial equity.

10. **Rate Sensitivity Score** - Shows how much your monthly payment would increase if interest rates rise by 1%. Critical metric when approaching the end of your interest binding period.

### 📈 Tables & Data

- **Detailed Amortization Schedule**: Year-by-year table with all relevant metrics
- **Overview Cards**: Quick view of the most important metrics with interactive tooltips
- **Metric Boxes**: Grouped presentation of input, rate, total information, and KPIs
- **Risk Analysis Section**: Dedicated section with interactive tooltips explaining low-priority KPIs for risk assessment
- **Interactive Tooltips**: Hover over KPI titles (shown with dotted underline and help cursor) to see detailed explanations, formulas, and interpretation guidance

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

> 💡 **Customization**: Default input values (purchase price, equity, interest rate, etc.)
> are defined in `app/config.py` and can be overridden by editing that file or
> supplying corresponding environment variables (`DEFAULT_PURCHASE_PRICE`,
> `DEFAULT_EQUITY`, …) before launching the app.

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
| Purchase Price | €400,000 (configurable in `app/config.py`) | €0+ | Total purchase price of the property |
| Equity | €50,000 (see config) | €0+ | Available equity capital |
| Interest Rate p.a. | 4.0% (see config) | 0-20% | Annual interest rate |
| Initial Amortization | 2.0% (see config) | 0-10% | Initial amortization rate |
| Interest Binding | 10 years (see config) | 1-50 | Duration of interest rate binding |
| Special Payment | €0 (see config) | €0+ | Additional annual payments |
| Years to Show | calculated max | 1-50 | Slider for planning horizon; defaults to the full payoff period |

#### Tabs (Main Area)

**📊 Overview**
- Four overview cards with the most important metrics (loan amount, monthly rate, total interest, remaining debt)
- Hover over card titles to see detailed tooltips with explanations and formulas
- Five metric boxes with detailed information:
  - Input parameters (purchase price, equity, interest rate)
  - Rate information (annual rate, monthly rate, total amortization)
  - Total values (total paid, interest costs, remaining debt)
  - Key Performance Indicators (total cost of ownership, LTV ratio, interest-to-principal ratio)
  - Risk Analysis section with interactive tooltips on all metrics (buffer ratio, time to 50% equity, rate sensitivity)
- All KPI titles feature tooltips accessible by hovering over the dotted-underlined text

**📈 Amortization Schedule**
- Tabular presentation of the amortization
- Year-by-year breakdown with remaining debt, interest portion, amortization, etc.

**📉 Charts**
- 6 interactive Plotly diagrams with hover tooltips for detailed information
- Zoom and pan functions available
- Download button in top right of each chart
- Includes breakeven milestone markers and equity buildup visualization

**⬇️ Export**
- CSV Button: Saves the amortization schedule as .csv file
- JSON Button: Saves all calculation data as .json file

**💰 Affordability**
- Calculate how many years to pay off the loan based on household income
- Input: Net household income and percentage you want to spend on payments (5-40%)
- Output: Affordable monthly payment, years to payoff, total interest, remaining debt
- Reverse calculation: Given income constraints, find the timeline instead of fixed years
- Perfect for: Income-based financing decisions and affordability assessment
- Includes housing expense ratio benchmark (Good: <28%, Caution: 28-33%, Risky: >33%)

## 🎯 KPI Reference Guide

This section provides detailed information about each KPI to help you interpret the metrics and make informed financing decisions.

### High-Priority KPIs

#### 1. Total Cost of Ownership
**What it measures**: The complete financial commitment for your property over the loan period.

**Formula**: Purchase Price + Total Interest Paid

**How to interpret**:
- Shows the true cost of financing beyond the sticker price
- Compare different financing scenarios to minimize total cost
- Higher values indicate more expensive financing overall

**Typical values**:
- With 4% interest over 30 years: ~1.7x the purchase price
- With 3% interest over 20 years: ~1.3x the purchase price
- Lower is better - reduce through higher equity, lower rates, or faster amortization

#### 2. Loan-to-Value (LTV) Ratio
**What it measures**: The percentage of the property value financed through the loan.

**Formula**: (Loan Amount / Purchase Price) × 100

**How to interpret**:
- Lower LTV = more equity = less risk for you and the lender
- Affects your ability to get favorable loan terms
- Important for refinancing opportunities

**Typical ranges**:
- **Excellent**: <60% (high equity position)
- **Good**: 60-80% (standard financing)
- **Caution**: 80-90% (low equity, higher risk)
- **Risky**: >90% (very low equity)

**Benchmark**: Aim for <80% to get better interest rates and avoid additional insurance requirements.

#### 3. Interest-to-Principal Ratio
**What it measures**: How much interest you pay relative to the principal borrowed.

**Formula**: Total Interest / Total Amortization

**How to interpret**:
- Shows the efficiency of your financing
- Lower ratios mean you're paying less for borrowing
- Affected by interest rate, loan term, and special payments

**Typical ranges**:
- **Excellent**: <0.30 (paying less than 30% of principal in interest)
- **Good**: 0.30-0.50 (moderate interest burden)
- **Caution**: 0.50-0.75 (significant interest costs)
- **High**: >0.75 (paying nearly as much or more in interest than principal)

**Benchmark**: Target <0.50 for efficient financing. Special payments significantly reduce this ratio.

#### 4. Interest Savings from Special Payments
**What it measures**: The financial benefit of making additional payments beyond the regular rate.

**What it shows**:
- Interest saved (euros) compared to scenario without special payments
- Years saved in payoff time
- Return on investment for special payments

**How to interpret**:
- Only displayed when annual special payments are configured
- Shows immediate financial impact of extra payments
- Helps justify special payments from savings or bonuses

**Example**: A €10,000 annual special payment on a €400,000 loan at 4% might save €50,000+ in interest and reduce payoff time by 5-7 years.

### Medium-Priority KPIs

#### 5. Breakeven Point
**What it measures**: The year when cumulative principal payments exceed cumulative interest paid.

**How to interpret**:
- Psychological milestone showing meaningful loan progress
- Earlier breakeven = more efficient financing
- Visualized with a marker line in the Cumulative Development chart

**Typical ranges**:
- **Fast**: 8-12 years (higher amortization or special payments)
- **Moderate**: 13-18 years (standard 2-3% amortization)
- **Slow**: 19-25 years (low amortization, high interest)
- **Never**: Indicates very low amortization relative to interest

**Benchmark**: Aim to reach breakeven before year 15 for healthy loan progression.

#### 6. Equity Buildup Rate
**What it measures**: Year-by-year growth of your ownership stake in the property.

**What it shows**:
- Annual equity gained (euros)
- Cumulative equity percentage over time
- Acceleration of equity growth as loan matures

**How to interpret**:
- Equity grows slowly at first (mostly paying interest)
- Accelerates over time as interest portion decreases
- Special payments dramatically increase equity buildup
- Important for refinancing opportunities and net worth tracking

**Visual**: Displayed as dual-axis chart showing both absolute gains (bars) and percentage ownership (line).

#### 7. Housing Expense Ratio
**What it measures**: Your monthly loan payment as a percentage of net household income.

**Formula**: (Monthly Payment / Monthly Net Income) × 100

**How to interpret**:
- Standard measure of housing affordability
- Used by lenders to assess loan risk
- Helps determine sustainable financing levels

**Benchmarks** (industry standard):
- **Good**: <28% (comfortable affordability)
- **Caution**: 28-33% (acceptable but tight)
- **Risky**: >33% (may strain budget, higher default risk)

**Recommendation**: Stay below 28% to maintain financial flexibility for other expenses and savings.

### Low-Priority KPIs (Risk Analysis)

#### 8. Emergency Fund Buffer Ratio
**What it measures**: Emergency fund coverage relative to your equity position.

**Formula**: (Monthly Payment × 6) / Current Equity

**How to interpret**:
- Lower values indicate better financial cushion
- Shows months of emergency fund needed
- Helps assess financial security and risk tolerance

**Typical ranges**:
- **Excellent**: <0.15 (strong equity cushion)
- **Good**: 0.15-0.30 (adequate security)
- **Caution**: 0.30-0.50 (lower cushion)
- **Risky**: >0.50 (thin equity relative to payment obligations)

**Recommendation**: Maintain 6-12 months of payments in emergency fund, especially if ratio is high.

#### 9. Time to 50% Equity
**What it measures**: Years until you own half the property value.

**Why it matters**:
- Important milestone for refinancing opportunities
- Demonstrates substantial ownership stake
- Reduces refinancing risk and improves loan terms

**How to interpret**:
- Earlier is better for financial flexibility
- Affected by initial equity, amortization rate, and special payments
- Key threshold for accessing home equity lines of credit

**Typical ranges**:
- **Fast**: 5-10 years (high initial equity or aggressive amortization)
- **Moderate**: 10-15 years (standard financing)
- **Slow**: 15-20+ years (low equity start, low amortization)

**Benchmark**: Reaching 50% equity within 10-12 years provides good refinancing flexibility.

#### 10. Rate Sensitivity Score
**What it measures**: Monthly payment increase if interest rates rise by 1%.

**Formula**: Payment at (Current Rate + 1%) - Current Payment

**How to interpret**:
- Shows vulnerability to interest rate changes
- **Critical** when approaching end of interest binding period
- Helps plan for refinancing or rate adjustment scenarios

**How to use**:
- Multiply by expected rate change to estimate payment impact
- Example: If sensitivity is €50/month, a 2% rate increase = €100/month more
- Plan budget accordingly for post-binding period

**Risk levels**:
- **Low**: <€50/month (manageable increase)
- **Moderate**: €50-€100/month (noticeable impact)
- **High**: €100-€200/month (significant budget adjustment needed)
- **Very High**: >€200/month (major financial impact)

**Action**: If sensitivity is high and binding period ends soon, consider fixed-rate extension or increased amortization now.

---

## 💡 Using Tooltips - Quick Guide

### What Are Tooltips?
Tooltips provide detailed explanations, formulas, and guidance for all KPIs and metrics in the calculator. They help you understand what each number means and how to interpret it for your financing decisions.

### How to Identify Tooltips
Look for these visual indicators on KPI titles:
- **Dotted underline**: A subtle dotted line beneath the text
- **Help cursor**: Your mouse cursor changes to a question mark (?) when hovering

### How to Use Tooltips
1. **Find** a KPI title with a dotted underline
2. **Hover** your mouse over the underlined text
3. **Wait** a moment for the tooltip to appear
4. **Read** the detailed explanation including:
   - What the KPI measures
   - How it's calculated (formula)
   - How to interpret the values
   - Benchmarks and recommended ranges
5. **Move away** to dismiss the tooltip

### Example KPIs with Tooltips
All these metrics have detailed tooltips:
- **Overview Cards**: Loan Amount, Monthly Rate, Total Interest, Remaining Debt
- **Key Metrics**: Total Cost of Ownership, LTV Ratio, Interest-to-Principal Ratio
- **Risk Analysis**: Buffer Ratio, Time to 50% Equity, Rate Sensitivity Score
- **Affordability**: Housing Expense Ratio, Affordable Monthly Payment

### Benefits
- **Learn as you go**: No need to consult external documentation
- **Make informed decisions**: Understand the significance of each metric
- **Bilingual support**: Available in English and German
- **Always accessible**: Just hover to get help anytime

---

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

The project includes a comprehensive test suite for the calculator module and KPIs:

```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html
```

### Test Suite

**Location**: `tests/`

**Coverage**: Comprehensive unit tests organized into multiple test modules

| Test Module | Purpose |
|-----------|---------|
| `test_calculator.py` | Core calculation logic and formulas (24 tests) |
| `test_callbacks.py` | Dash callback functionality |
| `test_config.py` | Configuration management |
| `test_low_priority_kpis.py` | Low-priority KPIs (buffer ratio, time to 50% equity, rate sensitivity) |
| `test_kpi_integration.py` | KPI integration and interaction tests |
| `test_advanced_kpi_scenarios.py` | Complex KPI scenarios and edge cases |

**Original Test Classes** (in `test_calculator.py`):
- `TestFinancingInput` - Validate input parameter dataclass
- `TestYearlySchedule` - Verify schedule entry structure
- `TestFinancingCalculator` - Core calculation logic and formulas
- `TestFinancialAccuracy` - Financial calculation verification
- `TestEdgeCases` - Boundary conditions and edge cases

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
- **Rate Change Metrics** (if enabled): Total interest with rate change, interest difference, payoff years with change, years difference

### Detailed Metrics

#### Input Metrics Box
- Purchase price, equity, interest rate

#### Rate Metrics Box
- Annual rate, monthly rate, total amortization

#### Totals Metrics Box
- Total payments, interest costs, remaining debt after N years

#### KPI Metrics Box
- Total Cost of Ownership
- Loan-to-Value (LTV) Ratio
- Interest-to-Principal Ratio

#### Interest Savings Box (when special payments configured)
- Total interest without special payments
- Total interest with special payments
- Interest savings amount
- Time saved in years

#### Risk Analysis Box (with tooltips)
- Emergency Fund Buffer Ratio
- Time to 50% Equity
- Rate Sensitivity Score (+1%)

### Advanced Metrics
- **Annual Rate**: Calculated from (interest rate + amortization) × loan amount
- **Total Amortization**: Sum of all amortization portions
- **Total Payments**: Amortization + interest
- **Cumulative Values**: Running totals after each year
- **Breakeven Year**: Year when cumulative principal exceeds cumulative interest
- **Equity Buildup**: Year-by-year equity growth data

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

### 9 Comprehensive KPIs
The calculator provides 9 key performance indicators organized by priority:
- **High-Priority**: Total Cost of Ownership, LTV Ratio, Interest-to-Principal Ratio, Interest Savings
- **Medium-Priority**: Breakeven Point, Equity Buildup Rate, Housing Expense Ratio
- **Low-Priority**: Emergency Fund Buffer Ratio, Time to 50% Equity, Rate Sensitivity Score

Each KPI includes contextual information to help you understand and interpret the metrics.

### Interactive Tooltips
The application features comprehensive tooltips for all KPIs and metrics:
- **Hover-based Help**: Hover over KPI titles to see detailed explanations
- **Visual Indicators**: Titles with tooltips are marked with a dotted underline and help cursor
- **Comprehensive Content**: Each tooltip includes:
  - Clear description of what the metric measures
  - Calculation formula or method
  - Interpretation guidance and benchmarks
  - Actionable insights for decision-making
- **Bilingual Support**: All tooltips available in English and German
- **No Icon Clutter**: Tooltips are applied directly to titles for a clean, modern interface

### Interest Curve (Zinsverlauf)
The dedicated "Interest Curve" chart shows one of the most important aspects of financing:
- How annual interest charges decrease as the loan progresses
- The dramatic reduction of interest portions over time
- Perfect visualization of why special payments make sense

### Cumulative Development with Breakeven Marker
Shows the overall progression of paid interest vs. amortization:
- Visualizes the relationship between interest costs and debt reduction
- Marks the breakeven milestone when principal exceeds interest
- Helps understand interest load distribution over time
- Valuable decision-making aid for credit terms

### Equity Buildup Visualization
Dual-axis chart showing:
- Annual equity gains (bars)
- Cumulative equity percentage (line)
- Demonstrates accelerating nature of amortization
- Helps track wealth building over time

## 📚 Additional Resources

- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas DataFrame](https://pandas.pydata.org/docs/reference/frame.html)

## 📝 License

This project is licensed under the MIT License.

## 👤 Support

For questions or issues, contact the developer or open an issue in the repository.

---

**Last Updated**: March 9, 2026
**Version**: 0.1.0
**Status**: In progress