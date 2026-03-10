"""
Translations for Financing Calculator
Supports German (de) and English (en)
"""

TRANSLATIONS = {
    "en": {
        "app_title": "Financing Calculator",
        "app_subtitle": "Interactive analysis of property financing with detailed interest curve diagrams",
        "input_params": "Input Parameters",
        "purchase_price": "Purchase Price (€)",
        "equity": "Equity (€)",
        "interest_rate": "Interest Rate p.a. (%)",
        "initial_amortization": "Initial Amortization p.a. (%)",
        "interest_binding": "Interest Period (Years)",
        "special_payment": "Special Payment (€)",
        "years_to_show": "Years to Show",
        "overview": "Overview",
        "schedule": "Amortization Schedule",
        "charts": "Charts",
        "export": "Export",
        "loan_amount": "Loan Amount",
        "monthly_rate": "Monthly Rate",
        "total_interest": "Total Interest",
        "remaining_debt": "Remaining Debt after",
        "years_short": "Years",
        "input": "Input",
        "rates": "Rates",
        "totals": "Totals",
        "purchase_price_label": "Purchase Price",
        "equity_label": "Equity",
        "interest_rate_label": "Interest Rate",
        "annual_rate": "Annual Rate",
        "total_amortization": "Total Amortization",
        "total_paid": "Total Paid",
        "interest_costs": "Interest Costs",
        "debt_development": "Remaining Debt Development",
        "year": "Year",
        "interest_vs_amortization": "Interest vs. Amortization per Year",
        "cost_distribution": "Cost Distribution",
        "interest_curve": "Interest Curve over Years",
        "cumulative_progress": "Cumulative Progress: Amortization vs. Interest",
        "interest_portion": "Interest Portion",
        "amortization": "Amortization",
        "cumulative_amortization": "Cumulative Amortization",
        "cumulative_interest": "Cumulative Interest",
        "export_data": "Export Data",
        "download_csv": "📥 Download CSV",
        "download_json": "📥 Download JSON",
        "amount": "Amount",
        "language": "Language",
        "de": "Deutsch",
        "en": "English",
        "error_calculation": "Error in calculation",
        "export_csv_filename": "amortization_schedule.csv",
        "export_json_filename": "amortization_schedule.json",
        "affordability": "Affordability",
        "household_income": "Household Net Income (€/month)",
        "income_percentage": "Percentage for Rate (%)",
        "rate_of_income": "Rate as % of Net Income",
        "of_household_income": "of household income",
        "calculate_years": "Calculate Years to Payoff",
        "affordable_monthly_payment": "Affordable Monthly Payment",
        "years_to_payoff": "Years to Payoff Loan",
        "payoff_summary": "Loan Payoff Summary",
        "monthly_payment_affordable": "Monthly Payment (Affordable)",
        "years_needed": "Years Needed to Payoff",
        "total_interest_by_payoff": "Total Interest by Payoff",
        "final_remaining_debt": "Remaining Debt After Period",
        "total_payoff_years": "Total Years to Payoff Loan",
        "enable_rate_change": "Calculate with Interest Rate Change",
        "new_interest_rate": "New Interest Rate p.a. (%)",
        "after_binding_period": "After binding period",
        "total_interest_with_change": "Total Interest (with change)",
        "payoff_years_with_change": "Payoff Years (with change)",
        "interest_difference": "Interest Difference",
        "years_difference": "Years Difference",
        "rate_change_comparison": "Interest Comparison: Original vs Rate Change",
        "original_rate": "Original Rate",
        "with_rate_change": "With Rate Change",
        "binding_period_end": "Binding Period End",
        "total_cost_of_ownership": "Total Cost of Ownership",
        "interest_to_principal_ratio": "Interest-to-Principal Ratio",
        "ltv_ratio": "Loan-to-Value (LTV) Ratio",
        "interest_savings": "Interest Savings from Special Payments",
        "interest_without_special": "Total Interest (without special payments)",
        "interest_with_special": "Total Interest (with special payments)",
        "time_saved": "Time Saved",
        "kpis": "Key Performance Indicators",
        "financing_risk": "Financing Risk & Cost Metrics",
        "risk_analysis": "Risk Analysis",
        "buffer_ratio": "Emergency Fund Buffer Ratio",
        "buffer_ratio_desc": "Months of emergency fund needed relative to current equity",
        "time_to_50_equity": "Time to 50% Equity",
        "time_to_50_equity_desc": "Years until you own half the property - important for refinancing",
        "rate_sensitivity_score": "Rate Sensitivity (+1%)",
        "rate_sensitivity_desc": "Monthly payment increase if rates rise by 1% - critical near end of binding period",
        "months": "months",
        # Medium-priority KPIs
        "breakeven_year": "Breakeven Point",
        "breakeven_milestone": "Breakeven Milestone (Principal > Interest)",
        "equity_buildup": "Equity Buildup Rate",
        "equity_buildup_progression": "Equity Growth Over Time",
        "year_breakeven": "Year",
        "not_reached": "Not Reached",
        "housing_expense_ratio": "Housing Expense Ratio",
        "housing_expense_benchmark": "Housing Expense Benchmark",
        "good_ratio": "Good (< 28%)",
        "caution_ratio": "Caution (28-33%)",
        "risky_ratio": "Risky (> 33%)",
        "equity_gained_per_year": "Equity Gained per Year",
        "cumulative_equity": "Cumulative Equity",
        "equity_percentage": "Equity Percentage",
        # Tooltips for KPIs
        "tooltip_loan_amount": """**Loan Amount**
The total amount you need to borrow from the bank to purchase the property.

*Calculation:* Purchase Price - Equity
*Significance:* This is the principal amount you'll be paying interest on. A lower loan amount means less interest paid over time.""",
        "tooltip_monthly_rate": """**Monthly Rate**
Your regular monthly payment to the bank, including both interest and principal repayment.

*Calculation:* (Loan Amount × (Interest Rate + Initial Amortization)) / 12
*Significance:* This is what you'll pay every month. Make sure this fits comfortably in your budget.""",
        "tooltip_total_interest": """**Total Interest**
The total amount you'll pay in interest over the entire loan period or shown timeframe.

*Calculation:* Sum of all interest payments across all years
*Significance:* This represents the true cost of borrowing. Lower interest means more affordable financing.""",
        "tooltip_total_payoff_years": """**Total Payoff Years**
The complete duration needed to pay off the loan in full, including all principal and interest.

*Calculation:* Years until remaining debt reaches zero
*Significance:* Shows your financial commitment timeline. Shorter payoff means less interest and faster ownership.""",
        "tooltip_remaining_debt": """**Remaining Debt**
The outstanding loan balance at the end of the selected time period.

*Calculation:* Initial Loan Amount - Cumulative Principal Repaid
*Significance:* Shows how much you still owe. Important for refinancing decisions.""",
        "tooltip_rate_of_income": """**Rate as % of Net Income**
The percentage of your household income that goes toward the mortgage payment.

*Calculation:* (Monthly Payment / Household Net Income) × 100
*Significance:* Financial experts recommend keeping this below 28-33% to maintain financial flexibility.""",
        "tooltip_breakeven_milestone": """**Breakeven Milestone**
The year when your cumulative principal payments exceed cumulative interest payments.

*Calculation:* Year when Cumulative Amortization > Cumulative Interest
*Significance:* A psychological milestone showing you're paying more toward ownership than interest costs.""",
        "tooltip_purchase_price": """**Purchase Price**
The total price of the property you're buying.

*Calculation:* Input parameter
*Significance:* This is your total investment target, including equity and loan amount.""",
        "tooltip_equity": """**Equity**
The amount of money you're paying upfront from your own savings.

*Calculation:* Input parameter
*Significance:* Higher equity means lower loan amount, less interest, and better loan terms. Aim for at least 20%.""",
        "tooltip_interest_rate": """**Interest Rate**
The annual percentage rate charged by the bank on your loan.

*Calculation:* Input parameter (per annum)
*Significance:* Even small changes in interest rate significantly impact total cost. Shop around for the best rate.""",
        "tooltip_annual_rate": """**Annual Rate**
Your total yearly payment to the bank, including both interest and principal.

*Calculation:* Monthly Payment × 12
*Significance:* Useful for annual budgeting and tax planning.""",
        "tooltip_total_amortization": """**Total Amortization**
The total principal repaid over the selected time period.

*Calculation:* Sum of all principal payments
*Significance:* Shows how much of the property you've actually paid for (equity built).""",
        "tooltip_total_paid": """**Total Paid**
The complete amount you've paid to the bank, including both principal and interest.

*Calculation:* Total Amortization + Total Interest
*Significance:* Shows the true total cost of your payments over the period.""",
        "tooltip_interest_costs": """**Interest Costs**
Same as Total Interest - the cumulative interest paid to the bank.

*Calculation:* Sum of all interest payments
*Significance:* Pure cost with no equity gain. Minimize this through higher equity or special payments.""",
        "tooltip_total_cost_of_ownership": """**Total Cost of Ownership**
The complete cost of owning the property, including purchase price and all interest.

*Calculation:* Purchase Price + Total Interest
*Significance:* The true total cost - what you actually pay to own the property outright.""",
        "tooltip_ltv_ratio": """**Loan-to-Value (LTV) Ratio**
The percentage of the property value you're financing through the loan.

*Calculation:* (Loan Amount / Purchase Price) × 100
*Significance:* Lower LTV (below 80%) typically means better interest rates and lower risk.""",
        "tooltip_interest_to_principal_ratio": """**Interest-to-Principal Ratio**
The ratio of total interest paid to total principal repaid.

*Calculation:* Total Interest / Total Amortization
*Significance:* Lower is better. Shows how efficiently you're building equity versus paying interest costs.""",
        "tooltip_interest_without_special": """**Interest Without Special Payments**
Total interest you would pay if you made no special payments.

*Calculation:* Calculated scenario without annual special payments
*Significance:* Baseline for comparison to show the benefit of special payments.""",
        "tooltip_interest_with_special": """**Interest With Special Payments**
Total interest you'll pay when making special payments.

*Calculation:* Calculated with annual special payments included
*Significance:* Shows reduced interest costs when accelerating repayment.""",
        "tooltip_interest_savings": """**Interest Savings**
The amount you save in interest by making special payments.

*Calculation:* Interest Without Special - Interest With Special
*Significance:* Direct financial benefit of special payments. Can save tens of thousands over loan lifetime.""",
        "tooltip_time_saved": """**Time Saved**
Years saved in loan payoff by making special payments.

*Calculation:* Payoff Years Without Special - Payoff Years With Special
*Significance:* Special payments accelerate ownership and free up future income sooner.""",
        "tooltip_buffer_ratio": """**Emergency Fund Buffer Ratio**
Months of emergency fund needed relative to your current equity.

*Calculation:* (Monthly Payment × 6) / Current Equity
*Significance:* Lower is better. Shows if you have adequate reserves relative to your mortgage commitment.""",
        "tooltip_time_to_50_equity": """**Time to 50% Equity**
Years until you own half of the property value.

*Calculation:* Years until (Equity + Cumulative Principal) ≥ 50% of Purchase Price
*Significance:* Important milestone for refinancing options and financial security.""",
        "tooltip_rate_sensitivity_score": """**Rate Sensitivity (+1%)**
How much your monthly payment increases if interest rates rise by 1%.

*Calculation:* Payment at (Current Rate + 1%) - Current Payment
*Significance:* Critical near end of binding period. High sensitivity means you're vulnerable to rate increases.""",
        "tooltip_household_income": """**Household Net Income**
Your total monthly take-home income after taxes.

*Calculation:* Input parameter (monthly)
*Significance:* Foundation for affordability calculations. Be conservative - use guaranteed income only.""",
        "tooltip_affordable_monthly_payment": """**Affordable Monthly Payment**
The monthly payment amount based on your income and chosen percentage.

*Calculation:* Household Income × Income Percentage
*Significance:* What you can realistically afford to pay each month while maintaining quality of life.""",
        "tooltip_housing_expense_ratio": """**Housing Expense Ratio**
Percentage of income going to housing costs.

*Calculation:* (Monthly Payment / Household Income) × 100
*Significance:* Financial benchmark for housing affordability. Below 28% is good, 28-33% is caution, above 33% is risky.""",
        "tooltip_housing_expense_benchmark": """**Housing Expense Benchmark**
Risk assessment based on your housing expense ratio.

*Categories:* Good (<28%), Caution (28-33%), Risky (>33%)
*Significance:* Industry standard for financial health. Helps assess if you're overextending.""",
        "tooltip_years_to_payoff": """**Years to Payoff**
How many years needed to fully pay off the loan with your affordable payment.

*Calculation:* Simulated year-by-year until debt reaches zero
*Significance:* Shows your commitment timeline with affordable payments. Longer term = more interest.""",
        # KPI-specific tooltips (with _tooltip suffix for test compatibility)
        "total_cost_of_ownership_tooltip": """Total Cost of Ownership represents the complete financial commitment of owning the property. Calculation: Purchase Price + Total Interest Paid. This metric shows what you actually pay over the entire financing period. Lower values indicate more cost-effective financing. A good target is to keep total interest below 30-40% of the purchase price.""",
        "interest_to_principal_ratio_tooltip": """Interest-to-Principal Ratio shows the efficiency of your loan repayment. Calculation: Total Interest / Total Principal Repaid. Lower ratios are better, indicating you're building equity faster relative to interest costs. A ratio below 0.5 is excellent, 0.5-1.0 is good, above 1.0 means you're paying more in interest than principal.""",
        "ltv_ratio_tooltip": """Loan-to-Value (LTV) Ratio indicates your loan risk level. Calculation: (Loan Amount / Purchase Price) × 100%. Lower LTV means less risk and typically better interest rates. LTV below 80% is considered good and often avoids additional insurance costs. Higher equity (lower LTV) provides better financial flexibility.""",
        "interest_savings_tooltip": """Interest Savings quantifies the financial benefit of making special payments. Calculation: Total Interest Without Special Payments - Total Interest With Special Payments. This shows how much money you save by accelerating loan repayment. Even modest special payments can save tens of thousands over the loan lifetime.""",
        "breakeven_year_tooltip": """Breakeven Year marks when cumulative principal payments exceed cumulative interest payments. Calculation: First year where Total Principal Paid > Total Interest Paid. This is a psychological and financial milestone showing you're investing more in ownership than in borrowing costs. Earlier breakeven indicates better loan efficiency.""",
        "equity_buildup_tooltip": """Equity Buildup Rate shows how your ownership share grows over time. This metric tracks year-by-year equity gains, revealing the accelerating nature of mortgage amortization (more principal paid as interest decreases). Faster equity buildup means better financial security and refinancing options.""",
        "housing_expense_ratio_tooltip": """Housing Expense Ratio measures affordability by comparing monthly housing costs to income. Calculation: (Monthly Payment / Household Net Income) × 100%. Industry benchmarks: Below 28% is good, 28-33% requires caution, above 33% is financially risky. Lower ratios provide better financial flexibility and emergency resilience.""",
        "buffer_ratio_tooltip": """Emergency Fund Buffer Ratio indicates financial resilience relative to mortgage obligations. Calculation: (Monthly Payment × 6 months) / Current Equity. This shows how many months of emergency reserves you need. Lower values are better. A ratio below 1.0 suggests good emergency preparedness relative to your investment.""",
        "time_to_50_equity_tooltip": """Time to 50% Equity marks when you own half the property value. Calculation: Years until (Initial Equity + Cumulative Principal) ≥ 50% of Purchase Price. This milestone is critical for refinancing opportunities and financial security. Reaching 50% equity typically takes 10-15 years with standard financing but can be accelerated with special payments.""",
        "rate_sensitivity_score_tooltip": """Rate Sensitivity Score shows vulnerability to interest rate increases. Calculation: Monthly Payment at (Current Rate + 1%) - Current Monthly Payment. This is critical when approaching the end of your interest binding period. Higher sensitivity means greater exposure to refinancing risk. Plan ahead if your sensitivity is high (>€200/month).""",
        # Table column headers
        "table_year": "Year",
        "table_beginning_debt": "Beginning Debt (€)",
        "table_annual_rate": "Annual Rate (€)",
        "table_interest": "Interest (€)",
        "table_amortization": "Amortization (€)",
        "table_ending_debt": "Ending Debt (€)",
        # Error messages
        "error_payment_positive": "Payment must be positive",
        "error_payment_insufficient": "Monthly payment insufficient to cover interest",
        "error_payoff_too_long": "Loan would take too long to pay off with this payment",
        # Placeholder text
        "placeholder_currency": "€",
    },
    "de": {
        "app_title": "Baufinanzierung Rechner",
        "app_subtitle": "Interaktive Analyse von Immobilienfinanzierungen mit detaillierten Zinsverlauf-Diagrammen",
        "input_params": "Eingabeparameter",
        "purchase_price": "Kaufpreis (€)",
        "equity": "Eigenkapital (€)",
        "interest_rate": "Sollzins p.a. (%)",
        "initial_amortization": "Anfängliche Tilgung p.a. (%)",
        "interest_binding": "Zinsbindung (Jahre)",
        "special_payment": "Jährliche Sondertilgung (€)",
        "years_to_show": "Jahre anzeigen",
        "overview": "Übersicht",
        "schedule": "Tilgungsplan",
        "charts": "Diagramme",
        "export": "Export",
        "loan_amount": "Darlehensbetrag",
        "monthly_rate": "Monatliche Rate",
        "total_interest": "Gezahlte Zinsen",
        "remaining_debt": "Restschuld nach",
        "years_short": "Jahren",
        "input": "Eingabe",
        "rates": "Raten",
        "totals": "Gesamtsummen",
        "purchase_price_label": "Kaufpreis",
        "equity_label": "Eigenkapital",
        "interest_rate_label": "Zinssatz",
        "annual_rate": "Jährliche Rate",
        "total_amortization": "Gesamttilgung",
        "total_paid": "Zahlungen gesamt",
        "interest_costs": "Zinskosten",
        "debt_development": "Entwicklung der Restschuld",
        "year": "Jahr",
        "interest_vs_amortization": "Zinsanteil vs. Tilgung pro Jahr",
        "cost_distribution": "Kostenaufteilung",
        "interest_curve": "Zinsverlauf über die Jahre",
        "cumulative_progress": "Kumulativer Verlauf: Tilgung vs. Zinsen",
        "interest_portion": "Zinsanteil",
        "amortization": "Tilgung",
        "cumulative_amortization": "Kumulierte Tilgung",
        "cumulative_interest": "Kumulierte Zinsen",
        "export_data": "Daten exportieren",
        "download_csv": "📥 Als CSV herunterladen",
        "download_json": "📥 Als JSON herunterladen",
        "amount": "Betrag",
        "language": "Sprache",
        "de": "Deutsch",
        "en": "English",
        "error_calculation": "Fehler bei der Berechnung",
        "export_csv_filename": "tilgungsplan.csv",
        "export_json_filename": "tilgungsplan.json",
        "affordability": "Leistbarkeit",
        "household_income": "Haushaltsnettoeinkommen (€/Monat)",
        "income_percentage": "Prozentsatz für Rate (%)",
        "rate_of_income": "Rate als % des Nettoeinkommens",
        "of_household_income": "des Haushaltseinkommens",
        "calculate_years": "Jahre bis Rückzahlung berechnen",
        "affordable_monthly_payment": "Leistbare monatliche Rate",
        "years_to_payoff": "Jahre bis Darlehenssanierung",
        "payoff_summary": "Tilgungszusammenfassung",
        "monthly_payment_affordable": "Monatliche Rate (leistbar)",
        "years_needed": "Benötigte Jahre bis Sanierung",
        "total_interest_by_payoff": "Gesamtzinsen bei Sanierung",
        "final_remaining_debt": "Restschuld am Ende des Zeitraums",
        "total_payoff_years": "Gesamtzahlungsdauer des Darlehens",
        "enable_rate_change": "Mit Zinsänderung berechnen",
        "new_interest_rate": "Neuer Sollzins p.a. (%)",
        "after_binding_period": "Nach Zinsbindung",
        "total_interest_with_change": "Gezahlte Zinsen (mit Änderung)",
        "payoff_years_with_change": "Zahlungsdauer (mit Änderung)",
        "interest_difference": "Zinsunterschied",
        "years_difference": "Jahresunterschied",
        "rate_change_comparison": "Zinsvergleich: Original vs Zinsänderung",
        "original_rate": "Originalzinssatz",
        "with_rate_change": "Mit Zinsänderung",
        "binding_period_end": "Ende Zinsbindung",
        "total_cost_of_ownership": "Gesamtkosten des Eigentums",
        "interest_to_principal_ratio": "Zins-Tilgungs-Verhältnis",
        "ltv_ratio": "Beleihungsauslauf (LTV)",
        "interest_savings": "Zinsersparnis durch Sondertilgung",
        "interest_without_special": "Gesamtzinsen (ohne Sondertilgung)",
        "interest_with_special": "Gesamtzinsen (mit Sondertilgung)",
        "time_saved": "Zeitersparnis",
        "kpis": "Wichtige Kennzahlen",
        "financing_risk": "Finanzierungsrisiko & Kostenmetriken",
        "risk_analysis": "Risikoanalyse",
        "buffer_ratio": "Notfall-Puffer-Verhältnis",
        "buffer_ratio_desc": "Anzahl der Monate für Notfallfonds im Verhältnis zum Eigenkapital",
        "time_to_50_equity": "Zeit bis 50% Eigenkapital",
        "time_to_50_equity_desc": "Jahre bis Sie die Hälfte der Immobilie besitzen - wichtig für Anschlussfinanzierung",
        "rate_sensitivity_score": "Zinssensitivität (+1%)",
        "rate_sensitivity_desc": "Anstieg der monatlichen Rate bei 1% Zinserhöhung - kritisch vor Ende der Zinsbindung",
        "months": "Monate",
        # Medium-priority KPIs
        "breakeven_year": "Break-Even-Punkt",
        "breakeven_milestone": "Break-Even-Meilenstein (Tilgung > Zinsen)",
        "equity_buildup": "Eigenkapitalaufbau-Rate",
        "equity_buildup_progression": "Eigenkapitalwachstum über die Zeit",
        "year_breakeven": "Jahr",
        "not_reached": "Nicht erreicht",
        "housing_expense_ratio": "Wohnkosten-Einkommens-Verhältnis",
        "housing_expense_benchmark": "Wohnkosten-Benchmark",
        "good_ratio": "Gut (< 28%)",
        "caution_ratio": "Vorsicht (28-33%)",
        "risky_ratio": "Riskant (> 33%)",
        "equity_gained_per_year": "Eigenkapitalzuwachs pro Jahr",
        "cumulative_equity": "Kumuliertes Eigenkapital",
        "equity_percentage": "Eigenkapitalquote",
        # Tooltips für KPIs (German)
        "tooltip_loan_amount": """**Darlehensbetrag**
Der Gesamtbetrag, den Sie von der Bank leihen müssen, um die Immobilie zu kaufen.

*Berechnung:* Kaufpreis - Eigenkapital
*Bedeutung:* Dies ist der Kapitalbetrag, auf den Sie Zinsen zahlen. Ein niedrigerer Darlehensbetrag bedeutet weniger Zinsen über die Zeit.""",
        "tooltip_monthly_rate": """**Monatliche Rate**
Ihre regelmäßige monatliche Zahlung an die Bank, einschließlich Zinsen und Tilgung.

*Berechnung:* (Darlehensbetrag × (Zinssatz + Anfängliche Tilgung)) / 12
*Bedeutung:* Das zahlen Sie jeden Monat. Stellen Sie sicher, dass dies bequem in Ihr Budget passt.""",
        "tooltip_total_interest": """**Gezahlte Zinsen**
Der Gesamtbetrag, den Sie über den gesamten Kreditzeitraum oder den angezeigten Zeitrahmen an Zinsen zahlen.

*Berechnung:* Summe aller Zinszahlungen über alle Jahre
*Bedeutung:* Dies stellt die wahren Kreditkosten dar. Niedrigere Zinsen bedeuten günstigere Finanzierung.""",
        "tooltip_total_payoff_years": """**Gesamtzahlungsdauer**
Die vollständige Dauer, die benötigt wird, um das Darlehen einschließlich aller Tilgungen und Zinsen vollständig zurückzuzahlen.

*Berechnung:* Jahre bis die Restschuld null erreicht
*Bedeutung:* Zeigt Ihren finanziellen Verpflichtungszeitraum. Kürzere Laufzeit bedeutet weniger Zinsen und schnelleres Eigentum.""",
        "tooltip_remaining_debt": """**Restschuld**
Der ausstehende Kreditsaldo am Ende des ausgewählten Zeitraums.

*Berechnung:* Anfänglicher Darlehensbetrag - Kumulierte Tilgung
*Bedeutung:* Zeigt, wie viel Sie noch schulden. Wichtig für Anschlussfinanzierungsentscheidungen.""",
        "tooltip_rate_of_income": """**Rate als % des Nettoeinkommens**
Der Prozentsatz Ihres Haushaltseinkommens, der für die Hypothekenzahlung aufgewendet wird.

*Berechnung:* (Monatliche Rate / Haushaltsnettoeinkommen) × 100
*Bedeutung:* Finanzexperten empfehlen, dies unter 28-33% zu halten, um finanzielle Flexibilität zu bewahren.""",
        "tooltip_breakeven_milestone": """**Break-Even-Meilenstein**
Das Jahr, in dem Ihre kumulierten Tilgungszahlungen die kumulierten Zinszahlungen übersteigen.

*Berechnung:* Jahr, in dem Kumulierte Tilgung > Kumulierte Zinsen
*Bedeutung:* Ein psychologischer Meilenstein, der zeigt, dass Sie mehr für Eigentum als für Zinskosten zahlen.""",
        "tooltip_purchase_price": """**Kaufpreis**
Der Gesamtpreis der Immobilie, die Sie kaufen.

*Berechnung:* Eingabeparameter
*Bedeutung:* Dies ist Ihr gesamtes Investitionsziel, einschließlich Eigenkapital und Darlehensbetrag.""",
        "tooltip_equity": """**Eigenkapital**
Der Geldbetrag, den Sie im Voraus aus Ihren eigenen Ersparnissen zahlen.

*Berechnung:* Eingabeparameter
*Bedeutung:* Höheres Eigenkapital bedeutet niedrigeren Darlehensbetrag, weniger Zinsen und bessere Kreditkonditionen. Streben Sie mindestens 20% an.""",
        "tooltip_interest_rate": """**Sollzins**
Der jährliche Prozentsatz, den die Bank für Ihr Darlehen berechnet.

*Berechnung:* Eingabeparameter (per annum)
*Bedeutung:* Selbst kleine Änderungen des Zinssatzes wirken sich erheblich auf die Gesamtkosten aus. Vergleichen Sie für den besten Zinssatz.""",
        "tooltip_annual_rate": """**Jährliche Rate**
Ihre gesamte jährliche Zahlung an die Bank, einschließlich Zinsen und Tilgung.

*Berechnung:* Monatliche Rate × 12
*Bedeutung:* Nützlich für jährliche Budgetierung und Steuerplanung.""",
        "tooltip_total_amortization": """**Gesamttilgung**
Die über den ausgewählten Zeitraum zurückgezahlte Gesamttilgung.

*Berechnung:* Summe aller Tilgungszahlungen
*Bedeutung:* Zeigt, wie viel von der Immobilie Sie tatsächlich bezahlt haben (aufgebautes Eigenkapital).""",
        "tooltip_total_paid": """**Zahlungen gesamt**
Der vollständige Betrag, den Sie an die Bank gezahlt haben, einschließlich Tilgung und Zinsen.

*Berechnung:* Gesamttilgung + Gezahlte Zinsen
*Bedeutung:* Zeigt die wahren Gesamtkosten Ihrer Zahlungen über den Zeitraum.""",
        "tooltip_interest_costs": """**Zinskosten**
Wie Gezahlte Zinsen - die kumulierten Zinsen, die an die Bank gezahlt wurden.

*Berechnung:* Summe aller Zinszahlungen
*Bedeutung:* Reine Kosten ohne Eigenkapitalgewinn. Minimieren Sie dies durch höheres Eigenkapital oder Sondertilgungen.""",
        "tooltip_total_cost_of_ownership": """**Gesamtkosten des Eigentums**
Die vollständigen Kosten für den Besitz der Immobilie, einschließlich Kaufpreis und aller Zinsen.

*Berechnung:* Kaufpreis + Gezahlte Zinsen
*Bedeutung:* Die wahren Gesamtkosten - was Sie tatsächlich zahlen, um die Immobilie vollständig zu besitzen.""",
        "tooltip_ltv_ratio": """**Beleihungsauslauf (LTV)**
Der Prozentsatz des Immobilienwerts, den Sie durch das Darlehen finanzieren.

*Berechnung:* (Darlehensbetrag / Kaufpreis) × 100
*Bedeutung:* Niedrigerer LTV (unter 80%) bedeutet typischerweise bessere Zinssätze und geringeres Risiko.""",
        "tooltip_interest_to_principal_ratio": """**Zins-Tilgungs-Verhältnis**
Das Verhältnis der gezahlten Gesamtzinsen zur zurückgezahlten Gesamttilgung.

*Berechnung:* Gezahlte Zinsen / Gesamttilgung
*Bedeutung:* Niedriger ist besser. Zeigt, wie effizient Sie Eigenkapital aufbauen im Vergleich zu Zinszahlungen.""",
        "tooltip_interest_without_special": """**Zinsen ohne Sondertilgung**
Gesamtzinsen, die Sie zahlen würden, wenn Sie keine Sondertilgungen leisten.

*Berechnung:* Berechnetes Szenario ohne jährliche Sondertilgungen
*Bedeutung:* Grundlage für Vergleich, um den Nutzen von Sondertilgungen zu zeigen.""",
        "tooltip_interest_with_special": """**Zinsen mit Sondertilgung**
Gesamtzinsen, die Sie bei Sondertilgungen zahlen.

*Berechnung:* Berechnet mit jährlichen Sondertilgungen
*Bedeutung:* Zeigt reduzierte Zinskosten bei beschleunigter Rückzahlung.""",
        "tooltip_interest_savings": """**Zinsersparnis**
Der Betrag, den Sie durch Sondertilgungen an Zinsen sparen.

*Berechnung:* Zinsen ohne Sondertilgung - Zinsen mit Sondertilgung
*Bedeutung:* Direkter finanzieller Nutzen von Sondertilgungen. Kann über die Laufzeit Zehntausende sparen.""",
        "tooltip_time_saved": """**Zeitersparnis**
Jahre, die bei der Kreditrückzahlung durch Sondertilgungen eingespart werden.

*Berechnung:* Laufzeit ohne Sondertilgung - Laufzeit mit Sondertilgung
*Bedeutung:* Sondertilgungen beschleunigen das Eigentum und setzen zukünftiges Einkommen früher frei.""",
        "tooltip_buffer_ratio": """**Notfall-Puffer-Verhältnis**
Monate Notfallfonds, die im Verhältnis zu Ihrem aktuellen Eigenkapital benötigt werden.

*Berechnung:* (Monatliche Rate × 6) / Aktuelles Eigenkapital
*Bedeutung:* Niedriger ist besser. Zeigt, ob Sie ausreichende Reserven im Verhältnis zu Ihrer Hypothekenverpflichtung haben.""",
        "tooltip_time_to_50_equity": """**Zeit bis 50% Eigenkapital**
Jahre bis Sie die Hälfte des Immobilienwerts besitzen.

*Berechnung:* Jahre bis (Eigenkapital + Kumulierte Tilgung) ≥ 50% des Kaufpreises
*Bedeutung:* Wichtiger Meilenstein für Refinanzierungsoptionen und finanzielle Sicherheit.""",
        "tooltip_rate_sensitivity_score": """**Zinssensitivität (+1%)**
Wie stark Ihre monatliche Rate steigt, wenn die Zinsen um 1% steigen.

*Berechnung:* Zahlung bei (Aktueller Zinssatz + 1%) - Aktuelle Zahlung
*Bedeutung:* Kritisch vor Ende der Zinsbindung. Hohe Sensitivität bedeutet Anfälligkeit für Zinserhöhungen.""",
        "tooltip_household_income": """**Haushaltsnettoeinkommen**
Ihr gesamtes monatliches Nettoeinkommen nach Steuern.

*Berechnung:* Eingabeparameter (monatlich)
*Bedeutung:* Grundlage für Leistbarkeitsberechnungen. Seien Sie konservativ - nutzen Sie nur garantiertes Einkommen.""",
        "tooltip_affordable_monthly_payment": """**Leistbare monatliche Rate**
Der monatliche Ratenbetrag basierend auf Ihrem Einkommen und gewähltem Prozentsatz.

*Berechnung:* Haushaltseinkommen × Einkommensprozentsatz
*Bedeutung:* Was Sie realistisch jeden Monat zahlen können, während Sie Ihre Lebensqualität aufrechterhalten.""",
        "tooltip_housing_expense_ratio": """**Wohnkosten-Einkommens-Verhältnis**
Prozentsatz des Einkommens, der für Wohnkosten aufgewendet wird.

*Berechnung:* (Monatliche Rate / Haushaltseinkommen) × 100
*Bedeutung:* Finanzieller Benchmark für Wohnkostenleistbarkeit. Unter 28% ist gut, 28-33% ist Vorsicht, über 33% ist riskant.""",
        "tooltip_housing_expense_benchmark": """**Wohnkosten-Benchmark**
Risikobewertung basierend auf Ihrem Wohnkosten-Einkommens-Verhältnis.

*Kategorien:* Gut (<28%), Vorsicht (28-33%), Riskant (>33%)
*Bedeutung:* Branchenstandard für finanzielle Gesundheit. Hilft zu beurteilen, ob Sie sich übernehmen.""",
        "tooltip_years_to_payoff": """**Jahre bis Rückzahlung**
Wie viele Jahre benötigt werden, um das Darlehen mit Ihrer leistbaren Rate vollständig zurückzuzahlen.

*Berechnung:* Jahr-für-Jahr-Simulation bis Schulden null erreichen
*Bedeutung:* Zeigt Ihren Verpflichtungszeitraum mit leistbaren Zahlungen. Längere Laufzeit = mehr Zinsen.""",
        # KPI-spezifische Tooltips (mit _tooltip-Suffix für Testkompatibilität)
        "total_cost_of_ownership_tooltip": """Gesamtkosten des Eigentums repräsentieren die vollständige finanzielle Verpflichtung für den Immobilienbesitz. Berechnung: Kaufpreis + Gesamte gezahlte Zinsen. Diese Kennzahl zeigt, was Sie tatsächlich über den gesamten Finanzierungszeitraum zahlen. Niedrigere Werte deuten auf kostengünstigere Finanzierung hin. Ein gutes Ziel ist, die Gesamtzinsen unter 30-40% des Kaufpreises zu halten.""",
        "interest_to_principal_ratio_tooltip": """Zins-Tilgungs-Verhältnis zeigt die Effizienz Ihrer Kreditrückzahlung. Berechnung: Gesamtzinsen / Gesamte zurückgezahlte Tilgung. Niedrigere Verhältnisse sind besser. Dies zeigt, dass Sie schneller Eigenkapital aufbauen im Verhältnis zu Zinskosten. Ein Verhältnis unter 0,5 ist ausgezeichnet. 0,5-1,0 ist gut. Über 1,0 bedeutet, Sie zahlen mehr Zinsen als Tilgung.""",
        "ltv_ratio_tooltip": """Beleihungsauslauf (LTV) zeigt Ihr Kreditrisiko-Niveau. Berechnung: (Darlehensbetrag / Kaufpreis) × 100%. Niedrigerer LTV bedeutet weniger Risiko und typischerweise bessere Zinssätze. LTV unter 80% gilt als gut und vermeidet oft zusätzliche Versicherungskosten. Höheres Eigenkapital (niedrigerer LTV) bietet bessere finanzielle Flexibilität.""",
        "interest_savings_tooltip": """Zinsersparnis quantifiziert den finanziellen Nutzen von Sondertilgungen. Berechnung: Gesamtzinsen ohne Sondertilgung - Gesamtzinsen mit Sondertilgung. Dies zeigt, wie viel Geld Sie durch beschleunigte Kreditrückzahlung sparen. Selbst bescheidene Sondertilgungen können über die Kreditlaufzeit Zehntausende sparen.""",
        "breakeven_year_tooltip": """Break-Even-Jahr markiert, wann kumulierte Tilgungszahlungen die kumulierten Zinszahlungen überschreiten. Berechnung: Erstes Jahr, in dem Gesamte gezahlte Tilgung > Gesamte gezahlte Zinsen. Dies ist ein psychologischer und finanzieller Meilenstein, der zeigt, dass Sie mehr in Eigentum als in Kreditkosten investieren. Früherer Break-Even zeigt bessere Krediteffizienz.""",
        "equity_buildup_tooltip": """Eigenkapitalaufbau-Rate zeigt, wie Ihr Eigentumsanteil über die Zeit wächst. Diese Kennzahl verfolgt jährliche Eigenkapitalgewinne und enthüllt die beschleunigende Natur der Hypothekentilgung (mehr Tilgung gezahlt, wenn Zinsen sinken). Schnellerer Eigenkapitalaufbau bedeutet bessere finanzielle Sicherheit und Refinanzierungsoptionen.""",
        "housing_expense_ratio_tooltip": """Wohnkosten-Einkommens-Verhältnis misst Leistbarkeit durch Vergleich monatlicher Wohnkosten mit Einkommen. Berechnung: (Monatliche Rate / Haushaltsnettoeinkommen) × 100%. Branchen-Benchmarks: Unter 28% ist gut, 28-33% erfordert Vorsicht, über 33% ist finanziell riskant. Niedrigere Verhältnisse bieten bessere finanzielle Flexibilität und Notfallresilienz.""",
        "buffer_ratio_tooltip": """Notfall-Puffer-Verhältnis zeigt finanzielle Widerstandsfähigkeit im Verhältnis zu Hypothekenverpflichtungen. Berechnung: (Monatliche Rate × 6 Monate) / Aktuelles Eigenkapital. Dies zeigt, wie viele Monate Notfallreserven Sie benötigen. Niedrigere Werte sind besser. Ein Verhältnis unter 1,0 deutet auf gute Notfallvorsorge im Verhältnis zu Ihrer Investition hin.""",
        "time_to_50_equity_tooltip": """Zeit bis 50% Eigenkapital markiert, wann Sie die Hälfte des Immobilienwerts besitzen. Berechnung: Jahre bis (Anfängliches Eigenkapital + Kumulierte Tilgung) ≥ 50% des Kaufpreises. Dieser Meilenstein ist kritisch für Refinanzierungsmöglichkeiten und finanzielle Sicherheit. 50% Eigenkapital zu erreichen dauert typischerweise 10-15 Jahre bei Standardfinanzierung, kann aber mit Sondertilgungen beschleunigt werden.""",
        "rate_sensitivity_score_tooltip": """Zinssensitivität zeigt Anfälligkeit für Zinserhöhungen. Berechnung: Monatliche Rate bei (Aktueller Zinssatz + 1%) - Aktuelle monatliche Rate. Dies ist kritisch, wenn Sie sich dem Ende Ihrer Zinsbindung nähern. Höhere Sensitivität bedeutet größere Exposition gegenüber Refinanzierungsrisiko. Planen Sie voraus, wenn Ihre Sensitivität hoch ist (>200€/Monat).""",
        # Table column headers
        "table_year": "Jahr",
        "table_beginning_debt": "Restschuld Anfang (€)",
        "table_annual_rate": "Jahresrate (€)",
        "table_interest": "Zinsanteil (€)",
        "table_amortization": "Tilgung (€)",
        "table_ending_debt": "Restschuld Ende (€)",
        # Error messages
        "error_payment_positive": "Zahlung muss positiv sein",
        "error_payment_insufficient": "Monatliche Zahlung reicht nicht aus, um Zinsen zu decken",
        "error_payoff_too_long": "Darlehensrückzahlung würde mit dieser Zahlung zu lange dauern",
        # Placeholder text
        "placeholder_currency": "€",
    },
}


def get_text(lang, key):
    """Get translated text for a given language and key"""
    if lang not in TRANSLATIONS:
        lang = "en"
    return TRANSLATIONS.get(lang, {}).get(key, key)


def get_all_texts(lang):
    """Get all translations for a given language"""
    if lang not in TRANSLATIONS:
        lang = "en"
    return TRANSLATIONS.get(lang, {})
