import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Page configuration
st.set_page_config(
    page_title="India Wealth Management Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional finance look
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
    }
    .main-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 0.9rem;
        color: #8892B0;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #233;
        padding-bottom: 0.75rem;
    }
    .kpi-card {
        background-color: #1A1D24;
        border-radius: 8px;
        padding: 1rem;
        border-left: 3px solid #00D4B4;
    }
    .kpi-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #8892B0;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 600;
        color: #FFFFFF;
    }
    .insight-text {
        background-color: #1A1D24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #FF5E7A;
        font-size: 0.85rem;
        color: #CCD6F6;
    }
</style>
""", unsafe_allow_html=True)

# Load data with error handling
@st.cache_data
def load_data():
    # Try multiple possible file paths
    possible_paths = [
        "wealth_data.csv",
        "data/wealth_data.csv",
        "./wealth_data.csv",
        "./data/wealth_data.csv"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df
    
    # If no file found, show error and stop
    st.error("Data file not found. Please ensure wealth_data.csv is in the correct location.")
    st.stop()

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar filters
st.sidebar.markdown("### Analysis Controls")
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(2010, 2025),
    step=1
)

filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Quality Legend")
st.sidebar.markdown("• **Real**: Direct source (AMFI, SEBI, World Bank, CFA)")
st.sidebar.markdown("• **Interpolated**: Linear between real anchors")
st.sidebar.markdown("• **Estimated**: Backward extrapolation (2010-2014)")

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Sources**")
st.sidebar.markdown("AMFI | SEBI | World Bank Findex | CFA Institute 2025")

# Main header
st.markdown('<div class="main-header">The Role of Financial Advisors in Wealth Management</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">India | 2010–2025 | 16-Year Panel Dataset</div>', unsafe_allow_html=True)

# Key KPIs in first row
col1, col2, col3, col4, col5 = st.columns(5)

latest = filtered_df[filtered_df["Year"] == filtered_df["Year"].max()].iloc[0]
first = filtered_df[filtered_df["Year"] == filtered_df["Year"].min()].iloc[0]

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total AUM (2025)</div>
        <div class="kpi-value">₹{latest['AUM_Crore']/100000:.2f}L Cr</div>
        <div style="font-size:0.7rem; color:#2DD4A0;">+{(latest['AUM_Crore']/first['AUM_Crore'] - 1)*100:.0f}% since 2010</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Investor Folios (2025)</div>
        <div class="kpi-value">{latest['Folios_Crore']:.2f} Cr</div>
        <div style="font-size:0.7rem; color:#2DD4A0;">+{(latest['Folios_Crore']/first['Folios_Crore'] - 1)*100:.0f}% since 2010</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Financial Literacy Score</div>
        <div class="kpi-value">{latest['Literacy']} / 100</div>
        <div style="font-size:0.7rem; color:#2DD4A0;">+{latest['Literacy'] - first['Literacy']} pts since 2010</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Trust in Advisors</div>
        <div class="kpi-value">{latest['Trust_Percent']}%</div>
        <div style="font-size:0.7rem; color:#2DD4A0;">+{latest['Trust_Percent'] - first['Trust_Percent']} pp since 2010</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Registered Advisors</div>
        <div class="kpi-value">{latest['Advisors']:,.0f}</div>
        <div style="font-size:0.7rem; color:#FF5E7A;">Peak: 1,100 (2020)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Row 2: Growth trends
st.markdown("#### Wealth Management Ecosystem Growth (2010–2025)")

tab1, tab2, tab3 = st.tabs(["Absolute Values", "Indexed Growth (2010=100)", "Year-over-Year Change"])

with tab1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=filtered_df["Year"], y=filtered_df["AUM_Crore"]/100000, mode="lines+markers", name="AUM (Rs Lakh Cr)", line=dict(color="#00D4B4", width=2)))
    fig1.add_trace(go.Scatter(x=filtered_df["Year"], y=filtered_df["Folios_Crore"], mode="lines+markers", name="Folios (Crore)", line=dict(color="#4B9EFF", width=2), yaxis="y2"))
    fig1.update_layout(
        title="AUM and Folios Growth",
        xaxis_title="Year",
        yaxis_title="AUM (Rs Lakh Crore)",
        yaxis2=dict(title="Folios (Crore)", overlaying="y", side="right"),
        template="plotly_dark",
        height=450,
        hovermode="x unified"
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    indexed = filtered_df.copy()
    for col in ["AUM_Crore", "Folios_Crore", "Literacy", "Trust_Percent", "Advisors"]:
        indexed[col + "_index"] = (indexed[col] / indexed[col].iloc[0]) * 100
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["AUM_Crore_index"], mode="lines+markers", name="AUM", line=dict(color="#00D4B4", width=2)))
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["Folios_Crore_index"], mode="lines+markers", name="Folios", line=dict(color="#4B9EFF", width=2)))
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["Literacy_index"], mode="lines+markers", name="Financial Literacy", line=dict(color="#F5A623", width=2)))
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["Trust_Percent_index"], mode="lines+markers", name="Trust in Advisors", line=dict(color="#8B7CF6", width=2)))
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["Advisors_index"], mode="lines+markers", name="Registered Advisors", line=dict(color="#FF5E7A", width=2, dash="dash")))
    fig2.update_layout(
        title="Indexed Growth (2010 = 100)",
        xaxis_title="Year",
        yaxis_title="Index (2010 = 100)",
        template="plotly_dark",
        height=450,
        hovermode="x unified"
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    yoy = filtered_df.copy()
    for col in ["AUM_Crore", "Folios_Crore", "Literacy", "Trust_Percent", "Advisors"]:
        yoy[col + "_yoy"] = yoy[col].pct_change() * 100
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=yoy["Year"], y=yoy["AUM_Crore_yoy"], name="AUM YoY %", marker_color="#00D4B4"))
    fig3.add_trace(go.Scatter(x=yoy["Year"], y=yoy["Literacy_yoy"], mode="lines+markers", name="Literacy YoY %", line=dict(color="#F5A623", width=2), yaxis="y2"))
    fig3.update_layout(
        title="Year-over-Year Growth Rates",
        xaxis_title="Year",
        yaxis_title="AUM Growth (%)",
        yaxis2=dict(title="Literacy Growth (pp)", overlaying="y", side="right"),
        template="plotly_dark",
        height=450,
        hovermode="x unified"
    )
    st.plotly_chart(fig3, use_container_width=True)

# Row 3: Correlation heatmap
st.markdown("#### Correlation Matrix (2010–2025)")
corr_cols = ["AUM_Crore", "Folios_Crore", "Literacy", "Trust_Percent", "Advisors"]
corr_matrix = filtered_df[corr_cols].corr()

fig4 = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale="Tealgrn",
    aspect="auto",
    title="Pearson Correlation Coefficients"
)
fig4.update_layout(template="plotly_dark", height=500)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
<div class="insight-text">
<strong>Key correlation insights:</strong><br>
• Literacy ↔ AUM: r = 0.962 — strongest single driver of wealth growth<br>
• Trust ↔ AUM: r = 0.935 — trust is nearly as powerful as literacy<br>
• Advisors ↔ AUM: r = 0.766 — moderate, because advisor count peaked in 2020 then declined<br>
• Literacy ↔ Trust: r = 0.993 — these two move almost perfectly together
</div>
""", unsafe_allow_html=True)

