import streamlit as st
import requests
from datetime import datetime

#how to run: streamlit run frontend/frontend_app.py

st.set_page_config(
    page_title = "CodeSense — AI Code Review",
    page_icon  = "◈",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# ══════════════════════════════════════════════════════
# CSS — Refined Dark Editorial Theme
# Fonts: Instrument Serif (display) + DM Mono (code)
# ══════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

:root {
    --bg-base:       #060910;
    --bg-surface:    #0C1018;
    --bg-elevated:   #111827;
    --bg-border:     #1C2333;
    --bg-hover:      #161E2E;

    --text-primary:  #F0F4F8;
    --text-secondary:#8B9AB0;
    --text-muted:    #4A5568;
    --text-code:     #A8B4C8;

    --accent-blue:   #4A9EFF;
    --accent-teal:   #2DD4BF;
    --accent-amber:  #F59E0B;
    --accent-rose:   #F87171;
    --accent-violet: #A78BFA;
    --accent-green:  #34D399;

    --font-display:  'Instrument Serif', Georgia, serif;
    --font-sans:     'DM Sans', system-ui, sans-serif;
    --font-mono:     'DM Mono', 'Fira Code', monospace;

    --radius-sm:  6px;
    --radius-md:  10px;
    --radius-lg:  16px;
    --radius-xl:  20px;

    --shadow-sm:  0 1px 3px rgba(0,0,0,0.4);
    --shadow-md:  0 4px 16px rgba(0,0,0,0.5);
    --shadow-lg:  0 12px 40px rgba(0,0,0,0.6);
}

/* ── Reset & Base ─────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main .block-container {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-sans) !important;
}

.main .block-container {
    padding-top: 0 !important;
    max-width: 100% !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--bg-border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Scrollbar ────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--bg-border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ── Top Navigation Bar ───────────────────────────── */
.topbar {
    background: var(--bg-surface);
    border-bottom: 1px solid var(--bg-border);
    padding: 0 40px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
}
.topbar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}
.topbar-symbol {
    font-size: 22px;
    color: var(--accent-blue);
    font-weight: 300;
    line-height: 1;
}
.topbar-name {
    font-family: var(--font-display);
    font-size: 20px;
    color: var(--text-primary);
    letter-spacing: -0.3px;
    font-style: italic;
}
.topbar-version {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    background: var(--bg-elevated);
    padding: 3px 8px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--bg-border);
    margin-left: 10px;
}
.topbar-status {
    display: flex;
    align-items: center;
    gap: 7px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
}
.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--accent-green);
    box-shadow: 0 0 6px var(--accent-green);
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Page Content ─────────────────────────────────── */
.page-content {
    padding: 36px 48px 48px 48px;
    animation: fade-up 0.5s ease forwards;
}
@keyframes fade-up {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Page Header ──────────────────────────────────── */
.page-header {
    margin-bottom: 36px;
}
.page-eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--accent-blue);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.page-title {
    font-family: var(--font-display);
    font-size: 44px;
    font-weight: 400;
    font-style: italic;
    color: var(--text-primary);
    line-height: 1.05;
    letter-spacing: -1px;
}
.page-title em {
    color: var(--accent-blue);
    font-style: italic;
}
.page-desc {
    font-family: var(--font-sans);
    font-size: 15px;
    color: var(--text-secondary);
    margin-top: 12px;
    font-weight: 300;
    line-height: 1.6;
    max-width: 560px;
}

/* ── PR Context Strip ─────────────────────────────── */
.context-strip {
    background: var(--bg-elevated);
    border: 1px solid var(--bg-border);
    border-radius: var(--radius-lg);
    padding: 18px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.context-strip::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--accent-blue), var(--accent-violet));
    border-radius: 3px 0 0 3px;
}
.context-repo {
    font-family: var(--font-mono);
    font-size: 14px;
    font-weight: 500;
    color: var(--accent-blue);
    letter-spacing: -0.3px;
}
.context-pr {
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 3px;
}
.context-pill {
    font-family: var(--font-mono);
    font-size: 10px;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-weight: 500;
}
.pill-open   { background: rgba(52,211,153,0.1); color: var(--accent-green);  border: 1px solid rgba(52,211,153,0.2); }
.pill-github { background: rgba(74,158,255,0.1); color: var(--accent-blue);   border: 1px solid rgba(74,158,255,0.2);
               text-decoration: none; display: inline-block; }
