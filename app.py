import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Page configuration
st.set_page_config(
    page_title="India Wealth Management Dashboard | Financial Advisors Study",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional finance dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0B0F18;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main header */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.25rem;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #00D4B4 0%, #4B9EFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sub-header {
        font-size: 0.85rem;
        color: #6B7B8D;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #1E2D3D;
        padding-bottom: 0.75rem;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #131A26 0%, #0F151F 100%);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        border: 1px solid #1E2D3D;
        border-left: 4px solid #00D4B4;
        transition: all 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #2A3A4A;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    .kpi-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8B9BB0;
        font-weight: 600;
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.2;
    }
    
    .kpi-delta {
        font-size: 0.7rem;
        margin-top: 6px;
    }
    
    .delta-positive {
        color: #2DD4A0;
    }
    
    .delta-negative {
        color: #FF5E7A;
    }
    
    /* Insight Box */
    .insight-card {
        background: linear-gradient(135deg, #131A26 0%, #0F151F 100%);
        border-radius: 12px;
        padding: 1.25rem;
        border-left: 4px solid #F5A623;
        margin: 1rem 0;
    }
    
    .insight-title {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #F5A623;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .insight-text {
        font-size: 0.85rem;
        color: #CCDDFF;
        line-height: 1.6;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #E6EDF3;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1E2D3D;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #0B0F18;
    }
    
    /* Metric boxes */
    .metric-box {
        background: #131A26;
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        border: 1px solid #1E2D3D;
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #00D4B4;
    }
    
    .metric-label {
        font-size: 0.65rem;
        color: #6B7B8D;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Load data with error handling
@st.cache_data
def load_data():
    possible_paths = ["wealth_data.csv", "data/wealth_data.csv", "./wealth_data.csv", "./data/wealth_data.csv"]
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df
    st.error("Data file not found. Please ensure wealth_data.csv is in the correct location.")
    st.stop()

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown("### Analysis Controls")
    year_range = st.slider(
        "Select Year Range",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(2010, 2025),
        step=1
    )
    
    st.markdown("---")
    st.markdown("### Data Quality Legend")
    st.markdown("🔵 **Real**: Direct source (AMFI, SEBI, World Bank, CFA)")
    st.markdown("🟡 **Interpolated**: Linear between real anchors")
    st.markdown("🔴 **Estimated**: Backward extrapolation (2010-2014)")
    
    st.markdown("---")
    st.markdown("### Research Context")
    st.markdown("""
    **Key Question:**  
    How do financial advisors, literacy, and trust drive wealth growth in India?
    
    **Time Period:** 2010-2025 (16 years)
    
    **Data Sources:**  
    AMFI · SEBI · World Bank · CFA Institute
    """)
    
    st.markdown("---")
    st.markdown("**Ronit Kapoor** | MS25GF125")
    st.markdown("Global Finance | SP Jain")

filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# Main header
st.markdown('<div class="main-header">The Role of Financial Advisors in Wealth Management</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">India | 2010–2025 | 16-Year Panel Dataset | Regression Analysis & Elasticity Modeling</div>', unsafe_allow_html=True)

# KPI Row
latest = filtered_df[filtered_df["Year"] == filtered_df["Year"].max()].iloc[0]
first = filtered_df[filtered_df["Year"] == filtered_df["Year"].min()].iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    aum_growth = (latest['AUM_Crore']/first['AUM_Crore'] - 1)*100
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">TOTAL AUM</div>
        <div class="kpi-value">₹{latest['AUM_Crore']/100000:.2f}L Cr</div>
        <div class="kpi-delta delta-positive">▲ {aum_growth:.0f}% since 2010</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    folio_growth = (latest['Folios_Crore']/first['Folios_Crore'] - 1)*100
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">INVESTOR FOLIOS</div>
        <div class="kpi-value">{latest['Folios_Crore']:.2f} Cr</div>
        <div class="kpi-delta delta-positive">▲ {folio_growth:.0f}% since 2010</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    literacy_gain = latest['Literacy'] - first['Literacy']
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">FINANCIAL LITERACY</div>
        <div class="kpi-value">{latest['Literacy']} / 100</div>
        <div class="kpi-delta delta-positive">▲ +{literacy_gain} pts since 2010</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    trust_gain = latest['Trust_Percent'] - first['Trust_Percent']
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">TRUST IN ADVISORS</div>
        <div class="kpi-value">{latest['Trust_Percent']}%</div>
        <div class="kpi-delta delta-positive">▲ +{trust_gain} pp since 2010</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    peak_advisors = filtered_df['Advisors'].max()
    peak_year = filtered_df[filtered_df['Advisors'] == peak_advisors]['Year'].values[0]
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">REGISTERED ADVISORS</div>
        <div class="kpi-value">{latest['Advisors']:,.0f}</div>
        <div class="kpi-delta delta-negative">Peak: {peak_advisors:,.0f} ({peak_year})</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Key Insight Banner
st.markdown("""
<div class="insight-card">
    <div class="insight-title">RESEARCH THESIS</div>
    <div class="insight-text">
    <strong>India's wealth management transformation (2010-2025) is driven by three interconnected forces:</strong> 
    rising financial literacy (27 → 63), growing trust in advisors (58% → 91%), and regulatory evolution that prioritizes 
    advisor quality over quantity. The post-2020 decline in registered advisors (-15.5%) paired with 158% AUM growth 
    reveals a fundamental shift: <strong>trust and competence now matter more than headcount.</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# SECTION 1: Growth Trends
st.markdown('<div class="section-header">Wealth Management Ecosystem Growth (2010–2025)</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Absolute Values", "Indexed Growth", "YoY Change", "Advisor Paradox"])

with tab1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=filtered_df["Year"], y=filtered_df["AUM_Crore"]/100000,
        mode="lines+markers", name="AUM (₹ Lakh Cr)",
        line=dict(color="#00D4B4", width=3), marker=dict(size=8, symbol="circle")
    ))
    fig1.add_trace(go.Scatter(
        x=filtered_df["Year"], y=filtered_df["Folios_Crore"],
        mode="lines+markers", name="Folios (Crore)",
        line=dict(color="#4B9EFF", width=3), marker=dict(size=8, symbol="square"),
        yaxis="y2"
    ))
    fig1.update_layout(
        title="AUM and Folios Growth (2010-2025)",
        title_font=dict(size=14, color="#E6EDF3"),
        xaxis=dict(title="Year", showgrid=True, gridcolor="#1E2D3D", tickmode="linear"),
        yaxis=dict(title="AUM (₹ Lakh Crore)", showgrid=True, gridcolor="#1E2D3D", color="#00D4B4"),
        yaxis2=dict(title="Folios (Crore)", overlaying="y", side="right", color="#4B9EFF"),
        template="plotly_dark",
        height=450,
        hovermode="x unified",
        plot_bgcolor="#0B0F18",
        paper_bgcolor="#0B0F18"
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    indexed = filtered_df.copy()
    for col in ["AUM_Crore", "Folios_Crore", "Literacy", "Trust_Percent", "Advisors"]:
        indexed[col + "_index"] = (indexed[col] / indexed[col].iloc[0]) * 100
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["AUM_Crore_index"], mode="lines+markers", name="AUM", line=dict(color="#00D4B4", width=2.5)))
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["Folios_Crore_index"], mode="lines+markers", name="Folios", line=dict(color="#4B9EFF", width=2.5)))
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["Literacy_index"], mode="lines+markers", name="Financial Literacy", line=dict(color="#F5A623", width=2.5)))
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["Trust_Percent_index"], mode="lines+markers", name="Trust in Advisors", line=dict(color="#8B7CF6", width=2.5)))
    fig2.add_trace(go.Scatter(x=indexed["Year"], y=indexed["Advisors_index"], mode="lines+markers", name="Registered Advisors", line=dict(color="#FF5E7A", width=2.5, dash="dash")))
    fig2.update_layout(
        title="Indexed Growth (2010 = 100)",
        title_font=dict(size=14, color="#E6EDF3"),
        xaxis=dict(title="Year", showgrid=True, gridcolor="#1E2D3D"),
        yaxis=dict(title="Index (2010 = 100)", showgrid=True, gridcolor="#1E2D3D"),
        template="plotly_dark",
        height=450,
        hovermode="x unified",
        plot_bgcolor="#0B0F18",
        paper_bgcolor="#0B0F18"
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    yoy = filtered_df.copy()
    for col in ["AUM_Crore", "Folios_Crore", "Literacy", "Trust_Percent"]:
        yoy[col + "_yoy"] = yoy[col].pct_change() * 100
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=yoy["Year"], y=yoy["AUM_Crore_yoy"], name="AUM Growth %", marker_color="#00D4B4", opacity=0.8))
    fig3.add_trace(go.Scatter(x=yoy["Year"], y=yoy["Literacy_yoy"], mode="lines+markers", name="Literacy Growth (pp)", line=dict(color="#F5A623", width=2.5), yaxis="y2"))
    fig3.update_layout(
        title="Year-over-Year Growth Rates",
        title_font=dict(size=14, color="#E6EDF3"),
        xaxis=dict(title="Year", showgrid=True, gridcolor="#1E2D3D"),
        yaxis=dict(title="AUM Growth (%)", showgrid=True, gridcolor="#1E2D3D", color="#00D4B4"),
        yaxis2=dict(title="Literacy Growth (percentage points)", overlaying="y", side="right", color="#F5A623"),
        template="plotly_dark",
        height=450,
        hovermode="x unified",
        plot_bgcolor="#0B0F18",
        paper_bgcolor="#0B0F18"
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    fig5 = make_subplots(specs=[[{"secondary_y": True}]])
    fig5.add_trace(go.Scatter(
        x=filtered_df["Year"], y=filtered_df["AUM_Crore"]/100000,
        mode="lines+markers", name="AUM (₹ Lakh Cr)",
        line=dict(color="#00D4B4", width=3), marker=dict(size=9)
    ), secondary_y=False)
    fig5.add_trace(go.Scatter(
        x=filtered_df["Year"], y=filtered_df["Advisors"],
        mode="lines+markers", name="Registered Advisors",
        line=dict(color="#FF5E7A", width=3, dash="dash"), marker=dict(size=9, symbol="diamond")
    ), secondary_y=True)
    fig5.update_layout(
        title="The Advisor Paradox: AUM Up, Advisor Count Down (Post-2020)",
        title_font=dict(size=14, color="#E6EDF3"),
        xaxis=dict(title="Year", showgrid=True, gridcolor="#1E2D3D"),
        template="plotly_dark",
        height=450,
        hovermode="x unified",
        plot_bgcolor="#0B0F18",
        paper_bgcolor="#0B0F18"
    )
    fig5.update_yaxes(title_text="AUM (₹ Lakh Crore)", secondary_y=False, color="#00D4B4", showgrid=True, gridcolor="#1E2D3D")
    fig5.update_yaxes(title_text="Number of Registered Advisors", secondary_y=True, color="#FF5E7A")
    st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">INSIGHT: THE ADVISOR PARADOX</div>
        <div class="insight-text">
        <strong>From 2020 to 2025:</strong> Registered advisors fell 15.5% (1,100 → 930) due to SEBI's stricter 2020 Investment Adviser Regulations. 
        Yet AUM grew 158% (₹31L Cr → ₹80L Cr). This confirms that <strong>advisor quality, trust, and regulatory compliance now drive wealth growth</strong> — not headcount.
        </div>
    </div>
    """, unsafe_allow_html=True)

# SECTION 2: Correlation Analysis
st.markdown('<div class="section-header">Driver Analysis: What Actually Drives Wealth Growth?</div>', unsafe_allow_html=True)

col_corr1, col_corr2 = st.columns([2, 1])

with col_corr1:
    corr_cols = ["AUM_Crore", "Folios_Crore", "Literacy", "Trust_Percent", "Advisors"]
    corr_matrix = filtered_df[corr_cols].corr()
    
    fig4 = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="Tealgrn",
        aspect="auto",
        title="Pearson Correlation Matrix (2010-2025)"
    )
    fig4.update_layout(
        template="plotly_dark",
        height=500,
        title_font=dict(size=14, color="#E6EDF3"),
        plot_bgcolor="#0B0F18",
        paper_bgcolor="#0B0F18"
    )
    st.plotly_chart(fig4, use_container_width=True)

with col_corr2:
    st.markdown("""
    <div class="metric-box" style="margin-bottom: 1rem;">
        <div class="metric-value">r = 0.962</div>
        <div class="metric-label">Literacy ↔ AUM</div>
        <div style="font-size:0.7rem; color:#2DD4A0;">Strongest driver</div>
    </div>
    <div class="metric-box" style="margin-bottom: 1rem;">
        <div class="metric-value">r = 0.935</div>
        <div class="metric-label">Trust ↔ AUM</div>
        <div style="font-size:0.7rem; color:#2DD4A0;">Nearly as powerful</div>
    </div>
    <div class="metric-box" style="margin-bottom: 1rem;">
        <div class="metric-value">r = 0.993</div>
        <div class="metric-label">Literacy ↔ Trust</div>
        <div style="font-size:0.7rem; color:#F5A623;">Move almost perfectly together</div>
    </div>
    <div class="metric-box">
        <div class="metric-value">r = 0.766</div>
        <div class="metric-label">Advisors ↔ AUM</div>
        <div style="font-size:0.7rem; color:#FF5E7A;">Moderate (post-2020 decline)</div>
    </div>
    """, unsafe_allow_html=True)

# SECTION 3: Elasticity Calculator (THE EXTRA FEATURE)
st.markdown('<div class="section-header">Strategic Tool: Literacy-to-AUM Elasticity Calculator</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-card">
    <div class="insight-title">FROM YOUR REGRESSION ANALYSIS</div>
    <div class="insight-text">
    <strong>Log-Log Elasticity = 2.8245</strong><br>
    Interpretation: A 1% increase in Financial Literacy Score is associated with a 2.82% increase in Total Mutual Fund AUM.<br>
    <strong>R² = 0.9913</strong> | p < 0.001 | This is the strongest driver in your model.
    </div>
</div>
""", unsafe_allow_html=True)

col_elast1, col_elast2, col_elast3 = st.columns([1, 1, 1])

with col_elast1:
    current_lit = latest["Literacy"]
    target_lit = st.slider(
        "Target Literacy Score (0-100)",
        min_value=int(current_lit),
        max_value=100,
        value=min(int(current_lit) + 10, 100),
        step=1
    )
    
    lit_change_pct = ((target_lit - current_lit) / current_lit) * 100
    aum_change_pct = lit_change_pct * 2.8245
    projected_aum = latest["AUM_Crore"] * (1 + aum_change_pct / 100)
    
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Current Literacy (2025)</div>
        <div class="metric-value">{current_lit}</div>
    </div>
    """, unsafe_allow_html=True)

with col_elast2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Literacy Change</div>
        <div class="metric-value" style="color:#F5A623;">{lit_change_pct:+.1f}%</div>
        <div style="font-size:0.7rem;">{current_lit} → {target_lit}</div>
    </div>
    <div class="metric-box" style="margin-top: 1rem;">
        <div class="metric-label">Projected AUM Impact</div>
        <div class="metric-value" style="color:#00D4B4;">{aum_change_pct:+.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col_elast3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Current AUM (2025)</div>
        <div class="metric-value">₹{latest['AUM_Crore']/100000:.2f}L Cr</div>
    </div>
    <div class="metric-box" style="margin-top: 1rem;">
        <div class="metric-label">Projected AUM</div>
        <div class="metric-value" style="color:#00D4B4;">₹{projected_aum/100000:.2f}L Cr</div>
    </div>
    """, unsafe_allow_html=True)

# SECTION 4: Regression Summary
st.markdown('<div class="section-header">Regression Output Summary</div>', unsafe_allow_html=True)

reg_col1, reg_col2, reg_col3 = st.columns(3)

with reg_col1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">SIMPLE LINEAR</div>
        <div class="metric-value">R² = 0.9259</div>
        <div style="font-size:0.7rem;">AUM ~ Literacy</div>
        <div style="font-size:0.65rem; color:#6B7B8D; margin-top:5px;">Literacy alone explains 92.6% of AUM variance</div>
    </div>
    """, unsafe_allow_html=True)

with reg_col2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">MULTIPLE LINEAR</div>
        <div class="metric-value">R² = 0.9964</div>
        <div style="font-size:0.7rem;">AUM ~ Literacy + Trust + Advisors</div>
        <div style="font-size:0.65rem; color:#6B7B8D; margin-top:5px;">Adj. R² = 0.9955 | F = 1097.16</div>
    </div>
    """, unsafe_allow_html=True)

with reg_col3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">LOG-LOG ELASTICITY</div>
        <div class="metric-value">β = 2.8245</div>
        <div style="font-size:0.7rem;">ln(AUM) ~ ln(Literacy)</div>
        <div style="font-size:0.65rem; color:#6B7B8D; margin-top:5px;">R² = 0.9913 | t = 39.9</div>
    </div>
    """, unsafe_allow_html=True)

