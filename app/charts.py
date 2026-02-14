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
