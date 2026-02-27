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

/* ── Headings ── */
h1 { color: #FFFFFF !important; font-weight: 700; letter-spacing: -0.5px; }
h2 { color: #FFFFFF !important; font-weight: 600; }
h3 { color: #C9D1D9 !important; font-weight: 600; }

/* ── Divider ── */
hr { border-color: #1E2A3B !important; }

/* ── st.metric cards ── */
[data-testid="metric-container"] {
    background: #141A28;
    border: 1px solid #1E2A3B;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
[data-testid="metric-container"] label {
    color: #9CA3AF !important;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.88rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0099BB, #00D4FF);
    color: #0B0F1A !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    letter-spacing: 0.03em;
    transition: opacity 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,212,255,0.25);
}
.stButton > button:hover {
    opacity: 0.88;
    box-shadow: 0 4px 16px rgba(0,212,255,0.45);
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
    font-size: 1rem;
    font-weight: 700;
    color: #00D4FF;
    border-left: 4px solid #00D4FF;
    padding-left: 12px;
    margin: 22px 0 12px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.nc-kpi-card {
    background: #141A28;
    border: 1px solid #1E2A3B;
    border-radius: 14px;
    padding: 22px 26px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.45);
    transition: border-color 0.2s;
}
.nc-kpi-card:hover { border-color: #00D4FF; }
.nc-kpi-title {
    font-size: 0.76rem;
    color: #9CA3AF;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.nc-kpi-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.15;
}
.nc-kpi-delta-pos { color: #00F5A0; font-size: 0.88rem; margin-top: 4px; }
.nc-kpi-delta-neg { color: #FF4B4B; font-size: 0.88rem; margin-top: 4px; }
.nc-kpi-delta-neu { color: #9CA3AF; font-size: 0.88rem; margin-top: 4px; }

.nc-result-card {
    background: #141A28;
    border: 1px solid #1E2A3B;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
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
