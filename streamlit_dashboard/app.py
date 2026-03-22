"""
AQI Double Jeopardy Dashboard - Consolidated Single-Page App with Top Navigation
Datathon 2026 - Professional Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
import os
import re

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="AQI Double Jeopardy Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# CUSTOM CSS - Professional Climate Justice Theme + Hide Sidebar
# =============================================================================
st.markdown("""
<style>
    /* ========== HIDE SIDEBAR ========== */
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* ========== GLOBAL STYLES ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ========== TYPOGRAPHY ========== */
    h1 {
        color: #0f172a;
        font-weight: 700;
        font-size: 2.25rem !important;
        letter-spacing: -0.025em;
        margin-bottom: 0.5rem !important;
        line-height: 1.2;
    }

    h2 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.5rem !important;
        letter-spacing: -0.01em;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        color: #334155;
        font-weight: 600;
        font-size: 1.125rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }

    h4 {
        color: #475569;
        font-weight: 600;
        font-size: 1rem !important;
    }

    p, li {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ========== MAIN CONTENT ========== */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    /* ========== METRIC CARDS ========== */
    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }

    div[data-testid="metric-container"]:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 8px 24px rgba(0,0,0,0.04);
        transform: translateY(-1px);
    }

    div[data-testid="metric-container"] label {
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.75rem !important;
    }

    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }

    /* ========== CARDS & CONTAINERS ========== */
    .info-card {
        background: white;
        border-radius: 16px;
        padding: 28px 32px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }

    .info-card h4 {
        margin-top: 0 !important;
        margin-bottom: 16px !important;
        padding-bottom: 12px;
        border-bottom: 1px solid #f1f5f9;
    }

    .callout-box {
        background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 0 16px 16px 0;
        padding: 24px 28px;
        margin: 20px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }

    .callout-box strong {
        color: #1e40af;
    }

    .callout-box-orange {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .callout-box-orange strong {
        color: #c2410c;
    }

    .callout-box-red {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        border-left: 4px solid #dc2626;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .callout-box-red strong {
        color: #b91c1c;
    }

    .callout-box-purple {
        background: linear-gradient(135deg, #faf5ff 0%, #e9d5ff 100%);
        border-left: 4px solid #8b5cf6;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .callout-box-purple strong {
        color: #7c3aed;
    }

    .callout-box-teal {
        background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%);
        border-left: 4px solid #14b8a6;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .callout-box-teal strong {
        color: #0f766e;
    }

    .warning-box {
        background: linear-gradient(135deg, #fff7ed 0%, #fef2f2 100%);
        border-left: 4px solid #f97316;
        border-radius: 0 16px 16px 0;
        padding: 24px 28px;
        margin: 20px 0;
    }

    .warning-box strong {
        color: #c2410c;
    }

    .success-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid #22c55e;
        border-radius: 0 16px 16px 0;
        padding: 24px 28px;
        margin: 20px 0;
    }

    .success-box strong {
        color: #16a34a;
    }

    /* ========== FORM ELEMENTS ========== */
    .stSelectbox > div > div {
        border-radius: 10px;
        border-color: #e2e8f0;
        background: white;
    }

    .stSelectbox > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    .stSlider > div > div {
        color: #3b82f6;
    }

    .stSlider [data-baseweb="slider"] {
        margin-top: 8px;
    }

    /* ========== EXPANDER ========== */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        font-weight: 500;
        color: #334155;
    }

    .streamlit-expanderContent {
        border: 1px solid #e2e8f0;
        border-top: none;
        border-radius: 0 0 12px 12px;
        background: white;
    }

    /* ========== DATAFRAME ========== */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    /* ========== FOOTER ========== */
    .footer {
        text-align: center;
        padding: 32px 24px;
        color: #64748b;
        font-size: 0.85rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 64px;
        background: white;
        border-radius: 16px 16px 0 0;
    }

    .footer strong {
        color: #475569;
    }

    /* ========== SECTION ELEMENTS ========== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #e2e8f0 20%, #e2e8f0 80%, transparent 100%);
        margin: 32px 0;
    }

    .section-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* ========== PLOTLY CHART CONTAINER ========== */
    .stPlotlyChart {
        background: white;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    /* ========== PAGE HEADER ========== */
    .page-header {
        margin-bottom: 8px;
    }

    .page-header h1 {
        margin-bottom: 4px !important;
    }

    .page-subtitle {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }

    /* ========== FILTER SECTION ========== */
    .filter-section {
        background: white;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def page_header(title, subtitle=None, icon=""):
    if subtitle:
        st.markdown(f"""
        <div class="page-header">
            <h1>{icon} {title}</h1>
            <p class="page-subtitle">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"# {icon} {title}")


def section_label(text):
    st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)


def section_divider():
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# =============================================================================
# DATA LOADING - Cached for performance
# =============================================================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.dirname(current_dir)

    file_paths = [
        os.path.join(data_dir, "annual_aqi_by_county_2021.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2022.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2023.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2024.csv"),
    ]

    df_list = []
    for file in file_paths:
        if os.path.exists(file):
            current_df = pd.read_csv(file)
            match = re.search(r'(\d{4})\.csv', file)
            if match:
                current_df['Year'] = int(match.group(1))
            df_list.append(current_df)

    if not df_list:
        st.error("No data files found. Please ensure CSV files are in the parent directory.")
        return pd.DataFrame()

    return pd.concat(df_list, ignore_index=True)


@st.cache_data
def compute_county_stats(df):
    county_stats = df.groupby(['State', 'County']).agg({
        'Median AQI': 'mean',
        'Max AQI': 'mean'
    }).reset_index()
    county_stats.columns = ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']
    return county_stats


@st.cache_data
def compute_double_jeopardy(county_stats, percentile=90):
    median_threshold = county_stats['mean_median_aqi'].quantile(percentile / 100)
    max_threshold = county_stats['mean_max_aqi'].quantile(percentile / 100)

    stats = county_stats.copy()
    stats['Risk_Category'] = 'Low Risk'
    stats.loc[(stats['mean_median_aqi'] >= median_threshold), 'Risk_Category'] = 'High Chronic'
    stats.loc[(stats['mean_max_aqi'] >= max_threshold), 'Risk_Category'] = 'High Acute'
    stats.loc[(stats['mean_median_aqi'] >= median_threshold) &
              (stats['mean_max_aqi'] >= max_threshold), 'Risk_Category'] = 'Double Jeopardy'

    return stats, median_threshold, max_threshold


# =============================================================================
# LOAD DATA
# =============================================================================
df = load_data()
if df.empty:
    st.stop()

county_stats = compute_county_stats(df)

# =============================================================================
# TOP NAVIGATION BAR
# =============================================================================
selected = option_menu(
    menu_title=None,
    options=["Overview", "Chronic Pollution", "Extreme Spikes", "Double Jeopardy", "Severity Score", "County Drilldown", "Download Data"],
    icons=["globe", "bar-chart-fill", "lightning-charge-fill", "bullseye", "graph-up", "search", "download"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "#1e293b",
            "border-radius": "12px",
            "margin-bottom": "24px",
        },
        "icon": {"color": "#94a3b8", "font-size": "14px"},
        "nav-link": {
            "font-size": "13px",
            "text-align": "center",
            "margin": "0px",
            "padding": "12px 16px",
            "color": "#cbd5e1",
            "font-family": "Inter, sans-serif",
            "font-weight": "500",
            "--hover-color": "#334155",
        },
        "nav-link-selected": {
            "background-color": "#3b82f6",
            "color": "white",
            "font-weight": "600",
            "border-radius": "8px",
        },
    },
)


# =============================================================================
# PAGE 0: OVERVIEW
# =============================================================================
def render_overview():
    page_header("Air Quality Double Jeopardy Dashboard",
                "Identifying Communities Facing Chronic AND Acute Pollution Burden", "🌍")

    st.markdown("""
    <div class="callout-box">
    <strong>Project Summary:</strong> This dashboard analyzes EPA Air Quality Index data from 2021-2024 
    to identify U.S. counties experiencing <em>Double Jeopardy</em>—communities suffering from both 
    persistently poor daily air quality AND dangerous pollution spikes. These areas require 
    priority intervention for environmental justice.
    </div>
    """, unsafe_allow_html=True)

    section_divider()

    # Controls
    st.markdown('<p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;">Controls</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        year_range = st.slider(
            "Year Range to Include",
            min_value=2021, max_value=2024, value=(2021, 2024), step=1,
            help="Select which years of data to include in the analysis",
            key="overview_year_range"
        )

    with col2:
        all_states = sorted(county_stats['State'].unique().tolist())
        all_states.insert(0, 'All States')
        selected_state = st.selectbox("Filter by State", all_states, index=0, key="overview_state")

    with col3:
        top_n = st.slider("Top N for Bar Chart", min_value=5, max_value=25, value=10, step=1, key="overview_top_n")

    year_min, year_max = year_range
    df_filtered = df[(df['Year'] >= year_min) & (df['Year'] <= year_max)].copy()

    county_stats_filtered = df_filtered.groupby(['State', 'County']).agg({
        'Median AQI': 'mean',
        'Max AQI': 'mean'
    }).reset_index()
    county_stats_filtered.columns = ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']

    if selected_state != 'All States':
        county_stats_display = county_stats_filtered[county_stats_filtered['State'] == selected_state].copy()
    else:
        county_stats_display = county_stats_filtered.copy()

    stats_with_risk, median_thresh, max_thresh = compute_double_jeopardy(county_stats_display)
    double_jeopardy_count = len(stats_with_risk[stats_with_risk['Risk_Category'] == 'Double Jeopardy'])

    section_divider()

    # KPI Cards
    st.markdown('<p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;">Key Metrics at a Glance</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    total_counties = len(county_stats_display)

    with col1:
        st.metric(label="Total Counties Analyzed", value=f"{total_counties:,}")
    with col2:
        years_text = f"{year_min}-{year_max}" if year_min != year_max else str(year_min)
        st.metric(label="Year Range", value=years_text, help="Currently analyzing data from selected year range")
    with col3:
        pct = f"{(double_jeopardy_count/total_counties*100):.1f}% of total" if total_counties > 0 else "0%"
        st.metric(label="Double Jeopardy Counties", value=f"{double_jeopardy_count}", delta=pct)
    with col4:
        if selected_state != 'All States':
            st.metric(label="Geographic Filter", value=selected_state, help=f"Filtered to show only {selected_state} counties")
        else:
            st.metric(label="Geographic Filter", value="All States", help="Showing data for all states")

    section_divider()

    # Double Jeopardy Definition
    st.markdown('<h3 style="margin-top: 0;">🎯 How We Define Double Jeopardy</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="info-card">
        <h4 style="color: #dc2626; margin-top: 0; border-bottom: 1px solid #fef2f2; padding-bottom: 12px;">Double Jeopardy = High Chronic + High Acute</h4>
        <p>A county qualifies as <strong>Double Jeopardy</strong> if it meets BOTH criteria:</p>
        <ul>
            <li><strong>High Chronic Exposure:</strong> 4-year average Median AQI ≥ 90th percentile<br>
            <span style="color: #64748b; font-size: 0.9rem;">→ Persistent daily pollution burden affecting long-term health</span></li>
            <br>
            <li><strong>High Acute Exposure:</strong> 4-year average Max AQI ≥ 90th percentile<br>
            <span style="color: #64748b; font-size: 0.9rem;">→ Dangerous pollution spikes causing immediate health risks</span></li>
        </ul>
        <p style="margin-bottom: 0;"><strong>Why it matters:</strong> These communities face a compounding health burden—
        their residents never get relief from poor air quality AND face periodic dangerous episodes.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        risk_counts = stats_with_risk['Risk_Category'].value_counts()
        fig_pie = go.Figure(data=[go.Pie(
            labels=risk_counts.index, values=risk_counts.values, hole=0.5,
            marker_colors=['#48bb78', '#ecc94b', '#ed8936', '#c53030'],
            textinfo='percent+label', textposition='outside'
        )])
        fig_pie.update_layout(
            title=dict(text="Risk Category Distribution", font_size=14),
            showlegend=False, margin=dict(t=60, b=20, l=20, r=20),
            height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    section_divider()

    # Thresholds
    st.markdown('<p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;">Current Thresholds</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="info-card" style="text-align: center;">
            <h4 style="color: #2563eb; margin: 0; border: none; padding: 0;">Chronic Threshold</h4>
            <p style="font-size: 2.25rem; font-weight: 700; color: #0f172a; margin: 12px 0 8px 0;">{median_thresh:.1f}</p>
            <p style="color: #64748b; margin: 0; font-size: 0.85rem;">90th percentile Mean Median AQI</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="info-card" style="text-align: center;">
            <h4 style="color: #ea580c; margin: 0; border: none; padding: 0;">Acute Threshold</h4>
            <p style="font-size: 2.25rem; font-weight: 700; color: #0f172a; margin: 12px 0 8px 0;">{max_thresh:.1f}</p>
            <p style="color: #64748b; margin: 0; font-size: 0.85rem;">90th percentile Mean Max AQI</p>
        </div>
        """, unsafe_allow_html=True)

    section_divider()

    # Scatter plot
    st.markdown('<h3 style="margin-top: 0;">🗺️ Double Jeopardy Overview</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; font-size: 0.9rem; margin-top: -8px; margin-bottom: 16px;">Interactive scatter plot showing all counties by chronic vs. acute pollution levels</p>', unsafe_allow_html=True)

    color_map = {'Low Risk': '#48bb78', 'High Chronic': '#ecc94b', 'High Acute': '#ed8936', 'Double Jeopardy': '#c53030'}

    fig_scatter = px.scatter(
        stats_with_risk, x='mean_median_aqi', y='mean_max_aqi', color='Risk_Category',
        color_discrete_map=color_map, hover_name='County',
        hover_data={'State': True, 'mean_median_aqi': ':.1f', 'mean_max_aqi': ':.1f', 'Risk_Category': True},
        labels={'mean_median_aqi': 'Mean Median AQI (Chronic)', 'mean_max_aqi': 'Mean Max AQI (Acute)', 'Risk_Category': 'Risk Category'},
        category_orders={'Risk_Category': ['Low Risk', 'High Chronic', 'High Acute', 'Double Jeopardy']}
    )

    fig_scatter.add_hline(y=max_thresh, line_dash="dash", line_color="#dd6b20",
                          annotation_text="Acute Threshold", annotation_position="top right")
    fig_scatter.add_vline(x=median_thresh, line_dash="dash", line_color="#3182ce",
                          annotation_text="Chronic Threshold", annotation_position="top right")

    fig_scatter.update_layout(
        height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white',
        font=dict(family="Inter, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(t=80, b=40)
    )
    fig_scatter.update_xaxes(gridcolor='#e2e8f0', zeroline=False)
    fig_scatter.update_yaxes(gridcolor='#e2e8f0', zeroline=False)

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("""
    <div class="callout-box">
    <strong>💡 How to read this chart:</strong> Each dot represents a U.S. county. Counties in the 
    <span style="color: #dc2626; font-weight: 600;">upper-right quadrant (red)</span> face Double Jeopardy—
    they have both high daily pollution levels AND dangerous pollution spikes. Use the top navigation to 
    explore detailed analysis of each risk dimension.
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p style="margin: 0 0 8px 0;"><strong>Data Source:</strong> EPA Air Quality Index Annual Summary (2021-2024)</p>
        <p style="margin: 0; color: #94a3b8;"><strong>Built for:</strong> Datathon 2026 &nbsp;|&nbsp; <strong>Framework:</strong> Streamlit + Plotly</p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PAGE 1: CHRONIC POLLUTION
# =============================================================================
def render_chronic_pollution():
    page_header("Chronic Pollution Analysis", "Top Counties by Mean Median AQI (2021-2024)", "📊")

    st.markdown("""
    <div class="callout-box">
    <strong>What is Chronic Pollution?</strong> The Median AQI represents the <em>typical daily air quality</em> 
    a resident experiences. A high average Median AQI over 4 years indicates persistent, day-in-day-out 
    pollution exposure—the "daily grind" that affects long-term respiratory and cardiovascular health.
    </div>
    """, unsafe_allow_html=True)

    section_divider()
    section_label("Filters")

    col1, col2 = st.columns(2)
    with col1:
        states = ['All States'] + sorted(county_stats['State'].unique().tolist())
        selected_state = st.selectbox("Select State", states, key="chronic_state")
    with col2:
        top_n = st.slider("Show Top N Counties", min_value=10, max_value=50, value=15, step=5, key="chronic_topn")

    if selected_state != 'All States':
        filtered_stats = county_stats[county_stats['State'] == selected_state].copy()
    else:
        filtered_stats = county_stats.copy()

    chronic_top = filtered_stats.sort_values('mean_median_aqi', ascending=False).head(top_n)

    section_divider()
    section_label(f"Top {top_n} Counties by Chronic Pollution")

    fig = px.bar(
        chronic_top.sort_values('mean_median_aqi', ascending=False),
        x='mean_median_aqi', y='County', color='State', orientation='h',
        hover_data={'State': True, 'mean_median_aqi': ':.1f', 'mean_max_aqi': ':.1f'},
        labels={'mean_median_aqi': 'Average Median AQI (Daily Exposure)', 'County': '', 'State': 'State'},
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.update_layout(
        height=max(400, top_n * 28), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=""),
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis_title="Average Median AQI (Daily Exposure)", yaxis_title=""
    )
    fig.update_xaxes(gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0')
    fig.update_yaxes(gridcolor='#e2e8f0')
    st.plotly_chart(fig, use_container_width=True)

    if len(chronic_top) > 0:
        worst_county = chronic_top.iloc[0]
        st.markdown(f"""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #2563eb; border-bottom: 1px solid #eff6ff; padding-bottom: 12px;">💡 What This Means</h4>
        <p><strong>{worst_county['County']}, {worst_county['State']}</strong> has the highest chronic pollution 
        burden with an average Median AQI of <strong>{worst_county['mean_median_aqi']:.1f}</strong> over 2021-2024.</p>
        <p style="margin-bottom: 0;">Counties with high Median AQI experience poor air quality as their <em>norm</em>—residents breathe 
        moderately unhealthy air on a typical day, leading to cumulative health impacts over time including 
        increased rates of asthma, cardiovascular disease, and reduced life expectancy.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📋 View Data Table"):
        display_df = chronic_top[['County', 'State', 'mean_median_aqi', 'mean_max_aqi']].copy()
        display_df.columns = ['County', 'State', 'Mean Median AQI', 'Mean Max AQI']
        display_df = display_df.round(1)
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(display_df, use_container_width=True)


# =============================================================================
# PAGE 2: EXTREME SPIKES
# =============================================================================
def render_extreme_spikes():
    page_header("Extreme Pollution Spikes", "Top Counties by Mean Max AQI (2021-2024)", "⚡")

    st.markdown("""
    <div class="callout-box-orange">
    <strong>What are Extreme Spikes?</strong> The Max AQI represents the <em>worst single day</em> of air quality 
    each year. A high average Max AQI over 4 years indicates a county prone to dangerous pollution episodes—
    from wildfires, industrial accidents, or severe inversions—that pose immediate health emergencies.
    </div>
    """, unsafe_allow_html=True)

    section_divider()
    section_label("Filters")

    col1, col2, col3 = st.columns(3)
    with col1:
        states = ['All States'] + sorted(county_stats['State'].unique().tolist())
        selected_state = st.selectbox("Select State", states, key="acute_state")
    with col2:
        top_n = st.slider("Show Top N Counties", min_value=10, max_value=50, value=15, step=5, key="acute_topn")
    with col3:
        outlier_handling = st.selectbox(
            "Outlier Handling", ["None", "Cap at 500", "Winsorize Top 1%"],
            help="Extreme Max AQI values (often from wildfires) can skew visualizations"
        )

    if selected_state != 'All States':
        filtered_stats = county_stats[county_stats['State'] == selected_state].copy()
    else:
        filtered_stats = county_stats.copy()

    display_stats = filtered_stats.copy()
    if outlier_handling == "Cap at 500":
        display_stats['mean_max_aqi_display'] = display_stats['mean_max_aqi'].clip(upper=500)
    elif outlier_handling == "Winsorize Top 1%":
        p99 = display_stats['mean_max_aqi'].quantile(0.99)
        display_stats['mean_max_aqi_display'] = display_stats['mean_max_aqi'].clip(upper=p99)
    else:
        display_stats['mean_max_aqi_display'] = display_stats['mean_max_aqi']

    acute_top = display_stats.sort_values('mean_max_aqi', ascending=False).head(top_n)

    section_divider()
    section_label(f"Top {top_n} Counties by Acute Pollution")

    fig = px.bar(
        acute_top.sort_values('mean_max_aqi_display', ascending=False),
        x='mean_max_aqi_display', y='County', color='State', orientation='h',
        hover_data={'State': True, 'mean_median_aqi': ':.1f', 'mean_max_aqi': ':.1f', 'mean_max_aqi_display': False},
        labels={'mean_max_aqi_display': 'Average Max AQI (Extreme Events)', 'County': '', 'State': 'State'},
        color_discrete_sequence=px.colors.sequential.Magma
    )
    fig.update_layout(
        height=max(400, top_n * 28), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=""),
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis_title="Average Max AQI (Extreme Events)", yaxis_title=""
    )
    fig.add_vline(x=150, line_dash="dash", line_color="#c53030",
                  annotation_text="Unhealthy (150)", annotation_position="top")
    fig.add_vline(x=300, line_dash="dash", line_color="#742a2a",
                  annotation_text="Hazardous (300)", annotation_position="top")
    fig.update_xaxes(gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0')
    fig.update_yaxes(gridcolor='#e2e8f0')
    st.plotly_chart(fig, use_container_width=True)

    if len(acute_top) > 0:
        worst_county = acute_top.iloc[0]
        st.markdown(f"""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #ea580c; border-bottom: 1px solid #fff7ed; padding-bottom: 12px;">💡 What This Means</h4>
        <p><strong>{worst_county['County']}, {worst_county['State']}</strong> has the highest acute pollution 
        burden with an average Max AQI of <strong>{worst_county['mean_max_aqi']:.1f}</strong> over 2021-2024.</p>
        <p>Counties with high Max AQI experience <em>dangerous pollution episodes</em>—days when air quality 
        becomes immediately hazardous. These spikes often trigger health emergencies, especially for 
        vulnerable populations like children, elderly, and those with respiratory conditions.</p>
        <p style="margin-bottom: 0;"><strong>Note:</strong> Values above 300 are "Hazardous"—everyone may experience serious health effects.</p>
        </div>
        """, unsafe_allow_html=True)

    if outlier_handling != "None":
        st.markdown("""
        <div class="callout-box-orange">
        <strong>⚠️ About Outliers:</strong> Some counties (especially in California and the Pacific Northwest) 
        have extreme Max AQI values exceeding 500+ due to wildfire smoke. While these values are real and 
        impactful, they can make it harder to see variation among other counties. The outlier handling 
        options help visualize the distribution while preserving the true values in the data table.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📋 View Data Table (True Values)"):
        display_df = acute_top[['County', 'State', 'mean_median_aqi', 'mean_max_aqi']].copy()
        display_df.columns = ['County', 'State', 'Mean Median AQI', 'Mean Max AQI']
        display_df = display_df.round(1)
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(display_df, use_container_width=True)


# =============================================================================
# PAGE 3: DOUBLE JEOPARDY (Vulnerability Profile)
# =============================================================================
def render_double_jeopardy():
    page_header("Vulnerability Profile Analysis",
                "Counties by Vulnerability (Chronic) vs Hazard (Acute) Scores", "🎯")

    st.markdown("""
    <div class="callout-box-red">
    <strong>Understanding the Vulnerability Profile:</strong> This analysis maps counties by their 
    <em>Vulnerability Score</em> (chronic daily pollution burden) versus <em>Hazard Score</em> (acute pollution events).
    Counties in the <strong>High Vulnerability / High Hazard</strong> quadrant face double jeopardy—
    they need <em>priority intervention</em> as they face the worst of both worlds.
    </div>
    """, unsafe_allow_html=True)

    section_divider()
    section_label("Controls")

    col1, col2, col3 = st.columns(3)
    with col1:
        percentile = st.slider(
            "Percentile Threshold", min_value=80, max_value=99, value=90, step=1,
            help="Counties above this percentile for BOTH metrics qualify as Double Jeopardy"
        )
    with col2:
        states = ['All States'] + sorted(county_stats['State'].unique().tolist())
        selected_state = st.selectbox("Filter by State", states, key="dj_state")
    with col3:
        top_n = st.slider("Top N for Bar Chart", min_value=5, max_value=25, value=10, step=5)

    if selected_state != 'All States':
        filtered_stats = county_stats[county_stats['State'] == selected_state].copy()
    else:
        filtered_stats = county_stats.copy()

    # Compute normalized scores
    stats_with_scores = filtered_stats.copy()
    min_median = stats_with_scores['mean_median_aqi'].min()
    max_median = stats_with_scores['mean_median_aqi'].max()
    min_max_val = stats_with_scores['mean_max_aqi'].min()
    max_max_val = stats_with_scores['mean_max_aqi'].max()

    if max_median != min_median:
        stats_with_scores['vulnerability_score'] = (stats_with_scores['mean_median_aqi'] - min_median) / (max_median - min_median)
    else:
        stats_with_scores['vulnerability_score'] = 0.5

    if max_max_val != min_max_val:
        stats_with_scores['hazard_score'] = (stats_with_scores['mean_max_aqi'] - min_max_val) / (max_max_val - min_max_val)
    else:
        stats_with_scores['hazard_score'] = 0.5

    mean_vuln = stats_with_scores['vulnerability_score'].mean()
    mean_hazard = stats_with_scores['hazard_score'].mean()

    stats_with_scores['risk_category'] = 'Low Risk'
    stats_with_scores.loc[(stats_with_scores['vulnerability_score'] >= mean_vuln) &
                          (stats_with_scores['hazard_score'] < mean_hazard), 'risk_category'] = 'High Vulnerability'
    stats_with_scores.loc[(stats_with_scores['vulnerability_score'] < mean_vuln) &
                          (stats_with_scores['hazard_score'] >= mean_hazard), 'risk_category'] = 'High Hazard'
    stats_with_scores.loc[(stats_with_scores['vulnerability_score'] >= mean_vuln) &
                          (stats_with_scores['hazard_score'] >= mean_hazard), 'risk_category'] = 'Double Jeopardy'

    stats_with_scores['severity_score'] = (stats_with_scores['vulnerability_score'] + stats_with_scores['hazard_score']) / 2
    stats_with_scores['Vulnerability_Rank'] = stats_with_scores['vulnerability_score'].rank(ascending=False).astype(int)
    stats_with_scores['Hazard_Rank'] = stats_with_scores['hazard_score'].rank(ascending=False).astype(int)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    dj_count = len(stats_with_scores[stats_with_scores['risk_category'] == 'Double Jeopardy'])
    high_vuln = len(stats_with_scores[stats_with_scores['risk_category'] == 'High Vulnerability'])
    high_hazard = len(stats_with_scores[stats_with_scores['risk_category'] == 'High Hazard'])
    low_risk = len(stats_with_scores[stats_with_scores['risk_category'] == 'Low Risk'])

    with col1:
        st.metric("🔴 Double Jeopardy", dj_count)
    with col2:
        st.metric("🟡 High Vulnerability Only", high_vuln)
    with col3:
        st.metric("🟠 High Hazard Only", high_hazard)
    with col4:
        st.metric("�� Low Risk", low_risk)

    section_divider()
    section_label("Vulnerability Profile Dashboard")

    col_bar, col_scatter = st.columns([1, 1.5])

    # LEFT: Bar Chart
    with col_bar:
        st.markdown("#### Top Counties by Combined Severity")
        top_counties = stats_with_scores.sort_values('severity_score', ascending=False).head(top_n)
        top_counties_sorted = top_counties.sort_values('severity_score', ascending=True)

        bar_colors = {
            'Low Risk': '#48bb78', 'High Vulnerability': '#ecc94b',
            'High Hazard': '#ed8936', 'Double Jeopardy': '#c53030'
        }

        fig_bar = px.bar(
            top_counties_sorted, x='severity_score', y='County', color='risk_category',
            color_discrete_map=bar_colors, orientation='h',
            hover_data={
                'State': True, 'vulnerability_score': ':.3f', 'hazard_score': ':.3f',
                'severity_score': ':.3f', 'mean_median_aqi': ':.1f', 'mean_max_aqi': ':.1f'
            },
            labels={
                'severity_score': 'Combined Severity Score', 'County': '',
                'risk_category': 'Risk Category', 'vulnerability_score': 'Vulnerability Score',
                'hazard_score': 'Hazard Score'
            },
            category_orders={'risk_category': ['Double Jeopardy', 'High Hazard', 'High Vulnerability', 'Low Risk']}
        )
        fig_bar.update_yaxes(categoryorder='array', categoryarray=top_counties_sorted['County'].tolist())
        fig_bar.update_layout(
            height=max(400, top_n * 35), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=""),
            margin=dict(l=10, r=10, t=40, b=40), xaxis_range=[0, 1]
        )
        fig_bar.update_xaxes(gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0')
        fig_bar.update_yaxes(gridcolor='#e2e8f0')
        st.plotly_chart(fig_bar, use_container_width=True)

    # RIGHT: Vulnerability Profile Scatter
    with col_scatter:
        st.markdown("#### Vulnerability Profile (Interactive)")

        fig_scatter = go.Figure()
        scatter_colors = {
            'Low Risk': '#1a9850', 'High Vulnerability': '#d9ef8b',
            'High Hazard': '#fdae61', 'Double Jeopardy': '#d73027'
        }

        for category in ['Low Risk', 'High Vulnerability', 'High Hazard', 'Double Jeopardy']:
            category_data = stats_with_scores[stats_with_scores['risk_category'] == category]
            if len(category_data) > 0:
                fig_scatter.add_trace(go.Scatter(
                    x=category_data['vulnerability_score'], y=category_data['hazard_score'],
                    mode='markers', name=category,
                    marker=dict(size=10, color=scatter_colors[category], line=dict(width=1, color='white'), opacity=0.8),
                    text=category_data['County'] + ', ' + category_data['State'],
                    hovertemplate=(
                        "<b>%{text}</b><br>Vulnerability Score: %{x:.3f}<br>"
                        "Hazard Score: %{y:.3f}<br>Risk Category: " + category + "<br><extra></extra>"
                    )
                ))

        max_score = max(stats_with_scores['vulnerability_score'].max(), stats_with_scores['hazard_score'].max(), 1.0)

        # Diagonal y=x line
        fig_scatter.add_trace(go.Scatter(
            x=[0, max_score], y=[0, max_score], mode='lines',
            line=dict(dash='dash', color='gray', width=1.5), name='y = x', opacity=0.5, showlegend=False
        ))

        # Mean reference lines
        fig_scatter.add_hline(y=mean_hazard, line_dash="dot", line_color="gray", line_width=1, opacity=0.5,
                              annotation_text=f"Mean Hazard ({mean_hazard:.2f})", annotation_position="top right",
                              annotation_font_size=9, annotation_font_color="gray")
        fig_scatter.add_vline(x=mean_vuln, line_dash="dot", line_color="gray", line_width=1, opacity=0.5,
                              annotation_text=f"Mean Vuln ({mean_vuln:.2f})", annotation_position="top right",
                              annotation_font_size=9, annotation_font_color="gray")

        # Quadrant labels
        fig_scatter.add_annotation(x=max_score*0.75, y=max_score*0.85, text="High Vulnerability<br>High Hazard",
                                   showarrow=False, font=dict(size=10, color='#666'), opacity=0.7, align='center')
        fig_scatter.add_annotation(x=max_score*0.25, y=max_score*0.85, text="Low Vulnerability<br>High Hazard",
                                   showarrow=False, font=dict(size=10, color='#666'), opacity=0.7, align='center')
        fig_scatter.add_annotation(x=max_score*0.25, y=max_score*0.15, text="Low Vulnerability<br>Low Hazard",
                                   showarrow=False, font=dict(size=10, color='#666'), opacity=0.7, align='center')
        fig_scatter.add_annotation(x=max_score*0.75, y=max_score*0.15, text="High Vulnerability<br>Low Hazard",
                                   showarrow=False, font=dict(size=10, color='#666'), opacity=0.7, align='center')

        fig_scatter.update_layout(
            title=dict(text="Vulnerability Profile", font=dict(size=14, color='#1e293b'), x=0.5),
            height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=12),
            legend=dict(title="Risk Category", orientation="v", yanchor="top", y=0.99, xanchor="left", x=1.02,
                        bgcolor='rgba(255,255,255,0.9)', bordercolor='#e2e8f0', borderwidth=1),
            xaxis=dict(title="Vulnerability Score", range=[-0.05, max_score + 0.1], gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0'),
            yaxis=dict(title="Hazard Score", range=[-0.05, max_score + 0.1], gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0'),
            margin=dict(l=60, r=120, t=60, b=60)
        )
        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})

    # Interpretation
    st.markdown(f"""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #dc2626; border-bottom: 1px solid #fef2f2; padding-bottom: 12px;">💡 How to Read This Dashboard</h4>
    <p><strong>Vulnerability Score</strong> (X-axis): Normalized chronic pollution burden (0 = best, 1 = worst based on Mean Median AQI)</p>
    <p><strong>Hazard Score</strong> (Y-axis): Normalized acute pollution events (0 = best, 1 = worst based on Mean Max AQI)</p>
    <p><strong>Key Elements:</strong></p>
    <ul>
        <li><strong>Diagonal line (y=x):</strong> Counties above this line have higher hazard than vulnerability; below means the opposite</li>
        <li><strong>Mean reference lines:</strong> Divide the chart into four quadrants based on average scores</li>
        <li><strong>Upper-right quadrant (Red):</strong> <em>Double Jeopardy</em> counties with both high vulnerability AND high hazard</li>
    </ul>
    <p style="margin-bottom: 0;"><strong>{dj_count} counties</strong> fall into the Double Jeopardy zone. 
    These communities face both chronic daily pollution AND dangerous spikes—a compounding health crisis requiring priority intervention.</p>
    </div>
    """, unsafe_allow_html=True)

    section_divider()
    section_label("Double Jeopardy Counties")

    dj_counties = stats_with_scores[stats_with_scores['risk_category'] == 'Double Jeopardy']
    if len(dj_counties) > 0:
        display_df = dj_counties[['County', 'State', 'vulnerability_score', 'hazard_score',
                                  'severity_score', 'mean_median_aqi', 'mean_max_aqi']].copy()
        display_df.columns = ['County', 'State', 'Vulnerability Score', 'Hazard Score',
                              'Severity Score', 'Mean Median AQI', 'Mean Max AQI']
        display_df = display_df.sort_values('Severity Score', ascending=False).round(3)
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No Double Jeopardy counties found with the current filters. Try selecting 'All States' or adjusting the threshold.")


# =============================================================================
# PAGE 4: SEVERITY SCORE
# =============================================================================
def render_severity_score():
    page_header("Severity Score Analysis", "Combined Pollution Burden Metric", "📈")

    st.markdown("""
    <div class="callout-box-purple">
    <strong>What is the Severity Score?</strong> A single metric that combines both chronic and acute pollution 
    exposure into one comparable number. It normalizes both dimensions to a 0-1 scale and averages them, 
    allowing us to rank counties by overall pollution burden regardless of whether it's driven by daily 
    exposure, extreme events, or both.
    </div>
    """, unsafe_allow_html=True)

    section_divider()
    section_label("How It's Calculated")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #9333ea; border-bottom: 1px solid #faf5ff; padding-bottom: 12px;">Normalization Formula</h4>
        <p>For each metric (Median AQI and Max AQI):</p>
        <pre style="background: #f8fafc; padding: 12px; border-radius: 8px; font-size: 0.85rem; border: 1px solid #e2e8f0;">
Normalized = (Value - Min) / (Max - Min)</pre>
        <p style="margin-bottom: 0;">This scales all values between 0 (best) and 1 (worst).</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #9333ea; border-bottom: 1px solid #faf5ff; padding-bottom: 12px;">Severity Score Formula</h4>
        <pre style="background: #f8fafc; padding: 12px; border-radius: 8px; font-size: 0.85rem; border: 1px solid #e2e8f0;">
Severity = (Norm_Median + Norm_Max) / 2</pre>
        <p style="margin-bottom: 0;">Equal weighting means a county with moderate chronic + moderate acute pollution 
        scores similarly to one with high chronic + low acute (or vice versa).</p>
        </div>
        """, unsafe_allow_html=True)

    section_divider()
    section_label("Filters")

    col1, col2 = st.columns(2)
    with col1:
        states = ['All States'] + sorted(county_stats['State'].unique().tolist())
        selected_state = st.selectbox("Select State", states, key="severity_state")
    with col2:
        top_n = st.slider("Show Top N Counties", min_value=10, max_value=50, value=15, step=5, key="severity_topn")

    if selected_state != 'All States':
        filtered_stats = county_stats[county_stats['State'] == selected_state].copy()
    else:
        filtered_stats = county_stats.copy()

    stats_with_severity = filtered_stats.copy()
    median_range = stats_with_severity['mean_median_aqi'].max() - stats_with_severity['mean_median_aqi'].min()
    max_range = stats_with_severity['mean_max_aqi'].max() - stats_with_severity['mean_max_aqi'].min()

    if median_range != 0:
        stats_with_severity['norm_median'] = (stats_with_severity['mean_median_aqi'] - stats_with_severity['mean_median_aqi'].min()) / median_range
    else:
        stats_with_severity['norm_median'] = 0.5
    if max_range != 0:
        stats_with_severity['norm_max'] = (stats_with_severity['mean_max_aqi'] - stats_with_severity['mean_max_aqi'].min()) / max_range
    else:
        stats_with_severity['norm_max'] = 0.5
    stats_with_severity['severity_score'] = (stats_with_severity['norm_median'] + stats_with_severity['norm_max']) / 2

    severity_top = stats_with_severity.sort_values('severity_score', ascending=False).head(top_n)

    section_divider()
    section_label(f"Top {top_n} Counties by Severity Score")

    fig = px.bar(
        severity_top.sort_values('severity_score', ascending=False),
        x='severity_score', y='County', color='State', orientation='h',
        hover_data={
            'State': True, 'mean_median_aqi': ':.1f', 'mean_max_aqi': ':.1f',
            'norm_median': ':.3f', 'norm_max': ':.3f', 'severity_score': ':.3f'
        },
        labels={
            'severity_score': 'Severity Score (0-1)', 'County': '', 'State': 'State',
            'norm_median': 'Normalized Chronic', 'norm_max': 'Normalized Acute'
        },
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    fig.update_layout(
        height=max(400, top_n * 28), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=""),
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis_title="Severity Score (0 = Best, 1 = Worst)", yaxis_title="", xaxis_range=[0, 1]
    )
    fig.update_xaxes(gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0')
    fig.update_yaxes(gridcolor='#e2e8f0')
    st.plotly_chart(fig, use_container_width=True)

    if len(severity_top) > 0:
        worst_county = severity_top.iloc[0]
        st.markdown(f"""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #9333ea; border-bottom: 1px solid #faf5ff; padding-bottom: 12px;">💡 What This Means</h4>
        <p><strong>{worst_county['County']}, {worst_county['State']}</strong> has the highest Severity Score 
        of <strong>{worst_county['severity_score']:.3f}</strong> (on a 0-1 scale).</p>
        <p><strong>Component breakdown:</strong></p>
        <ul>
            <li>Normalized Chronic Score: {worst_county['norm_median']:.3f} (Mean Median AQI: {worst_county['mean_median_aqi']:.1f})</li>
            <li>Normalized Acute Score: {worst_county['norm_max']:.3f} (Mean Max AQI: {worst_county['mean_max_aqi']:.1f})</li>
        </ul>
        <p style="margin-bottom: 0;">A score close to 1.0 indicates a county near the worst on both dimensions. This metric helps 
        prioritize intervention by identifying counties with the highest <em>overall</em> pollution burden.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📋 View Full Data Table"):
        display_df = severity_top[['County', 'State', 'mean_median_aqi', 'mean_max_aqi',
                                   'norm_median', 'norm_max', 'severity_score']].copy()
        display_df.columns = ['County', 'State', 'Mean Median AQI', 'Mean Max AQI',
                              'Norm. Chronic', 'Norm. Acute', 'Severity Score']
        display_df = display_df.round(3)
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(display_df, use_container_width=True)


# =============================================================================
# PAGE 5: COUNTY DRILLDOWN
# =============================================================================
def render_county_drilldown():
    page_header("County Drilldown", "Explore Individual County Profiles", "🔍")

    st.markdown("""
    <div class="callout-box-teal">
    <strong>Deep Dive:</strong> Select a specific county to view its air quality trends over 2021-2024, 
    understand how it compares to thresholds, and download its data for further analysis.
    </div>
    """, unsafe_allow_html=True)

    section_divider()
    section_label("Select County")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        states = sorted(df['State'].unique().tolist())
        selected_state = st.selectbox("Select State", states, key="drilldown_state")
    with col2:
        counties_in_state = sorted(df[df['State'] == selected_state]['County'].unique().tolist())
        selected_county = st.selectbox("Select County", counties_in_state, key="drilldown_county")
    with col3:
        percentile = st.slider("Threshold Percentile", min_value=80, max_value=99, value=90, step=1,
                               help="Used to determine Double Jeopardy status")

    county_data = df[(df['State'] == selected_state) & (df['County'] == selected_county)].copy()
    county_yearly = county_data.groupby('Year').agg({
        'Median AQI': 'mean', 'Max AQI': 'mean', 'Days with AQI': 'sum',
        'Good Days': 'sum', 'Unhealthy Days': 'sum'
    }).reset_index()

    county_agg = county_stats[(county_stats['State'] == selected_state) &
                              (county_stats['County'] == selected_county)].iloc[0]

    median_threshold = county_stats['mean_median_aqi'].quantile(percentile / 100)
    max_threshold = county_stats['mean_max_aqi'].quantile(percentile / 100)
    is_high_chronic = county_agg['mean_median_aqi'] >= median_threshold
    is_high_acute = county_agg['mean_max_aqi'] >= max_threshold
    is_double_jeopardy = is_high_chronic and is_high_acute

    section_divider()
    section_label(f"Profile: {selected_county}, {selected_state}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("4-Year Mean Median AQI", f"{county_agg['mean_median_aqi']:.1f}",
                  delta=f"{'Above' if is_high_chronic else 'Below'} {percentile}th %ile",
                  delta_color="inverse" if is_high_chronic else "normal")
    with col2:
        st.metric("4-Year Mean Max AQI", f"{county_agg['mean_max_aqi']:.1f}",
                  delta=f"{'Above' if is_high_acute else 'Below'} {percentile}th %ile",
                  delta_color="inverse" if is_high_acute else "normal")
    with col3:
        chronic_rank = (county_stats['mean_median_aqi'] >= county_agg['mean_median_aqi']).sum()
        st.metric("Chronic Rank", f"#{chronic_rank}", delta=f"of {len(county_stats)} counties")
    with col4:
        acute_rank = (county_stats['mean_max_aqi'] >= county_agg['mean_max_aqi']).sum()
        st.metric("Acute Rank", f"#{acute_rank}", delta=f"of {len(county_stats)} counties")

    if is_double_jeopardy:
        st.markdown(f"""
        <div class="warning-box">
        <h4 style="margin-top: 0; color: #c53030;">⚠️ DOUBLE JEOPARDY STATUS: YES</h4>
        <p>At the {percentile}th percentile threshold, <strong>{selected_county}</strong> qualifies as a 
        Double Jeopardy county. It exceeds both the chronic threshold ({median_threshold:.1f}) and 
        acute threshold ({max_threshold:.1f}).</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        status_text = []
        if is_high_chronic:
            status_text.append("High Chronic (above chronic threshold)")
        if is_high_acute:
            status_text.append("High Acute (above acute threshold)")
        if not status_text:
            status_text.append("Low Risk (below both thresholds)")
        st.markdown(f"""
        <div class="success-box">
        <h4 style="margin-top: 0; color: #38a169;">✓ DOUBLE JEOPARDY STATUS: NO</h4>
        <p>At the {percentile}th percentile threshold, <strong>{selected_county}</strong> does not qualify 
        as Double Jeopardy. Status: {', '.join(status_text)}.</p>
        </div>
        """, unsafe_allow_html=True)

    # Yearly Trend Chart
    st.markdown("### 📈 Yearly Trends (2021-2024)")

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Median AQI (Daily Exposure)", "Max AQI (Peak Events)"))

    fig.add_trace(go.Scatter(
        x=county_yearly['Year'], y=county_yearly['Median AQI'], mode='lines+markers',
        name='Median AQI', line=dict(color='#3182ce', width=3), marker=dict(size=10)
    ), row=1, col=1)

    fig.add_hline(y=median_threshold, line_dash="dash", line_color="#dd6b20",
                  annotation_text=f"{percentile}th %ile Threshold", row=1, col=1)

    fig.add_trace(go.Scatter(
        x=county_yearly['Year'], y=county_yearly['Max AQI'], mode='lines+markers',
        name='Max AQI', line=dict(color='#c53030', width=3), marker=dict(size=10)
    ), row=1, col=2)

    fig.add_hline(y=max_threshold, line_dash="dash", line_color="#dd6b20",
                  annotation_text=f"{percentile}th %ile Threshold", row=1, col=2)

    fig.update_layout(
        height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=12), showlegend=False,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    fig.update_xaxes(gridcolor='#e2e8f0', dtick=1)
    fig.update_yaxes(gridcolor='#e2e8f0')
    st.plotly_chart(fig, use_container_width=True)

    # Trend interpretation
    if len(county_yearly) > 1:
        median_trend = county_yearly['Median AQI'].iloc[-1] - county_yearly['Median AQI'].iloc[0]
        max_trend = county_yearly['Max AQI'].iloc[-1] - county_yearly['Max AQI'].iloc[0]
        median_direction = "improving" if median_trend < 0 else "worsening"
        max_direction = "improving" if max_trend < 0 else "worsening"
        st.markdown(f"""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #0f766e; border-bottom: 1px solid #f0fdfa; padding-bottom: 12px;">📊 Trend Analysis</h4>
        <ul>
            <li><strong>Chronic (Median AQI):</strong> {median_direction} by {abs(median_trend):.1f} points 
            from {county_yearly['Year'].min()} to {county_yearly['Year'].max()}</li>
            <li><strong>Acute (Max AQI):</strong> {max_direction} by {abs(max_trend):.1f} points 
            from {county_yearly['Year'].min()} to {county_yearly['Year'].max()}</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    section_divider()
    section_label("Raw Data")

    display_df = county_yearly.copy()
    display_df.columns = ['Year', 'Median AQI', 'Max AQI', 'Days with AQI', 'Good Days', 'Unhealthy Days']
    display_df = display_df.round(1)
    st.dataframe(display_df, use_container_width=True)

    csv = county_data.to_csv(index=False)
    st.download_button(
        label="📥 Download County Data (CSV)", data=csv,
        file_name=f"{selected_county}_{selected_state}_aqi_data.csv", mime="text/csv"
    )


# =============================================================================
# PAGE 6: DOWNLOAD DATA & METHODOLOGY
# =============================================================================
def render_download_data():
    page_header("Download Data & Methodology", "Export Processed Data and Learn About Our Approach", "📥")

    section_divider()
    section_label("Data Downloads")

    # Compute export data
    full_stats = county_stats.copy()
    median_threshold = full_stats['mean_median_aqi'].quantile(0.90)
    max_threshold = full_stats['mean_max_aqi'].quantile(0.90)

    full_stats['Risk_Category'] = 'Low Risk'
    full_stats.loc[(full_stats['mean_median_aqi'] >= median_threshold), 'Risk_Category'] = 'High Chronic'
    full_stats.loc[(full_stats['mean_max_aqi'] >= max_threshold), 'Risk_Category'] = 'High Acute'
    full_stats.loc[(full_stats['mean_median_aqi'] >= median_threshold) &
                   (full_stats['mean_max_aqi'] >= max_threshold), 'Risk_Category'] = 'Double Jeopardy'

    median_range = full_stats['mean_median_aqi'].max() - full_stats['mean_median_aqi'].min()
    max_range = full_stats['mean_max_aqi'].max() - full_stats['mean_max_aqi'].min()
    if median_range != 0:
        full_stats['norm_median'] = (full_stats['mean_median_aqi'] - full_stats['mean_median_aqi'].min()) / median_range
    else:
        full_stats['norm_median'] = 0.5
    if max_range != 0:
        full_stats['norm_max'] = (full_stats['mean_max_aqi'] - full_stats['mean_max_aqi'].min()) / max_range
    else:
        full_stats['norm_max'] = 0.5
    full_stats['severity_score'] = (full_stats['norm_median'] + full_stats['norm_max']) / 2
    full_stats['Chronic_Rank'] = full_stats['mean_median_aqi'].rank(ascending=False).astype(int)
    full_stats['Acute_Rank'] = full_stats['mean_max_aqi'].rank(ascending=False).astype(int)
    full_stats['Severity_Rank'] = full_stats['severity_score'].rank(ascending=False).astype(int)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #dc2626; border-bottom: 1px solid #fef2f2; padding-bottom: 12px;">🔴 Double Jeopardy Counties</h4>
        <p style="margin-bottom: 0;">Counties exceeding the 90th percentile for BOTH Mean Median AQI and Mean Max AQI (2021-2024).</p>
        </div>
        """, unsafe_allow_html=True)

        dj_counties = full_stats[full_stats['Risk_Category'] == 'Double Jeopardy'].copy()
        dj_export = dj_counties[['County', 'State', 'mean_median_aqi', 'mean_max_aqi',
                                 'Chronic_Rank', 'Acute_Rank', 'severity_score', 'Severity_Rank']]
        dj_export.columns = ['County', 'State', 'Mean_Median_AQI', 'Mean_Max_AQI',
                             'Chronic_Rank', 'Acute_Rank', 'Severity_Score', 'Severity_Rank']
        dj_export = dj_export.sort_values('Severity_Score', ascending=False).round(3)

        st.download_button(
            label=f"📥 Download Double Jeopardy List ({len(dj_counties)} counties)",
            data=dj_export.to_csv(index=False),
            file_name="double_jeopardy_counties.csv", mime="text/csv"
        )

    with col2:
        st.markdown("""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #9333ea; border-bottom: 1px solid #faf5ff; padding-bottom: 12px;">📈 Top Severity Counties</h4>
        <p style="margin-bottom: 0;">Top 50 counties ranked by combined Severity Score (normalized chronic + acute exposure).</p>
        </div>
        """, unsafe_allow_html=True)

        top_severity = full_stats.nlargest(50, 'severity_score').copy()
        severity_export = top_severity[['County', 'State', 'mean_median_aqi', 'mean_max_aqi',
                                        'norm_median', 'norm_max', 'severity_score',
                                        'Risk_Category', 'Severity_Rank']]
        severity_export.columns = ['County', 'State', 'Mean_Median_AQI', 'Mean_Max_AQI',
                                   'Norm_Chronic', 'Norm_Acute', 'Severity_Score',
                                   'Risk_Category', 'Severity_Rank']
        severity_export = severity_export.round(3)

        st.download_button(
            label="📥 Download Top 50 Severity List",
            data=severity_export.to_csv(index=False),
            file_name="top_severity_counties.csv", mime="text/csv"
        )

    # Full dataset
    section_label("Full Processed Dataset")

    st.markdown("""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #2563eb; border-bottom: 1px solid #eff6ff; padding-bottom: 12px;">Complete County Statistics</h4>
    <p style="margin-bottom: 0;">All counties with aggregated statistics, risk categories, and severity scores.</p>
    </div>
    """, unsafe_allow_html=True)

    full_export = full_stats[['County', 'State', 'mean_median_aqi', 'mean_max_aqi',
                              'norm_median', 'norm_max', 'severity_score',
                              'Risk_Category', 'Chronic_Rank', 'Acute_Rank', 'Severity_Rank']]
    full_export.columns = ['County', 'State', 'Mean_Median_AQI', 'Mean_Max_AQI',
                           'Norm_Chronic', 'Norm_Acute', 'Severity_Score',
                           'Risk_Category', 'Chronic_Rank', 'Acute_Rank', 'Severity_Rank']
    full_export = full_export.sort_values('Severity_Score', ascending=False).round(3)

    st.download_button(
        label=f"📥 Download Full Dataset ({len(full_export)} counties)",
        data=full_export.to_csv(index=False),
        file_name="all_county_statistics.csv", mime="text/csv"
    )

    # Methodology
    st.markdown("---")
    st.markdown("## 📐 Methodology")

    st.markdown("""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #2d3748;">Data Processing Pipeline</h4>
    <ul>
        <li><strong>Data Source:</strong> EPA Air Quality Index Annual Summary files (2021-2024)</li>
        <li><strong>Geographic Unit:</strong> U.S. Counties</li>
        <li><strong>Aggregation:</strong> 4-year average of annual Median AQI and Max AQI per county</li>
        <li><strong>Threshold Calculation:</strong> 90th percentile computed dynamically from filtered dataset</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #2563eb; border-bottom: 1px solid #eff6ff; padding-bottom: 12px;">Key Metrics Defined</h4>
        <ul>
            <li><strong>Mean Median AQI:</strong> Average of yearly Median AQI values (2021-2024). 
            Represents typical daily air quality—the "daily grind" of chronic exposure.</li>
            <br>
            <li><strong>Mean Max AQI:</strong> Average of yearly Max AQI values (2021-2024). 
            Represents peak pollution events—acute exposure episodes like wildfires or inversions.</li>
            <br>
            <li><strong>Severity Score:</strong> (Normalized Median + Normalized Max) / 2. 
            A single 0-1 metric combining both dimensions for overall ranking.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
        <h4 style="margin-top: 0; color: #dc2626; border-bottom: 1px solid #fef2f2; padding-bottom: 12px;">Risk Categories</h4>
        <ul>
            <li><strong style="color: #22c55e;">Low Risk:</strong> Below 90th percentile on both metrics</li>
            <br>
            <li><strong style="color: #eab308;">High Chronic:</strong> Above 90th percentile for Median AQI only</li>
            <br>
            <li><strong style="color: #f97316;">High Acute:</strong> Above 90th percentile for Max AQI only</li>
            <br>
            <li><strong style="color: #dc2626;">Double Jeopardy:</strong> Above 90th percentile for BOTH metrics</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    section_divider()
    section_label("Important Limitations")

    st.markdown("""
    <div class="callout-box-orange">
    <p style="margin-top: 0;"><strong>This analysis has several limitations that users should consider:</strong></p>
    <ul>
        <li><strong>Monitoring Coverage:</strong> Not all counties have continuous air quality monitoring. 
        Counties with fewer monitoring stations may have less reliable data, and some rural areas are underrepresented.</li>
        <br>
        <li><strong>Outlier Events:</strong> Extreme Max AQI values (often exceeding 500) from wildfire smoke 
        can disproportionately affect averages. We provide outlier handling options, but true values 
        reflect real exposures.</li>
        <br>
        <li><strong>Temporal Aggregation:</strong> 4-year averages smooth out year-to-year variation. 
        A county that dramatically improved in 2024 may still appear high-risk due to earlier years.</li>
        <br>
        <li><strong>Population Weighting:</strong> This analysis treats all counties equally. 
        A county with 10,000 residents counts the same as one with 10 million. 
        Population-weighted analyses may yield different priorities.</li>
        <br>
        <li><strong>Single Pollutant Focus:</strong> AQI is a composite index. Counties may face different 
        primary pollutants (PM2.5 vs. ozone) requiring different interventions.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p style="margin: 0 0 8px 0;"><strong>Data Source:</strong> EPA Air Quality Index Annual Summary (2021-2024)</p>
        <p style="margin: 0; color: #94a3b8;"><strong>Dashboard:</strong> Datathon 2026 &nbsp;|&nbsp; Built with Streamlit + Plotly &nbsp;|&nbsp; <strong>Last Updated:</strong> February 2026</p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# ROUTE TO SELECTED PAGE
# =============================================================================
if selected == "Overview":
    render_overview()
elif selected == "Chronic Pollution":
    render_chronic_pollution()
elif selected == "Extreme Spikes":
    render_extreme_spikes()
elif selected == "Double Jeopardy":
    render_double_jeopardy()
elif selected == "Severity Score":
    render_severity_score()
elif selected == "County Drilldown":
    render_county_drilldown()
elif selected == "Download Data":
    render_download_data()
