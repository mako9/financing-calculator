"""
Chart Generation for Financing Calculator
Creates all Plotly figures for financial visualizations
"""

import plotly.graph_objects as go
from config import COLORS, CHART_HEIGHT


def create_debt_development_chart(df, lang_text_func):
    """Create chart showing remaining debt development over years"""
    t = lang_text_func
    debt_fig = go.Figure()
    debt_fig.add_trace(
        go.Scatter(
            x=df.iloc[:, 0],
            y=df.iloc[:, -1],
            mode="lines+markers",
            name=t("remaining_debt"),
            line=dict(color=COLORS["danger"], width=3),
            marker=dict(size=8),
            fill="tozeroy",
            fillcolor="rgba(255, 107, 107, 0.1)",
        )
    )
    debt_fig.update_layout(
        title=t("debt_development"),
        xaxis_title=t("year"),
        yaxis_title=t("amount"),
        hovermode="x unified",
        template="plotly_white",
        height=CHART_HEIGHT,
        showlegend=False,
    )
    return debt_fig


def create_interest_vs_amortization_chart(df, lang_text_func):
    """Create grouped bar chart comparing interest vs amortization per year"""
    t = lang_text_func
    interest_chart = go.Figure()
    interest_chart.add_trace(
        go.Bar(
            x=df.iloc[:, 0],
            y=df.iloc[:, 3],
            name=t("interest_portion"),
            marker=dict(color=COLORS["danger"]),
        )
    )
    interest_chart.add_trace(
        go.Bar(
            x=df.iloc[:, 0],
            y=df.iloc[:, 4],
            name=t("amortization"),
            marker=dict(color=COLORS["success"]),
        )
    )
    interest_chart.update_layout(
        title=t("interest_vs_amortization"),
        xaxis_title=t("year"),
        yaxis_title=t("amount"),
        barmode="group",
        hovermode="x unified",
        template="plotly_white",
        height=CHART_HEIGHT,
    )
    return interest_chart


def create_cost_distribution_pie_chart(summary, lang_text_func):
    """Create pie chart showing total amortization vs interest costs"""
    t = lang_text_func
    pie_fig = go.Figure(
        data=[
            go.Pie(
                labels=[t("amortization"), t("interest_portion")],
                values=[summary["total_amortization"], summary["total_interest"]],
                marker=dict(colors=[COLORS["success"], COLORS["danger"]]),
            )
        ]
    )
    pie_fig.update_layout(
        title=f"{t('cost_distribution')} {summary['years']} {t('years_short')}",
        height=CHART_HEIGHT,
    )
    return pie_fig


def create_interest_curve_chart(df, lang_text_func):
    """Create chart showing interest payment decline over years"""
    t = lang_text_func
    interest_curve_fig = go.Figure()
    interest_curve_fig.add_trace(
        go.Scatter(
            x=df.iloc[:, 0],
            y=df.iloc[:, 3],
            mode="lines+markers",
            name=t("interest_portion"),
            line=dict(color=COLORS["danger"], width=3),
            marker=dict(size=8),
            fill="tozeroy",
            fillcolor="rgba(255, 107, 107, 0.1)",
        )
    )
    interest_curve_fig.update_layout(
        title=t("interest_curve"),
        xaxis_title=t("year"),
        yaxis_title=t("amount"),
        hovermode="x unified",
        template="plotly_white",
        height=CHART_HEIGHT,
        showlegend=False,
    )
    return interest_curve_fig