.pill-date   { background: var(--bg-surface);    color: var(--text-muted);    border: 1px solid var(--bg-border); }

/* ── Summary Card ─────────────────────────────────── */
.summary-card {
    background: var(--bg-elevated);
    border: 1px solid var(--bg-border);
    border-radius: var(--radius-lg);
    padding: 24px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.summary-card::after {
    content: '"';
    font-family: var(--font-display);
    font-size: 120px;
    color: rgba(74,158,255,0.06);
    position: absolute;
    top: -20px;
    right: 20px;
    line-height: 1;
    pointer-events: none;
}
.summary-eyebrow {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--accent-blue);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.summary-text {
    font-family: var(--font-sans);
    font-size: 15px;
    color: var(--text-secondary);
    line-height: 1.75;
    font-weight: 300;
    font-style: italic;
}

/* ── Metric Strip ─────────────────────────────────── */
.metrics-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}
.metric-tile {
    background: var(--bg-elevated);
    border: 1px solid var(--bg-border);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.metric-tile:hover {
    border-color: var(--accent-blue);
    transform: translateY(-2px);
}
.metric-tile::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
}
.mt-score::before  { background: linear-gradient(90deg, var(--accent-blue), var(--accent-violet)); }
.mt-bugs::before   { background: linear-gradient(90deg, var(--accent-green), var(--accent-teal)); }
.mt-perf::before   { background: linear-gradient(90deg, var(--accent-amber), #FB923C); }
.mt-sec::before    { background: linear-gradient(90deg, var(--accent-rose),  #FB7185); }

.metric-label {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.metric-value {
    font-family: var(--font-display);
    font-size: 38px;
    font-style: italic;
    line-height: 1;
    letter-spacing: -1px;
}
.mv-score  { color: var(--accent-blue); }
.mv-bugs   { color: var(--accent-green); }
.mv-perf   { color: var(--accent-amber); }
.mv-sec    { color: var(--accent-rose); }

.metric-sub {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-muted);
    margin-top: 6px;
}

/* ── Review Section Cards ─────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}
.section-title {
    font-family: var(--font-display);
    font-size: 22px;
    font-style: italic;
    color: var(--text-primary);
    letter-spacing: -0.3px;
}
.section-count {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
    background: var(--bg-elevated);
    padding: 4px 10px;
    border-radius: 20px;
    border: 1px solid var(--bg-border);
}

/* Finding items */
.finding {
    background: var(--bg-elevated);
    border: 1px solid var(--bg-border);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    margin-bottom: 10px;
    transition: border-color 0.15s ease, background 0.15s ease;
    display: flex;
    gap: 14px;
    align-items: flex-start;
}
.finding:hover {
    background: var(--bg-hover);
    border-color: rgba(74,158,255,0.25);
}
.finding-icon {
    width: 32px;
    height: 32px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    margin-top: 1px;
}
.fi-bug  { background: rgba(52,211,153,0.1);  }
.fi-perf { background: rgba(245,158,11,0.1);  }
.fi-sec  { background: rgba(248,113,113,0.1); }

.finding-body { flex: 1; min-width: 0; }
.finding-desc {
    font-family: var(--font-sans);
    font-size: 13.5px;
    color: var(--text-secondary);
    line-height: 1.6;
    font-weight: 300;
}
.finding-desc code {
    font-family: var(--font-mono);
    font-size: 12px;
    background: rgba(74,158,255,0.1);
    color: var(--accent-blue);
    padding: 1px 6px;
    border-radius: 4px;
    word-break: break-word;
    white-space: normal;
}
.finding-meta {
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sev-badge {
    font-family: var(--font-mono);
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.sev-critical { background: rgba(248,113,113,0.15); color: #FCA5A5; border: 1px solid rgba(248,113,113,0.25); }
.sev-high     { background: rgba(251,146,60,0.15);  color: #FED7AA; border: 1px solid rgba(251,146,60,0.25); }
.sev-medium   { background: rgba(250,204,21,0.15);  color: #FEF08A; border: 1px solid rgba(250,204,21,0.25); }
.sev-low      { background: rgba(52,211,153,0.15);  color: #A7F3D0; border: 1px solid rgba(52,211,153,0.25); }

.finding-loc {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-muted);
}

/* Empty finding */
.finding-empty {
    background: var(--bg-elevated);
    border: 1px dashed var(--bg-border);
    border-radius: var(--radius-md);
    padding: 20px;
    text-align: center;
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--text-muted);
    letter-spacing: 0.3px;
}

/* ── Score Display ────────────────────────────────── */
.score-display {
    background: var(--bg-elevated);
    border: 1px solid var(--bg-border);
    border-radius: var(--radius-lg);
    padding: 40px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    min-height: 260px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.score-display::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(74,158,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.score-ring {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 2px solid var(--bg-border);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    position: relative;
    background: conic-gradient(var(--accent-blue) calc(var(--pct) * 1%), var(--bg-border) 0%);
}
.score-ring-inner {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    background: var(--bg-elevated);
    display: flex;
    align-items: center;
    justify-content: center;
}
.score-big {
    font-family: var(--font-display);
    font-size: 48px;
    font-style: italic;
    color: var(--accent-blue);
    line-height: 1;
    letter-spacing: -2px;
}
.score-out {
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}
.score-verdict {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 20px;
    margin-top: 12px;
}
.sv-excellent { background: rgba(52,211,153,0.12); color: var(--accent-green);  border: 1px solid rgba(52,211,153,0.2); }
.sv-good      { background: rgba(74,158,255,0.12); color: var(--accent-blue);   border: 1px solid rgba(74,158,255,0.2); }
.sv-average   { background: rgba(245,158,11,0.12); color: var(--accent-amber);  border: 1px solid rgba(245,158,11,0.2); }
.sv-poor      { background: rgba(248,113,113,0.12);color: var(--accent-rose);   border: 1px solid rgba(248,113,113,0.2); }

/* ── Section divider ──────────────────────────────── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--bg-border), transparent);
    margin: 32px 0;
}

/* ── History Items ────────────────────────────────── */
.history-item {
    background: var(--bg-elevated);
    border: 1px solid var(--bg-border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: border-color 0.15s ease;
}
.history-item:hover { border-color: rgba(74,158,255,0.3); }
.history-pr {
    font-family: var(--font-mono);
    font-size: 13px;
    color: var(--accent-blue);
    font-weight: 500;
}
.history-title {
    font-family: var(--font-sans);
    font-size: 14px;
    color: var(--text-primary);
    font-weight: 400;
    margin-top: 3px;
}
.history-meta {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ── Sidebar ──────────────────────────────────────── */
.sb-header {
    padding: 28px 20px 20px 20px;
    border-bottom: 1px solid var(--bg-border);
    margin-bottom: 24px;
}
.sb-logo {
    font-family: var(--font-display);
    font-size: 22px;
    font-style: italic;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}
.sb-tagline {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--accent-teal);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 5px;
}
.sb-label {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
    padding: 0 20px;
}
.sb-info {
    padding: 16px 20px;
    margin-top: 24px;
    border-top: 1px solid var(--bg-border);
}
.sb-info-title {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.sb-step {
    font-family: var(--font-sans);
    font-size: 13px;
    color: var(--text-secondary);
    padding: 8px 0;
    border-bottom: 1px solid var(--bg-border);
    font-weight: 300;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sb-step:last-child { border-bottom: none; }
.sb-step-num {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--accent-blue);
    background: rgba(74,158,255,0.1);
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

/* ── Streamlit overrides ──────────────────────────── */
.stTextInput > label, .stNumberInput > label,
.stSelectbox > label { display: none !important; }

.stTextInput input, .stNumberInput input {
    background: var(--bg-base) !important;
    border: 1px solid var(--bg-border) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(74,158,255,0.1) !important;
    outline: none !important;
}

.stSelectbox > div > div {
    background: var(--bg-base) !important;
    border: 1px solid var(--bg-border) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
}

.stButton > button {
    background: var(--accent-blue) !important;
    color: #060910 !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-mono) !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
    padding: 12px 20px !important;
    transition: all 0.15s ease !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: #6AB4FF !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(74,158,255,0.3) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--bg-border) !important;
    gap: 0 !important;
    margin-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    padding: 14px 24px !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    transition: color 0.15s ease !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-blue) !important;
    border-bottom: 2px solid var(--accent-blue) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 32px !important;
}

[data-testid="stExpander"] {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--bg-border) !important;
    border-radius: var(--radius-md) !important;
    margin-bottom: 10px !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-primary) !important;
    font-family: var(--font-sans) !important;
    font-size: 14px !important;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
    font-style: italic !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

div[data-testid="stSpinner"] p {
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.5px !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# CONSTANTS & HELPERS
# ══════════════════════════════════════════════════════

API_URL = " https://ai-reviewer-backend-sz5k.onrender.com"


def fetch_prs(repo):
    try:
        r = requests.get(f"{API_URL}/prs", params={"repo": repo, "limit": 10}, timeout=10)
        return r.json().get("prs", []) if r.status_code == 200 else []
    except: return []


def get_review(repo, pr_num):
    try:
        r = requests.post(f"{API_URL}/review",
                          json={"repo": repo, "pr_number": int(pr_num)}, timeout=60)
        return (r.json(), None) if r.status_code == 200 else (None, f"Error {r.status_code}: {r.text}")
    except requests.exceptions.ConnectionError: return (None, "conn")
    except Exception as e: return (None, str(e))


def get_history():
    try:
        r = requests.get(f"{API_URL}/history", timeout=10)
        return r.json().get("reviews", []) if r.status_code == 200 else []
    except: return []


def score_info(s):
    if s >= 9: return ("EXCELLENT", "sv-excellent", "◆◆◆◆◆")
    if s >= 7: return ("GOOD",      "sv-good",      "◆◆◆◆◇")
    if s >= 5: return ("AVERAGE",   "sv-average",   "◆◆◆◇◇")
    return           ("NEEDS WORK", "sv-poor",      "◆◇◇◇◇")


def sev_badge(sev):
    s = (sev or "low").lower()
    return f'<span class="sev-badge sev-{s}">{s}</span>'


def finding_html(icon, fi_class, items, kind="bug"):
    if not items:
        return f'<div class="finding-empty">◈ No {kind}s detected in this pull request</div>'
    out = ""
    for it in items:
        if isinstance(it, dict):
            desc = it.get("description", "")
            loc  = it.get("line", "")
            sev  = it.get("severity", "")
        else:
            desc, loc, sev = str(it), "", ""
        badge = sev_badge(sev) if sev else ""
        loc_html = f'<span class="finding-loc">◍ {loc}</span>' if loc else ""
        out += f"""
        <div class="finding">
            <div class="finding-icon {fi_class}">{icon}</div>
            <div class="finding-body">
                <div class="finding-desc">{desc}</div>
                <div class="finding-meta">{badge}{loc_html}</div>
            </div>
        </div>"""
    return out


# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
        <div class="sb-header">
            <div class="sb-logo">CodeSense</div>
            <div class="sb-tagline">AI · Code · Review</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-label">Repository</div>', unsafe_allow_html=True)
    repo_url = st.text_input("r", value="", label_visibility="collapsed", placeholder="username/repo")
     
    st.markdown('<div class="sb-label" style="margin-top:14px;">Pull Request</div>',
                unsafe_allow_html=True)
    pr_number = st.number_input("p", min_value=1, step=1, value=1, label_visibility="collapsed")

    if repo_url:
        st.markdown('<div class="sb-label" style="margin-top:14px;">Select PR</div>',
                    unsafe_allow_html=True)
        with st.spinner(""):
            prs = fetch_prs(repo_url)
        if prs:
            opts = {f"#{p['number']}  {p['title'][:36]}…": p['number'] for p in prs}
            sel  = st.selectbox("s", list(opts.keys()), label_visibility="collapsed")
            pr_number = opts[sel]

    st.markdown("<br>", unsafe_allow_html=True)
    clicked = st.button("◈  Run Analysis", use_container_width=True)

    st.markdown("""
        <div class="sb-info">
            <div class="sb-info-title">Workflow</div>
            <div class="sb-step"><span class="sb-step-num">1</span>Enter repository path</div>
            <div class="sb-step"><span class="sb-step-num">2</span>Choose a pull request</div>
            <div class="sb-step"><span class="sb-step-num">3</span>Run analysis</div>
            <div class="sb-step"><span class="sb-step-num">4</span>Review AI findings</div>
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TOP BAR
# ══════════════════════════════════════════════════════

st.markdown(f"""
    <div class="topbar">
        <div class="topbar-logo">
            <div class="topbar-symbol">◈</div>
            <div class="topbar-name">CodeSense</div>
            <div class="topbar-version">v1.0</div>
        </div>
        <div class="topbar-status">
            <div class="status-dot"></div>
            Groq LLaMA 3 · Connected
        </div>
    </div>
    <div class="page-content">
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════

st.markdown(f"""
    <div class="page-header">
        <div class="page-eyebrow">Pull Request Analysis</div>
        <div class="page-title">AI-Powered<br><em>Code Review</em></div>
        <div class="page-desc">
            Automated static analysis and AI review for GitHub pull requests.
            Powered by Groq LLaMA 3.
        </div>
    </div>

    <div class="context-strip">
        <div>
            <div class="context-repo">{repo_url} / pull / {pr_number}</div>
            <div class="context-pr">PR #{pr_number} · GitHub Repository</div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
            <span class="context-pill pill-date">{datetime.now().strftime('%b %d, %Y')}</span>
            <a class="context-pill pill-github"
               href="https://github.com/{repo_url}/pull/{pr_number}" target="_blank">
               View on GitHub ↗
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════

tab1, tab2 = st.tabs(["◈  Analysis", "◎  History"])


# ══════════════════════════════════════════════════════
# TAB 1 — ANALYSIS
# ══════════════════════════════════════════════════════

with tab1:

    if clicked:
        if not repo_url:
            st.warning("Enter a repository path in the sidebar.")
        else:
            with st.spinner("Running analysis — fetching diff and invoking AI model..."):
                result, err = get_review(repo_url, pr_number)

            if err == "conn":
                st.error("**Backend offline.** Start the server: `uvicorn backend.api:app --reload`")
            elif err:
                st.error(f"**Error:** {err}")
            else:
                review = result.get("review", {})
                bugs   = review.get("bugs", [])
                imps   = review.get("improvements", [])
                secs   = review.get("security_issues", [])
                score  = int(review.get("quality_score", 0))
                summ   = review.get("summary", "")
                sv_text, sv_cls, _ = score_info(score)
                pct = score * 10

                # Summary
                if summ:
                    st.markdown(f"""
                        <div class="summary-card">
                            <div class="summary-eyebrow">AI Summary</div>
                            <div class="summary-text">{summ}</div>
                        </div>
                    """, unsafe_allow_html=True)

                # Metrics strip
                st.markdown(f"""
                    <div class="metrics-strip">
                        <div class="metric-tile mt-score">
                            <div class="metric-label">Quality Score</div>
                            <div class="metric-value mv-score">{score}</div>
                            <div class="metric-sub">out of 10</div>
                        </div>
                        <div class="metric-tile mt-bugs">
                            <div class="metric-label">Bugs Found</div>
                            <div class="metric-value mv-bugs">{len(bugs)}</div>
                            <div class="metric-sub">issues detected</div>
                        </div>
                        <div class="metric-tile mt-perf">
                            <div class="metric-label">Improvements</div>
                            <div class="metric-value mv-perf">{len(imps)}</div>
                            <div class="metric-sub">suggestions</div>
                        </div>
                        <div class="metric-tile mt-sec">
                            <div class="metric-label">Security</div>
                            <div class="metric-value mv-sec">{len(secs)}</div>
                            <div class="metric-sub">vulnerabilities</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

                # Three columns of findings + score
                c1, c2, c3, c4 = st.columns([3, 3, 3, 2])

                with c1:
                    st.markdown(f"""
                        <div class="section-header">
                            <div class="section-title">Bugs</div>
                            <div class="section-count">{len(bugs)} found</div>
                        </div>
                        {finding_html("🪲", "fi-bug", bugs, "bug")}
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown(f"""
                        <div class="section-header">
                            <div class="section-title">Performance</div>
                            <div class="section-count">{len(imps)} suggestions</div>
                        </div>
                        {finding_html("⚡", "fi-perf", imps, "suggestion")}
                    """, unsafe_allow_html=True)

                with c3:
                    st.markdown(f"""
                        <div class="section-header">
                            <div class="section-title">Security</div>
                            <div class="section-count">{len(secs)} issues</div>
                        </div>
                        {finding_html("🔒", "fi-sec", secs, "security issue")}
                    """, unsafe_allow_html=True)

                with c4:
                    st.markdown(f"""
                        <div class="score-display" style="--pct:{pct};">
                            <div class="score-ring">
                                <div class="score-ring-inner">
                                    <div class="score-big">{score}</div>
                                </div>
                            </div>
                            <div class="score-out">/ 10 quality score</div>
                            <div class="score-verdict {sv_cls}">{sv_text}</div>
                        </div>
                    """, unsafe_allow_html=True)

    else:
        st.markdown("""
            <div style="text-align:center; padding: 80px 0 60px 0;">
                <div style="font-size:48px; margin-bottom:20px; opacity:0.3;">◈</div>
                <div style="font-family:var(--font-display); font-size:24px;
                     font-style:italic; color:var(--text-muted); margin-bottom:10px;">
                    Ready to analyse
                </div>
                <div style="font-family:var(--font-mono); font-size:12px;
                     color:var(--text-muted); letter-spacing:1px;">
                    Configure a repository in the sidebar and click Run Analysis
                </div>
            </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TAB 2 — HISTORY
# ══════════════════════════════════════════════════════

with tab2:

    history = get_history()

    if not history:
        st.markdown("""
            <div style="text-align:center; padding:80px 0 60px 0;">
                <div style="font-size:40px; margin-bottom:20px; opacity:0.3;">◎</div>
                <div style="font-family:var(--font-display); font-size:24px;
                     font-style:italic; color:var(--text-muted); margin-bottom:10px;">
                    No history yet
                </div>
                <div style="font-family:var(--font-mono); font-size:12px;
                     color:var(--text-muted); letter-spacing:1px;">
                    Reviews appear here after analysis
                </div>
            </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
            <div style="font-family:var(--font-mono); font-size:10px; color:var(--accent-blue);
            letter-spacing:2px; text-transform:uppercase; margin-bottom:20px;">
                {len(history)} past review(s)
            </div>
        """, unsafe_allow_html=True)

        for item in history:
            rev    = item.get("review", {})
            score  = int(rev.get("quality_score", 0))
            sv_t, sv_c, _ = score_info(score)

            with st.expander(f"  #{item['pr_number']}  —  {item.get('pr_title','PR Review')[:60]}"):

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Score",    f"{score}/10")
                m2.metric("Bugs",     len(rev.get("bugs", [])))
                m3.metric("Security", len(rev.get("security_issues", [])))
                m4.metric("Repo",     item.get("repo", ""))

                st.markdown(f"""
                    <div style="font-family:var(--font-mono); font-size:11px;
                    color:var(--text-muted); margin-top:12px; padding-top:12px;
                    border-top:1px solid var(--bg-border); display:flex; gap:16px;">
                        <span>👤 {item.get('pr_author','—')}</span>
                        <span>🕐 {item.get('created_at','')[:16]}</span>
                        <a href="{item.get('pr_url','#')}" target="_blank"
                           style="color:var(--accent-blue); text-decoration:none;">
                           View PR ↗
                        </a>
                    </div>
                """, unsafe_allow_html=True)

                if rev.get("summary"):
                    st.markdown(f"""
                        <div class="summary-card" style="margin-top:16px;margin-bottom:0;">
                            <div class="summary-eyebrow">Summary</div>
                            <div class="summary-text">{rev['summary']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# Close page-content div
st.markdown("</div>", unsafe_allow_html=True)