# Row 4: Advisor Paradox
st.markdown("#### The Advisor Paradox: Fewer Advisors, More AUM")

fig5 = make_subplots(specs=[[{"secondary_y": True}]])
fig5.add_trace(go.Scatter(x=filtered_df["Year"], y=filtered_df["AUM_Crore"]/100000, mode="lines+markers", name="AUM (Rs Lakh Cr)", line=dict(color="#00D4B4", width=2)), secondary_y=False)
fig5.add_trace(go.Scatter(x=filtered_df["Year"], y=filtered_df["Advisors"], mode="lines+markers", name="Registered Advisors", line=dict(color="#FF5E7A", width=2, dash="dash")), secondary_y=True)
fig5.update_layout(title="AUM vs Registered Advisor Count", template="plotly_dark", height=450, hovermode="x unified")
fig5.update_yaxes(title_text="AUM (Rs Lakh Crore)", secondary_y=False, color="#00D4B4")
fig5.update_yaxes(title_text="Number of Registered Advisors", secondary_y=True, color="#FF5E7A")
st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
<div class="insight-text">
<strong>Insight:</strong> Advisors peaked at 1,100 in 2020. By 2025, count fell to 930 (−15.5%) due to SEBI's stricter 2020 regulations. Yet AUM grew from Rs31L Cr to Rs80L Cr (+158%). <strong>Quality and trust now matter more than quantity.</strong>
</div>
""", unsafe_allow_html=True)

# Row 5: Elasticity Calculator
st.markdown("#### Elasticity Calculator: What If Literacy Improves?")
st.markdown("Using your log-log regression: A 1% increase in literacy → 2.82% increase in AUM (elasticity = 2.82)")

col_a, col_b = st.columns([1, 1])

with col_a:
    current_literacy = latest["Literacy"]
    target_literacy = st.slider(
        "Target Financial Literacy Score",
        min_value=int(current_literacy),
        max_value=100,
        value=int(current_literacy),
        step=1
    )
    
    literacy_change_pct = ((target_literacy - current_literacy) / current_literacy) * 100
    aum_change_pct = literacy_change_pct * 2.8245
    projected_aum = latest["AUM_Crore"] * (1 + aum_change_pct / 100)
    
    st.metric(
        label="Literacy Increase",
        value=f"{literacy_change_pct:.1f}%",
        delta=f"from {current_literacy} to {target_literacy}"
    )
    st.metric(
        label="Projected AUM Impact",
        value=f"Rs{projected_aum/100000:.2f}L Cr",
        delta=f"{aum_change_pct:+.1f}% change"
    )

with col_b:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Your Log-Log Elasticity</div>
        <div class="kpi-value">2.8245</div>
        <div style="font-size:0.7rem;">ln(AUM) = 4.0908 + 2.8245 × ln(Literacy)</div>
        <div style="font-size:0.7rem; margin-top:8px;">R² = 0.9913 | p < 0.001</div>
    </div>
    """, unsafe_allow_html=True)

