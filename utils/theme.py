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
p, li, span, label { font-size: 0.95rem; line-height: 1.6; }

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
    color: #9CA3AF !important;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 1.85rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

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
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
.stDataFrame thead th {
    background-color: #141A28 !important;
    color: #C9D1D9 !important;
}

/* ── Info / warning / error callouts ── */
[data-testid="stAlert"] { border-radius: 10px; }

/* ── Custom components ── */
.nc-section-header {
    font-size: 0.85rem;
    font-weight: 700;
    color: #00D4FF;
    border-left: 4px solid #00D4FF;
    padding-left: 12px;
    margin: 32px 0 16px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.nc-kpi-card {
    background: #141A28;
    border: 1px solid #1E2A3B;
    border-radius: 14px;
    padding: 26px 28px 22px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.45);
    transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
}
.nc-kpi-card:hover {
    border-color: rgba(0,212,255,0.6);
    box-shadow: 0 0 22px rgba(0,212,255,0.15), 0 6px 24px rgba(0,0,0,0.5);
    transform: translateY(-2px);
}
.nc-kpi-title {
    font-size: 0.78rem;
    font-weight: 600;
    color: #9CA3AF;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.nc-kpi-value {
    font-size: 2.15rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.15;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}
.nc-kpi-delta-pos {
    color: #00F5A0;
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 2px;
    letter-spacing: 0.02em;
}
.nc-kpi-delta-neg {
    color: #FF4B4B;
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 2px;
    letter-spacing: 0.02em;
}
.nc-kpi-delta-neu {
    color: #9CA3AF;
    font-size: 0.82rem;
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
        plot_bgcolor=COLORS["card_bg"],
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color=COLORS["text_sec"],
            size=12,
        ),
        title_font=dict(color=COLORS["text"], size=15, family="Inter, Segoe UI, sans-serif"),
        legend=dict(
            bgcolor="rgba(20,26,40,0.85)",
            bordercolor=COLORS["border"],
            borderwidth=1,
            font=dict(color=COLORS["text_sec"], size=11),
        ),
        xaxis=dict(
            gridcolor=COLORS["border"],
            linecolor=COLORS["border"],
            tickfont=dict(color=COLORS["text_muted"]),
            title_font=dict(color=COLORS["text_sec"]),
            zerolinecolor=COLORS["border"],
        ),
        yaxis=dict(
            gridcolor=COLORS["border"],
            linecolor=COLORS["border"],
            tickfont=dict(color=COLORS["text_muted"]),
            title_font=dict(color=COLORS["text_sec"]),
            zerolinecolor=COLORS["border"],
        ),
        margin=dict(l=48, r=28, t=52, b=48),
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
