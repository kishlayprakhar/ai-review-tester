import streamlit as st
import requests
from datetime import datetime

# how to run: streamlit run frontend/frontend_app.py

st.set_page_config(
    page_title = "CodeSense — AI Code Review",
    page_icon  = "◈",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400;1,9..144,500&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --base:        #05080F;
    --surface:     #090D18;
    --raised:      #0E1420;
    --overlay:     #131A2B;
    --border:      rgba(255,255,255,0.07);
    --border-mid:  rgba(255,255,255,0.12);
    --border-hi:   rgba(255,255,255,0.20);

    --ink:         #EDF0F7;
    --ink-2:       #8895A7;
    --ink-3:       #4E5A6B;
    --ink-4:       #2C3444;

    --blue:        #5B9EFF;
    --blue-dim:    rgba(91,158,255,0.12);
    --blue-glow:   rgba(91,158,255,0.25);
    --teal:        #2DCBA8;
    --teal-dim:    rgba(45,203,168,0.12);
    --amber:       #F0A732;
    --amber-dim:   rgba(240,167,50,0.12);
    --rose:        #F06680;
    --rose-dim:    rgba(240,102,128,0.12);
    --violet:      #9B87FF;
    --violet-dim:  rgba(155,135,255,0.12);
    --green:       #3DD68C;
    --green-dim:   rgba(61,214,140,0.12);

    --ff-display:  'Fraunces', Georgia, serif;
    --ff-sans:     'IBM Plex Sans', system-ui, sans-serif;
    --ff-mono:     'IBM Plex Mono', 'Fira Code', monospace;

    --r-sm:  5px;
    --r-md:  9px;
    --r-lg:  14px;
    --r-xl:  20px;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main .block-container {
    background: var(--base) !important;
    color: var(--ink) !important;
    font-family: var(--ff-sans) !important;
}
.main .block-container { padding-top: 0 !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-mid); border-radius: 2px; }

/* ── NAV BAR ─────────────────────────────────── */
.nav {
    height: 58px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 44px;
    position: sticky;
    top: 0;
    z-index: 200;
}
.nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-logo {
    font-family: var(--ff-display);
    font-style: italic;
    font-size: 21px;
    font-weight: 400;
    color: var(--ink);
    letter-spacing: -0.4px;
}
.nav-badge {
    font-family: var(--ff-mono);
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--ink-3);
    background: var(--overlay);
    border: 1px solid var(--border-mid);
    padding: 2px 7px;
    border-radius: var(--r-sm);
}
.nav-right {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: var(--ff-mono);
    font-size: 11px;
    color: var(--ink-3);
}
.nav-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    animation: blink 2.5s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.35} }

/* ── SIDEBAR ─────────────────────────────────── */
.sb-top {
    padding: 30px 22px 22px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 22px;
}
.sb-wordmark {
    font-family: var(--ff-display);
    font-style: italic;
    font-size: 24px;
    font-weight: 400;
    color: var(--ink);
    letter-spacing: -0.5px;
    line-height: 1;
}
.sb-sub {
    font-family: var(--ff-mono);
    font-size: 10px;
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--teal);
    margin-top: 6px;
}
.sb-lbl {
    font-family: var(--ff-mono);
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--ink-3);
    margin-bottom: 7px;
    padding: 0 22px;
}
.sb-steps {
    padding: 20px 22px 0;
    border-top: 1px solid var(--border);
    margin-top: 22px;
}
.sb-steps-title {
    font-family: var(--ff-mono);
    font-size: 9px;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--ink-3);
    margin-bottom: 14px;
}
.sb-step {
    display: flex;
    align-items: flex-start;
    gap: 11px;
    padding: 9px 0;
    border-bottom: 1px solid var(--border);
    font-family: var(--ff-sans);
    font-size: 13px;
    font-weight: 300;
    color: var(--ink-2);
    line-height: 1.4;
}
.sb-step:last-child { border-bottom: none; }
.sb-num {
    font-family: var(--ff-mono);
    font-size: 9px;
    font-weight: 500;
    color: var(--blue);
    background: var(--blue-dim);
    width: 19px;
    height: 19px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}

/* ── MAIN CONTENT ────────────────────────────── */
.wrap { padding: 42px 52px 60px; animation: rise 0.45s ease forwards; }
@keyframes rise { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }

