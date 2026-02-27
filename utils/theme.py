"""
utils/theme.py
Shared dark-enterprise theme for NeuroCore AI.

Provides:
- inject_css()          → call once per page to apply global styles
- plotly_layout()       → returns a dict of Plotly layout overrides
- Color constants       → COLORS dict
"""

import streamlit as st

# ── Color palette ──────────────────────────────────────────────────────────────
COLORS = {
    "bg":         "#0B0F1A",
    "card_bg":    "#141A28",
    "border":     "#1E2A3B",
    "text":       "#FFFFFF",
    "text_sec":   "#C9D1D9",
    "text_muted": "#9CA3AF",
    "accent":     "#00D4FF",
    "success":    "#00F5A0",
    "warning":    "#FFC107",
    "danger":     "#FF4B4B",
    "sidebar_bg": "#0D1321",
}

_CSS = """
<style>
/* ── Google Fonts – Inter ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global reset ── */
html, body, [class*="css"]  { font-family: 'Inter', 'Segoe UI', sans-serif; }
.stApp                       { background-color: #0B0F1A; color: #C9D1D9; }

/* ── Ensure main content text is always readable ── */
.main .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px; }
.stMarkdown, .stMarkdown p { color: #C9D1D9 !important; }
p, li { color: #C9D1D9; font-size: 0.95rem; line-height: 1.65; }
label, span { color: #C9D1D9; font-size: 0.95rem; line-height: 1.6; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0D1321;
    border-right: 1px solid #1E2A3B;
}
section[data-testid="stSidebar"] * { color: #C9D1D9 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
section[data-testid="stSidebar"] .stCaption { color: #9CA3AF !important; }
section[data-testid="stSidebar"] a:hover { color: #00D4FF !important; }

/* ── Typography scale ── */
h1 {
    color: #FFFFFF !important;
    font-size: 2.25rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.8px;
    line-height: 1.2;
    margin-bottom: 0.25rem;
}
h2 {
    color: #FFFFFF !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
    margin-top: 2rem;
    margin-bottom: 0.5rem;
}
h3 {
    color: #C9D1D9 !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0;
}

/* ── Divider ── */
hr { border-color: #1E2A3B !important; margin: 1.75rem 0 !important; }

/* ── st.metric cards ── */
[data-testid="metric-container"] {
    background: #141A28;
    border: 1px solid #1E2A3B;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
[data-testid="metric-container"]:hover {
    border-color: rgba(0,212,255,0.5);
    box-shadow: 0 0 18px rgba(0,212,255,0.12), 0 4px 16px rgba(0,0,0,0.4);
}
[data-testid="metric-container"] label {
    color: #C9D1D9 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] svg { display: inline-block; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0099BB, #00D4FF);
    color: #0B0F1A !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.04em;
    padding: 0.55rem 1.4rem;
    transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
    box-shadow: 0 2px 8px rgba(0,212,255,0.25);
    cursor: pointer;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,212,255,0.5);
    background: linear-gradient(135deg, #00AACF, #33DDFF);
}
.stButton > button:active {
    transform: translateY(0px);
    box-shadow: 0 2px 8px rgba(0,212,255,0.3);
}

/* ── Dataframe / table ── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #1E2A3B;
}

/* Streamlit dataframe – column headers */
[data-testid="stDataFrame"] th,
.dvn-scroller .col-header-cell,
[data-testid="stDataFrame"] [role="columnheader"] {
    background-color: #1B2438 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border-bottom: 2px solid #00D4FF !important;
}

/* Dataframe cell text */
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] [role="gridcell"] {
    background-color: #141A28 !important;
    color: #C9D1D9 !important;
    font-size: 0.88rem !important;
    border-bottom: 1px solid #1E2A3B !important;
}

/* Alternating rows for readability */
[data-testid="stDataFrame"] tr:nth-child(even) td,
[data-testid="stDataFrame"] [role="row"]:nth-child(even) [role="gridcell"] {
    background-color: #0F1520 !important;
}

/* Markdown tables */
.stMarkdown table {
    width: 100%;
    border-collapse: collapse;
    border-radius: 10px;
    overflow: hidden;
    background: #141A28;
    border: 1px solid #1E2A3B;
    margin: 1rem 0;
}
.stMarkdown table th {
    background-color: #1B2438 !important;
    color: #FFFFFF !important;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 12px 16px;
    border-bottom: 2px solid #00D4FF;
    text-align: left;
}
.stMarkdown table td {
    color: #C9D1D9 !important;
    font-size: 0.9rem;
    padding: 10px 16px;
    border-bottom: 1px solid #1E2A3B;
}
.stMarkdown table tr:nth-child(even) td {
    background-color: #0F1520;
}
.stMarkdown table tr:hover td {
    background-color: #192135;
}

/* ── Info / warning / error callouts ── */
[data-testid="stAlert"] { border-radius: 10px; }
[data-testid="stAlert"] p { color: inherit !important; }

/* ── Slider ── */
[data-testid="stSlider"] label { color: #C9D1D9 !important; font-weight: 500; }
[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p { color: #9CA3AF !important; }

/* ── Number input / text input ── */
[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label { color: #C9D1D9 !important; font-weight: 500; }

/* ── Caption ── */
.stCaption, [data-testid="stCaption"] { color: #9CA3AF !important; }

/* ── Spinner text ── */
[data-testid="stSpinner"] p { color: #C9D1D9 !important; }

/* ── Custom components ── */
.nc-section-header {
    font-size: 0.82rem;
    font-weight: 700;
    color: #00D4FF;
    border-left: 4px solid #00D4FF;
    padding: 4px 0 4px 12px;
    margin: 36px 0 18px;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    background: linear-gradient(90deg, rgba(0,212,255,0.07) 0%, transparent 100%);
    border-radius: 0 6px 6px 0;
}
.nc-kpi-card {
    background: #141A28;
    border: 1px solid #1E2A3B;
    border-radius: 14px;
    padding: 28px 28px 24px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.45);
    transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
    min-height: 130px;
}
.nc-kpi-card:hover {
    border-color: rgba(0,212,255,0.6);
    box-shadow: 0 0 22px rgba(0,212,255,0.15), 0 6px 24px rgba(0,0,0,0.5);
    transform: translateY(-2px);
}
.nc-kpi-title {
    font-size: 0.75rem;
    font-weight: 700;
    color: #C9D1D9;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.nc-kpi-value {
    font-size: 2.25rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.1;
    letter-spacing: -0.5px;
    margin-bottom: 10px;
    text-shadow: 0 0 20px rgba(255,255,255,0.1);
}
.nc-kpi-delta-pos {
    color: #00F5A0;
    font-size: 0.83rem;
    font-weight: 700;
    margin-top: 2px;
    letter-spacing: 0.02em;
}
.nc-kpi-delta-neg {
    color: #FF4B4B;
    font-size: 0.83rem;
    font-weight: 700;
    margin-top: 2px;
    letter-spacing: 0.02em;
}
.nc-kpi-delta-neu {
    color: #C9D1D9;
    font-size: 0.83rem;
    font-weight: 500;
    margin-top: 2px;
    letter-spacing: 0.02em;
}

.nc-result-card {
    background: #141A28;
    border: 1px solid #1E2A3B;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.35);
}
</style>
"""