# SECTION 5: Data Quality
st.markdown('<div class="section-header">Data Quality & Limitations</div>', unsafe_allow_html=True)

status_colors = {"Real": "#2DD4A0", "Interpolated": "#F5A623", "Estimated": "#FF5E7A"}
status_df = filtered_df[["Year", "Data_Status"]].copy()

fig6 = go.Figure()
for status, color in status_colors.items():
    subset = status_df[status_df["Data_Status"] == status]
    fig6.add_trace(go.Scatter(
        x=subset["Year"], y=[1]*len(subset),
        mode="markers", marker=dict(size=14, color=color, symbol="circle"),
        name=status
    ))
fig6.update_layout(
    title="Data Quality by Year",
    title_font=dict(size=14, color="#E6EDF3"),
    xaxis=dict(title="Year", tickmode="linear", showgrid=True, gridcolor="#1E2D3D"),
    yaxis=dict(showticklabels=False, showgrid=False),
    showlegend=True,
    template="plotly_dark",
    height=200,
    plot_bgcolor="#0B0F18",
    paper_bgcolor="#0B0F18"
)
st.plotly_chart(fig6, use_container_width=True)

st.markdown("""
<div class="insight-card">
    <div class="insight-title">LIMITATIONS ACKNOWLEDGED</div>
    <div class="insight-text">
    • <strong>2010-2014 values are estimated</strong> (backward extrapolation from 2015 anchors)<br>
    • <strong>Trust variable has only one real anchor</strong> (2025 CFA Institute survey; earlier years estimated)<br>
    • <strong>Multicollinearity present</strong> (Literacy, Trust, Advisors all r > 0.90)<br>
    • <strong>Associations only, not causation</strong> — time-series regression cannot establish causal direction<br>
    • <strong>Secondary data only</strong> — no primary survey or individual-level advisor-client data
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Data sources: AMFI (AUM, Folios) | SEBI (Registered Advisors) | World Bank Global Findex (Financial Literacy) | CFA Institute Global Graduate Outlook Survey 2025 (Trust in Advisors)")