/* ── HERO ─────────────────────────────────────── */
.hero { margin-bottom: 40px; }
.hero-label {
    font-family: var(--ff-mono);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--blue);
    margin-bottom: 14px;
}
.hero-title {
    font-family: var(--ff-display);
    font-style: italic;
    font-size: 52px;
    font-weight: 300;
    color: var(--ink);
    line-height: 1.02;
    letter-spacing: -1.5px;
    margin-bottom: 14px;
}
.hero-title span { color: var(--blue); }
.hero-desc {
    font-family: var(--ff-sans);
    font-size: 15px;
    font-weight: 300;
    color: var(--ink-2);
    line-height: 1.65;
    max-width: 520px;
}

/* ── PR CONTEXT BAR ──────────────────────────── */
.ctx-bar {
    background: var(--raised);
    border: 1px solid var(--border);
    border-left: 3px solid var(--blue);
    border-radius: var(--r-lg);
    padding: 16px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 34px;
}
.ctx-repo {
    font-family: var(--ff-mono);
    font-size: 13.5px;
    font-weight: 500;
    color: var(--blue);
    letter-spacing: -0.2px;
}
.ctx-pr {
    font-family: var(--ff-mono);
    font-size: 11px;
    color: var(--ink-3);
    margin-top: 4px;
}
.ctx-pills { display: flex; align-items: center; gap: 8px; }
.pill {
    font-family: var(--ff-mono);
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 5px 12px;
    border-radius: 20px;
    white-space: nowrap;
}
.pill-date  { background: var(--overlay); color: var(--ink-3); border: 1px solid var(--border-mid); }
.pill-link  { background: var(--blue-dim); color: var(--blue); border: 1px solid rgba(91,158,255,0.25);
              text-decoration: none; display: inline-block; }
.pill-link:hover { background: var(--blue-glow); }

/* ── TABS ─────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    margin-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--ink-3) !important;
    font-family: var(--ff-mono) !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    padding: 14px 26px !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    transition: color 0.15s ease !important;
}
.stTabs [aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom: 2px solid var(--blue) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 36px !important; }

/* ── SUMMARY ──────────────────────────────────── */
.summary-wrap {
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 24px 28px;
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}
.summary-wrap::after {
    content: '"';
    font-family: var(--ff-display);
    font-size: 130px;
    color: rgba(91,158,255,0.05);
    position: absolute;
    top: -24px; right: 18px;
    line-height: 1;
    pointer-events: none;
}
.summary-label {
    font-family: var(--ff-mono);
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--blue);
    margin-bottom: 12px;
}
.summary-body {
    font-family: var(--ff-sans);
    font-size: 15px;
    font-weight: 300;
    font-style: italic;
    color: var(--ink-2);
    line-height: 1.75;
}

/* ── METRIC TILES ────────────────────────────── */
.tiles {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 30px;
}
.tile {
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 18px 20px 16px;
    position: relative;
    overflow: hidden;
    cursor: default;
    transition: border-color 0.2s, transform 0.2s;
}
.tile:hover { border-color: var(--border-hi); transform: translateY(-2px); }
.tile::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0 0 var(--r-md) var(--r-md);
}
.tile-score::after  { background: linear-gradient(90deg, var(--blue), var(--violet)); }
.tile-bugs::after   { background: linear-gradient(90deg, var(--green), var(--teal)); }
.tile-perf::after   { background: linear-gradient(90deg, var(--amber), #fb923c); }
.tile-sec::after    { background: linear-gradient(90deg, var(--rose), #fb7185); }
.tile-label {
    font-family: var(--ff-mono);
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--ink-3);
    margin-bottom: 11px;
}
.tile-val {
    font-family: var(--ff-display);
    font-style: italic;
    font-size: 40px;
    font-weight: 300;
    line-height: 1;
    letter-spacing: -1.5px;
}
.tv-score  { color: var(--blue); }
.tv-bugs   { color: var(--green); }
.tv-perf   { color: var(--amber); }
.tv-sec    { color: var(--rose); }
.tile-hint {
    font-family: var(--ff-mono);
    font-size: 10px;
    color: var(--ink-4);
    margin-top: 7px;
}

/* ── DIVIDER ─────────────────────────────────── */
.rule {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-mid), transparent);
    margin: 30px 0;
}

/* ── SECTION HEADER ──────────────────────────── */
.sec-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}
.sec-title {
    font-family: var(--ff-display);
    font-style: italic;
    font-size: 22px;
    font-weight: 300;
    color: var(--ink);
    letter-spacing: -0.3px;
}
.sec-count {
    font-family: var(--ff-mono);
    font-size: 10px;
    color: var(--ink-3);
    background: var(--overlay);
    border: 1px solid var(--border-mid);
    padding: 3px 10px;
    border-radius: 20px;
}