# Row 6: Regression Summary
st.markdown("#### Regression Summary")

reg_tab1, reg_tab2, reg_tab3 = st.tabs(["Simple Linear", "Multiple Linear", "Log-Log Elasticity"])

with reg_tab1:
    st.markdown("**AUM ~ Financial Literacy Score**")
    st.markdown("""
    | Metric | Value |
    |--------|-------|
    | R² | 0.9259 |
    | Adj. R² | 0.9206 |
    | F-statistic | 174.86 (p < 0.001) |
    | Literacy Coefficient | Rs187,744 crore per 1-point increase |
    | Equation | AUM = -51,21,449 + (187,744 x Literacy) |
    """)

with reg_tab2:
    st.markdown("**AUM ~ Literacy + Trust + Advisors**")
    st.markdown("""
    | Metric | Value |
    |--------|-------|
    | R² | 0.9964 |
    | Adj. R² | 0.9955 |
    | Literacy (partial) | Rs454,397 crore per 1-point (p < 0.001) |
    | Trust (partial) | Rs-202,999 crore per 1% (multicollinearity artefact) |
    | Advisors (partial) | Rs-3,677 per advisor (multicollinearity artefact) |
    """)
    st.caption("Note: Negative partial coefficients are due to high multicollinearity (r > 0.90 between predictors). Bivariate correlations are all positive.")

with reg_tab3:
    st.markdown("**Log-Log: ln(AUM) ~ ln(Literacy)**")
    st.markdown("""
    | Metric | Value |
    |--------|-------|
    | R² | 0.9913 |
    | Elasticity | 2.8245 |
    | Interpretation | A 1% increase in literacy → 2.82% increase in AUM |
    | Equation | ln(AUM) = 4.0908 + (2.8245 x ln(Literacy)) |
    """)

# Row 7: Data Quality Tracker
st.markdown("#### Data Quality & Limitations")

status_colors = {"Real": "#2DD4A0", "Interpolated": "#F5A623", "Estimated": "#FF5E7A"}
status_df = filtered_df[["Year", "Data_Status"]].copy()
status_df["Color"] = status_df["Data_Status"].map(status_colors)

fig6 = go.Figure()
for status, color in status_colors.items():
    subset = status_df[status_df["Data_Status"] == status]
    fig6.add_trace(go.Scatter(x=subset["Year"], y=[1]*len(subset), mode="markers", marker=dict(size=12, color=color, symbol="circle"), name=status))
fig6.update_layout(title="Data Quality by Year", xaxis_title="Year", yaxis_title="", showlegend=True, template="plotly_dark", height=200, xaxis=dict(tickmode="linear"), yaxis=dict(showticklabels=False))
st.plotly_chart(fig6, use_container_width=True)

st.markdown("""
<div class="insight-text">
<strong>Limitations acknowledged:</strong><br>
• 2010–2014 values are estimated (no independent source)<br>
• Trust variable has only one real anchor (2025 CFA Institute survey)<br>
• Multicollinearity between Literacy, Trust, and Advisors (all r > 0.90)<br>
• Associations only — not causal inference
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Data sources: AMFI (AUM, Folios) | SEBI (Registered Advisors) | World Bank Global Findex (Literacy) | CFA Institute 2025 (Trust)")