def create_cumulative_progress_chart(df, lang_text_func):
    """Create chart showing cumulative amortization vs interest over time"""
    t = lang_text_func

    # Calculate cumulative columns
    df["Cumulative Amortization (€)"] = df.iloc[:, 4].cumsum()
    df["Cumulative Interest (€)"] = df.iloc[:, 3].cumsum()

    interest_dev_fig = go.Figure()
    interest_dev_fig.add_trace(
        go.Scatter(
            x=df.iloc[:, 0],
            y=df["Cumulative Amortization (€)"],
            mode="lines",
            name=t("cumulative_amortization"),
            line=dict(color=COLORS["success"], width=3),
            fill="tozeroy",
            fillcolor="rgba(78, 205, 196, 0.3)",
        )
    )
    interest_dev_fig.add_trace(
        go.Scatter(
            x=df.iloc[:, 0],
            y=df["Cumulative Interest (€)"],
            mode="lines",
            name=t("cumulative_interest"),
            line=dict(color=COLORS["danger"], width=3),
            fill="tozeroy",
            fillcolor="rgba(255, 107, 107, 0.3)",
        )
    )
    interest_dev_fig.update_layout(
        title=t("cumulative_progress"),
        xaxis_title=t("year"),
        yaxis_title=t("amount"),
        hovermode="x unified",
        template="plotly_white",
        height=CHART_HEIGHT,
    )
    return interest_dev_fig

def create_rate_change_comparison_chart(rate_change_result, binding_years, lang_text_func):
    """Create chart comparing cumulative interest with original vs changed rate"""
    t = lang_text_func
    
    if not rate_change_result or rate_change_result.get("years_difference") == 0:
        # If no rate change or same rate, return empty figure
        fig = go.Figure()
        fig.update_layout(
            title=t("rate_change_comparison"),
            template="plotly_white",
            height=CHART_HEIGHT,
        )
        return fig

    original_payoff = rate_change_result["original_payoff_years"]
    new_payoff = rate_change_result["new_payoff_years"]
    max_years = max(original_payoff, new_payoff) + 1

    # Create scenarios
    years_list = list(range(1, max_years + 1))
    
    # Original scenario: constant rate throughout
    original_rate = rate_change_result["original_interest_rate"] / 100
    cumulative_original = []
    
    # Changed scenario: rate changes after binding period
    new_rate = rate_change_result["new_interest_rate"] / 100
    cumulative_changed = []
    
    # Calculate cumulative interest for both scenarios
    # For original: use the actual calculation
    original_total = rate_change_result["original_total_interest"]
    changed_total = rate_change_result["new_total_interest"]
    
    # Distribute interest proportionally over years for visualization
    for year in years_list:
        if year <= original_payoff:
            cumulative_original.append((year / original_payoff) * original_total)
        else:
            cumulative_original.append(original_total)
            
        if year <= new_payoff:
            if year <= binding_years:
                # During binding period, same as original
                cumulative_changed.append((year / binding_years) * (
                    rate_change_result["original_total_interest"] * 
                    (binding_years / original_payoff)
                ))
            else:
                # After binding period with new rate
                years_after = year - binding_years
                interest_during = rate_change_result["original_total_interest"] * (binding_years / original_payoff)
                interest_after_portion = (years_after / (new_payoff - binding_years)) * (changed_total - interest_during)
                cumulative_changed.append(interest_during + interest_after_portion)
        else:
            cumulative_changed.append(changed_total)

    fig = go.Figure()
    
    # Add original scenario line
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=cumulative_original,
            mode="lines+markers",
            name=t("original_rate"),
            line=dict(color=COLORS["success"], width=3),
            marker=dict(size=6),
            fill="tozeroy",
            fillcolor="rgba(78, 205, 196, 0.2)",
        )
    )
    
    # Add changed scenario line
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=cumulative_changed,
            mode="lines+markers",
            name=t("with_rate_change"),
            line=dict(color=COLORS["danger"], width=3),
            marker=dict(size=6),
            fill="tozeroy",
            fillcolor="rgba(255, 107, 107, 0.2)",
        )
    )
    
    # Add binding period marker
    if binding_years < max_years:
        fig.add_vline(
            x=binding_years,
            line_dash="dash",
            line_color=COLORS["warning"],
            annotation_text=t("binding_period_end"),
            annotation_position="top left",
        )
    
    fig.update_layout(
        title=t("rate_change_comparison"),
        xaxis_title=t("year"),
        yaxis_title=t("cumulative_interest"),
        hovermode="x unified",
        template="plotly_white",
        height=CHART_HEIGHT,
        showlegend=True,
    )
    
    return fig