/* ── FINDING CARD ─────────────────────────────── */
.finding {
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 14px 16px;
    margin-bottom: 9px;
    display: flex;
    gap: 13px;
    align-items: flex-start;
    transition: border-color 0.15s, background 0.15s;
}
.finding:hover { background: var(--overlay); border-color: var(--border-mid); }
.f-icon {
    width: 30px; height: 30px;
    border-radius: var(--r-sm);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; flex-shrink: 0; margin-top: 1px;
}
.fi-bug  { background: var(--green-dim); }
.fi-perf { background: var(--amber-dim); }
.fi-sec  { background: var(--rose-dim); }
.f-body { flex: 1; min-width: 0; }
.f-desc {
    font-family: var(--ff-sans);
    font-size: 13px;
    font-weight: 300;
    color: var(--ink-2);
    line-height: 1.58;
}
.f-desc code {
    font-family: var(--ff-mono);
    font-size: 11.5px;
    background: var(--blue-dim);
    color: var(--blue);
    padding: 1px 5px;
    border-radius: 3px;
}
.f-foot { margin-top: 8px; display: flex; align-items: center; gap: 7px; flex-wrap: wrap; }
.sev {
    font-family: var(--ff-mono);
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 2px 7px;
    border-radius: 3px;
}
.sev-critical { background:rgba(240,102,128,0.15); color:#f9a8b8; border:1px solid rgba(240,102,128,0.25); }
.sev-high     { background:rgba(251,146,60,0.15);  color:#fcd4aa; border:1px solid rgba(251,146,60,0.25); }
.sev-medium   { background:rgba(240,167,50,0.15);  color:#fde78a; border:1px solid rgba(240,167,50,0.25); }
.sev-low      { background:rgba(61,214,140,0.15);  color:#a7f3d0; border:1px solid rgba(61,214,140,0.25); }
.f-loc {
    font-family: var(--ff-mono);
    font-size: 10px;
    color: var(--ink-4);
}
.f-empty {
    background: var(--raised);
    border: 1px dashed var(--border-mid);
    border-radius: var(--r-md);
    padding: 22px;
    text-align: center;
    font-family: var(--ff-mono);
    font-size: 11px;
    color: var(--ink-4);
    letter-spacing: 0.3px;
}

/* ── SCORE RING ───────────────────────────────── */
.score-card {
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 36px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 280px;
    position: relative;
    overflow: hidden;
}
.score-card::before {
    content:'';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% -10%, rgba(91,158,255,0.07) 0%, transparent 65%);
    pointer-events: none;
}
.score-ring {
    width: 110px; height: 110px;
    border-radius: 50%;
    background: conic-gradient(var(--blue) calc(var(--pct) * 1%), var(--overlay) 0%);
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 18px;
}
.score-inner {
    width: 86px; height: 86px;
    border-radius: 50%;
    background: var(--raised);
    display: flex; align-items: center; justify-content: center;
}
.score-num {
    font-family: var(--ff-display);
    font-style: italic;
    font-size: 46px;
    font-weight: 300;
    color: var(--blue);
    letter-spacing: -2px;
    line-height: 1;
}
.score-den {
    font-family: var(--ff-mono);
    font-size: 11px;
    color: var(--ink-3);
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}
.score-verdict {
    font-family: var(--ff-mono);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
}
.sv-excellent { background: var(--green-dim);  color: var(--green);  border: 1px solid rgba(61,214,140,0.25); }
.sv-good      { background: var(--blue-dim);   color: var(--blue);   border: 1px solid rgba(91,158,255,0.25); }
.sv-average   { background: var(--amber-dim);  color: var(--amber);  border: 1px solid rgba(240,167,50,0.25); }
.sv-poor      { background: var(--rose-dim);   color: var(--rose);   border: 1px solid rgba(240,102,128,0.25); }

/* ── EMPTY STATE ─────────────────────────────── */
.empty {
    text-align: center;
    padding: 80px 0 60px;
}
.empty-sym { font-size: 42px; color: var(--ink-4); margin-bottom: 18px; }
.empty-head {
    font-family: var(--ff-display);
    font-style: italic;
    font-size: 26px;
    font-weight: 300;
    color: var(--ink-3);
    margin-bottom: 10px;
    letter-spacing: -0.4px;
}
.empty-sub {
    font-family: var(--ff-mono);
    font-size: 11px;
    color: var(--ink-4);
    letter-spacing: 0.5px;
    line-height: 1.6;
}

/* ── HISTORY EXPANDERS ───────────────────────── */
[data-testid="stExpander"] {
    background: var(--raised) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-md) !important;
    margin-bottom: 9px !important;
}
[data-testid="stExpander"] details summary {
    font-family: var(--ff-sans) !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    color: var(--ink) !important;
    padding: 14px 18px !important;
}
[data-testid="stExpander"] details[open] summary {
    border-bottom: 1px solid var(--border) !important;
}

/* ── STREAMLIT ELEMENTS ──────────────────────── */
.stTextInput > label,
.stNumberInput > label,
.stSelectbox > label { display: none !important; }

.stTextInput input, .stNumberInput input {
    background: var(--base) !important;
    border: 1px solid var(--border-mid) !important;
    color: var(--ink) !important;
    border-radius: var(--r-md) !important;
    font-family: var(--ff-mono) !important;
    font-size: 12.5px !important;
    padding: 10px 13px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(91,158,255,0.12) !important;
    outline: none !important;
}
.stSelectbox > div > div {
    background: var(--base) !important;
    border: 1px solid var(--border-mid) !important;
    color: var(--ink) !important;
    border-radius: var(--r-md) !important;
    font-family: var(--ff-mono) !important;
    font-size: 11.5px !important;
}
.stButton > button {
    background: var(--blue) !important;
    color: #04080F !important;
    border: none !important;
    border-radius: var(--r-md) !important;
    font-family: var(--ff-mono) !important;
    font-weight: 500 !important;
    font-size: 11px !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    padding: 13px 20px !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #7AB4FF !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(91,158,255,0.3) !important;
}
[data-testid="stMetricValue"] {
    color: var(--ink) !important;
    font-family: var(--ff-display) !important;
    font-style: italic !important;
    font-size: 28px !important;
}
[data-testid="stMetricLabel"] {
    color: var(--ink-3) !important;
    font-family: var(--ff-mono) !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
}
div[data-testid="stSpinner"] p {
    font-family: var(--ff-mono) !important;
    font-size: 12px !important;
    color: var(--ink-3) !important;
    letter-spacing: 0.5px !important;
}
.stAlert {
    background: var(--raised) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--r-md) !important;
    font-family: var(--ff-sans) !important;
    font-size: 14px !important;
    color: var(--ink) !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# CONFIG & HELPERS
# ══════════════════════════════════════════════════════

API_URL = "http://localhost:8000"


def fetch_prs(repo):
    try:
        r = requests.get(f"{API_URL}/prs", params={"repo": repo, "limit": 10}, timeout=10)
        return r.json().get("prs", []) if r.status_code == 200 else []
    except:
        return []


def get_review(repo, pr_num):
    try:
        r = requests.post(f"{API_URL}/review",
                          json={"repo": repo, "pr_number": int(pr_num)},
                          timeout=60)
        return (r.json(), None) if r.status_code == 200 else (None, f"Error {r.status_code}: {r.text}")
    except requests.exceptions.ConnectionError:
        return (None, "conn")
    except Exception as e:
        return (None, str(e))


def get_history():
    try:
        r = requests.get(f"{API_URL}/history", timeout=10)
        return r.json().get("reviews", []) if r.status_code == 200 else []
    except:
        return []


def score_info(s):
    if s >= 9: return "EXCELLENT", "sv-excellent"
    if s >= 7: return "GOOD",      "sv-good"
    if s >= 5: return "AVERAGE",   "sv-average"
    return           "NEEDS WORK", "sv-poor"


def sev_html(sev):
    s = (sev or "low").lower()
    return f'<span class="sev sev-{s}">{s}</span>'


def findings_html(icon, cls, items, kind):
    if not items:
        return f'<div class="f-empty">◈ &nbsp; No {kind}s detected in this pull request</div>'
    out = ""
    for it in items:
        if isinstance(it, dict):
            desc = it.get("description", "")
            loc  = it.get("line", "")
            sev  = it.get("severity", "")
        else:
            desc, loc, sev = str(it), "", ""
        badge   = sev_html(sev) if sev else ""
        loc_tag = f'<span class="f-loc">◍ {loc}</span>' if loc else ""
        out += f"""
        <div class="finding">
            <div class="f-icon {cls}">{icon}</div>
            <div class="f-body">
                <div class="f-desc">{desc}</div>
                <div class="f-foot">{badge}{loc_tag}</div>
            </div>
        </div>"""
    return out


# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
        <div class="sb-top">
            <div class="sb-wordmark">CodeSense</div>
            <div class="sb-sub">AI · Code · Review</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-lbl">Repository</div>', unsafe_allow_html=True)
    repo_url = st.text_input("repo", value="", label_visibility="collapsed",
                              placeholder="username/repo")

    st.markdown('<div class="sb-lbl" style="margin-top:14px;">Pull Request #</div>',
                unsafe_allow_html=True)
    pr_number = st.number_input("pr", min_value=1, step=1, value=1,
                                 label_visibility="collapsed")

    if repo_url:
        st.markdown('<div class="sb-lbl" style="margin-top:14px;">Quick Select</div>',
                    unsafe_allow_html=True)
        with st.spinner(""):
            prs = fetch_prs(repo_url)
        if prs:
            opts = {f"#{p['number']}  {p['title'][:34]}…": p["number"] for p in prs}
            sel  = st.selectbox("qs", list(opts.keys()), label_visibility="collapsed")
            pr_number = opts[sel]

    st.markdown("<br>", unsafe_allow_html=True)
    clicked = st.button("◈  Run Analysis")

    st.markdown("""
        <div class="sb-steps">
            <div class="sb-steps-title">Workflow</div>
            <div class="sb-step"><span class="sb-num">1</span>Enter repository path</div>
            <div class="sb-step"><span class="sb-num">2</span>Choose a pull request</div>
            <div class="sb-step"><span class="sb-num">3</span>Run analysis</div>
            <div class="sb-step"><span class="sb-num">4</span>Review AI findings</div>
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════════════════

st.markdown("""
    <div class="nav">
        <div class="nav-brand">
            <span style="font-size:20px;color:var(--blue);line-height:1;">◈</span>
            <span class="nav-logo">CodeSense</span>
            <span class="nav-badge">v1.0</span>
        </div>
        <div class="nav-right">
            <div class="nav-dot"></div>
            Groq LLaMA 3 &nbsp;·&nbsp; Connected
        </div>
    </div>
    <div class="wrap">
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════

st.markdown(f"""
    <div class="hero">
        <div class="hero-label">Pull Request Analysis</div>
        <div class="hero-title">AI-Powered<br><span>Code Review</span></div>
        <div class="hero-desc">
            Automated static analysis and intelligent code review for GitHub
            pull requests — catching bugs, security flaws and performance issues
            before they reach production.
        </div>
    </div>

    <div class="ctx-bar">
        <div>
            <div class="ctx-repo">{repo_url or "—"} / pull / {pr_number}</div>
            <div class="ctx-pr">PR #{pr_number} · GitHub Repository</div>
        </div>
        <div class="ctx-pills">
            <span class="pill pill-date">{datetime.now().strftime('%b %d, %Y')}</span>
            <a class="pill pill-link"
               href="https://github.com/{repo_url}/pull/{pr_number}"
               target="_blank">View on GitHub ↗</a>
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
            st.warning("⚠️  Enter a repository path in the sidebar first.")
        else:
            with st.spinner("Fetching diff and invoking AI model — this may take a moment..."):
                result, err = get_review(repo_url, pr_number)

            if err == "conn":
                st.error("🔌  **Backend offline.** Start the server:\n```\nuvicorn backend.api:app --reload\n```")
            elif err:
                st.error(f"❌  **{err}**")
            else:
                review = result.get("review", {})
                bugs   = review.get("bugs", [])
                imps   = review.get("improvements", [])
                secs   = review.get("security_issues", [])
                score  = int(review.get("quality_score", 0))
                summ   = review.get("summary", "")
                sv_t, sv_c = score_info(score)
                pct = score * 10

                # Summary
                if summ:
                    st.markdown(f"""
                        <div class="summary-wrap">
                            <div class="summary-label">AI Summary</div>
                            <div class="summary-body">{summ}</div>
                        </div>
                    """, unsafe_allow_html=True)

                # Metric tiles
                st.markdown(f"""
                    <div class="tiles">
                        <div class="tile tile-score">
                            <div class="tile-label">Quality Score</div>
                            <div class="tile-val tv-score">{score}</div>
                            <div class="tile-hint">out of 10</div>
                        </div>
                        <div class="tile tile-bugs">
                            <div class="tile-label">Bugs Found</div>
                            <div class="tile-val tv-bugs">{len(bugs)}</div>
                            <div class="tile-hint">issues detected</div>
                        </div>
                        <div class="tile tile-perf">
                            <div class="tile-label">Improvements</div>
                            <div class="tile-val tv-perf">{len(imps)}</div>
                            <div class="tile-hint">suggestions</div>
                        </div>
                        <div class="tile tile-sec">
                            <div class="tile-label">Security</div>
                            <div class="tile-val tv-sec">{len(secs)}</div>
                            <div class="tile-hint">vulnerabilities</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

                # Finding columns + score ring
                c1, c2, c3, c4 = st.columns([3, 3, 3, 2])

                with c1:
                    st.markdown(f"""
                        <div class="sec-head">
                            <div class="sec-title">Bugs</div>
                            <div class="sec-count">{len(bugs)} found</div>
                        </div>
                        {findings_html("🪲", "fi-bug", bugs, "bug")}
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown(f"""
                        <div class="sec-head">
                            <div class="sec-title">Performance</div>
                            <div class="sec-count">{len(imps)} suggestions</div>
                        </div>
                        {findings_html("⚡", "fi-perf", imps, "suggestion")}
                    """, unsafe_allow_html=True)

                with c3:
                    st.markdown(f"""
                        <div class="sec-head">
                            <div class="sec-title">Security</div>
                            <div class="sec-count">{len(secs)} issues</div>
                        </div>
                        {findings_html("🔒", "fi-sec", secs, "security issue")}
                    """, unsafe_allow_html=True)

                with c4:
                    st.markdown(f"""
                        <div class="score-card" style="--pct:{pct};">
                            <div class="score-ring">
                                <div class="score-inner">
                                    <div class="score-num">{score}</div>
                                </div>
                            </div>
                            <div class="score-den">/ 10 quality score</div>
                            <div class="score-verdict {sv_c}">{sv_t}</div>
                        </div>
                    """, unsafe_allow_html=True)

    else:
        st.markdown("""
            <div class="empty">
                <div class="empty-sym">◈</div>
                <div class="empty-head">Ready to analyse</div>
                <div class="empty-sub">
                    Enter a repository in the sidebar<br>
                    and click <strong style="color:var(--blue);">Run Analysis</strong> to begin
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
            <div class="empty">
                <div class="empty-sym">◎</div>
                <div class="empty-head">No history yet</div>
                <div class="empty-sub">
                    Completed reviews will appear here
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="font-family:var(--ff-mono);font-size:10px;color:var(--blue);
            letter-spacing:2px;text-transform:uppercase;margin-bottom:18px;">
                {len(history)} review(s) on record
            </div>
        """, unsafe_allow_html=True)

        for item in history:
            rev   = item.get("review", {})
            score = int(rev.get("quality_score", 0))
            sv_t, sv_c = score_info(score)

            with st.expander(
                f"#{item['pr_number']}  —  {item.get('pr_title','PR Review')[:62]}  ·  {score}/10"
            ):
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Score",    f"{score}/10")
                m2.metric("Bugs",     len(rev.get("bugs", [])))
                m3.metric("Security", len(rev.get("security_issues", [])))
                m4.metric("Repo",     item.get("repo", "—"))

                st.markdown(f"""
                    <div style="font-family:var(--ff-mono);font-size:11px;
                    color:var(--ink-3);margin-top:14px;padding-top:14px;
                    border-top:1px solid var(--border);display:flex;gap:18px;flex-wrap:wrap;">
                        <span>👤 {item.get('pr_author','—')}</span>
                        <span>🕐 {item.get('created_at','')[:16]}</span>
                        <a href="{item.get('pr_url','#')}" target="_blank"
                           style="color:var(--blue);text-decoration:none;">View PR ↗</a>
                    </div>
                """, unsafe_allow_html=True)

                if rev.get("summary"):
                    st.markdown(f"""
                        <div class="summary-wrap" style="margin-top:16px;margin-bottom:0;">
                            <div class="summary-label">Summary</div>
                            <div class="summary-body">{rev['summary']}</div>
                        </div>
                    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