def inject_css() -> None:
    """Inject the global NeuroCore AI dark-enterprise CSS into the current page."""
    st.markdown(_CSS, unsafe_allow_html=True)


def plotly_layout(**overrides) -> dict:
    """
    Return a Plotly layout dict configured for the dark enterprise theme.

    Keyword arguments are merged on top of the defaults, allowing per-chart
    customisation without repeating boilerplate.
    """
    defaults = dict(
        template="plotly_dark",
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor="#111827",
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color=COLORS["text_sec"],
            size=12,
        ),
        title_font=dict(color=COLORS["text"], size=15, family="Inter, Segoe UI, sans-serif"),
        title_x=0.0,
        legend=dict(
            bgcolor="rgba(20,26,40,0.9)",
            bordercolor=COLORS["border"],
            borderwidth=1,
            font=dict(color=COLORS["text_sec"], size=12),
        ),
        xaxis=dict(
            gridcolor="#1E2A3B",
            linecolor="#2A3A50",
            tickfont=dict(color=COLORS["text_sec"], size=11),
            title_font=dict(color=COLORS["text_sec"], size=12),
            zerolinecolor="#1E2A3B",
        ),
        yaxis=dict(
            gridcolor="#1E2A3B",
            linecolor="#2A3A50",
            tickfont=dict(color=COLORS["text_sec"], size=11),
            title_font=dict(color=COLORS["text_sec"], size=12),
            zerolinecolor="#1E2A3B",
        ),
        margin=dict(l=52, r=32, t=52, b=52),
        hoverlabel=dict(
            bgcolor=COLORS["card_bg"],
            bordercolor=COLORS["border"],
            font=dict(color=COLORS["text"], size=12),
        ),
    )
    # Deep-merge top-level keys; caller overrides win
    defaults.update(overrides)
    return defaults


def section_header(label: str) -> None:
    """Render a styled section header."""
    st.markdown(
        f'<div class="nc-section-header">{label}</div>',
        unsafe_allow_html=True,
    )
