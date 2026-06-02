import streamlit as st
import requests
from datetime import datetime

# how to run: streamlit run frontend/frontend_app.py

st.set_page_config(
    page_title="CodeSentry — Instant AI Reviews",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide legacy sidebar elements
)

# ══════════════════════════════════════════════════════
# ROUTING CONTROLLER
# ══════════════════════════════════════════════════════
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'repo' not in st.session_state:
    st.session_state.repo = ''
if 'pr' not in st.session_state:
    st.session_state.pr = 1

def go_to_input():
    st.session_state.page = 'input'

def go_to_results(repo_url, pr_num):
    st.session_state.repo = repo_url
    st.session_state.pr = pr_num
    st.session_state.page = 'results'

def go_to_landing():
    st.session_state.page = 'landing'

# ══════════════════════════════════════════════════════
# REFINED HIGH-END RENDERING CSS ENGINE
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400;1,9..144,500&family=Inter:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg-base:       #F8FAFC;
    --bg-surface:    #FFFFFF;
    --border:        #E2E8F0;
    
    --text-main:     #0F172A;
    --text-muted:    #475569;
    --text-light:    #94A3B8;
    
    --accent:        #0F172A;
    --accent-hover:  #1E293B;
    
    --blue:          #2563EB;
    --blue-dim:      rgba(37, 99, 235, 0.06);
    --green:         #16A34A;
    --green-dim:     rgba(22, 163, 74, 0.06);
    --amber:         #D97706;
    --amber-dim:     rgba(217, 119, 6, 0.06);
    --rose:          #DC2626;
    --rose-dim:      rgba(220, 38, 38, 0.06);

    --ff-display:    'Fraunces', serif;
    --ff-sans:       'Inter', sans-serif;
    --ff-mono:       'Fira Code', monospace;
    
    --radius-md:     12px;
    --radius-lg:     24px;
}

/* Framework Clean Up Overrides */
html, body, [data-testid="stAppViewContainer"], .main .block-container {
    background-color: var(--bg-base) !important;
    color: var(--text-main) !important;
    font-family: var(--ff-sans) !important;
}
/* Fixed: Removed massive padding and vh gaps to pull the page completely up */
.main .block-container { padding: 0px !important; max-width: 100% !important; margin: 0 !important; }
[data-testid="stSidebar"], header, footer { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; height: 0px !important; display: none !important; }

/* ── NAV ARCHITECTURE ── */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 60px;
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border);
    position: relative;
    z-index: 100;
}
.nav-brand {
    font-family: var(--ff-sans);
    font-weight: 600;
    font-size: 19px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-main);
}
.nav-brand-icon { color: var(--rose); font-size: 22px; line-height: 1; }
.nav-links {
    display: flex;
    gap: 40px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-muted);
}
.nav-links span:hover { color: var(--text-main); cursor: pointer; }
.nav-actions { display: flex; gap: 20px; align-items: center; font-size: 14px; font-weight: 500; }
.btn-solid { background: var(--text-main); color: white !important; padding: 10px 20px; border-radius: 30px; }

/* ── LANDING STYLING MATRIX ── */
.hero-container {
    padding: 100px 20px 140px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
}
.hero-title {
    font-family: var(--ff-display);
    font-size: 92px;
    font-weight: 300;
    line-height: 1.08;
    color: var(--text-main);
    margin-bottom: 24px;
    max-width: 900px;
    letter-spacing: -2px;
}
.hero-title i { font-style: italic; color: #1E293B; font-weight: 400; }
.hero-subtitle {
    font-family: var(--ff-sans);
    font-size: 18px;
    color: var(--text-muted);
    max-width: 580px;
    line-height: 1.65;
    margin-bottom: 44px;
}
.bg-canvas {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 35%, #E2E8F0 0%, #EBF1FA 25%, #F8FAFC 65%);
    z-index: -1;
}

/* ── FORM CONTAINER CONTROL ── */
.form-screen {
    padding: 80px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.input-card {
    background: var(--bg-surface);
    padding: 44px;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    width: 100%;
    max-width: 520px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.02);
}
.input-card h2 { font-family: var(--ff-display); font-size: 36px; font-style: italic; margin-bottom: 12px; color: var(--text-main); }
.input-card p { color: var(--text-muted); font-size: 14px; margin-bottom: 0; }

/* ── NEW ATTRACTIVE RESULTS CONTAINER ── */
.results-container { 
    padding: 40px 60px 80px; 
    background: var(--bg-base); 
}
.ctx-bar {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    display: flex; 
    align-items: center; 
    justify-content: space-between;
    margin-bottom: 30px;
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.ctx-repo { font-family: var(--ff-mono); font-weight: 600; color: var(--text-main); font-size: 17px; letter-spacing: -0.3px;}
.ctx-pr { font-size: 12px; color: var(--text-light); margin-top: 4px; font-family: var(--ff-mono); }

.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 30px; }
.tile {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 24px;
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.tile-label { font-family: var(--ff-mono); font-size: 11px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 1px; margin-bottom: 10px; }
.tile-val { font-family: var(--ff-display); font-size: 46px; font-style: italic; line-height: 1; color: var(--text-main); }
.tv-score { color: var(--blue); }
.tv-bugs { color: var(--green); }
.tv-perf { color: var(--amber); }
.tv-sec { color: var(--rose); }

.summary-box {
    background: var(--bg-surface); 
    border: 1px solid var(--border); 
    padding: 28px; 
    border-radius: var(--radius-md); 
    margin-bottom: 34px;
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.summary-box h4 { margin: 0 0 12px; font-family: var(--ff-display); font-size: 22px; font-style: italic; color: var(--text-main); }
.summary-box p { color: var(--text-muted); font-size: 15px; margin: 0; line-height: 1.65; }

/* Structured Column Layouts */
.findings-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 24px;
    min-height: 380px;
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.findings-card h4 { font-family: var(--ff-display); font-style: italic; font-size: 22px; margin-bottom: 20px; color: var(--text-main); border-bottom: 1px solid var(--border); padding-bottom: 10px;}

.finding {
    background: var(--bg-base); 
    border: 1px solid var(--border);
    border-radius: 8px; 
    padding: 16px; 
    margin-bottom: 12px;
    display: flex; 
    gap: 14px; 
    align-items: flex-start; 
}
.f-icon { width: 34px; height: 34px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0;}
.fi-bug  { background: var(--green-dim); color: var(--green); }
.fi-perf { background: var(--amber-dim); color: var(--amber); }
.fi-sec  { background: var(--rose-dim); color: var(--rose); }
.f-desc { font-size: 13.5px; color: var(--text-muted); line-height: 1.6; }
.f-desc code { font-family: var(--ff-mono); background: var(--bg-surface); color: var(--text-main); padding: 2px 6px; border-radius: 4px; font-size: 12px; word-break: break-word; white-space: normal;}
.f-empty { background: transparent; border: 1px dashed var(--border); padding: 32px; text-align: center; border-radius: 8px; color: var(--text-light); font-family: var(--ff-mono); font-size: 12px;}

.score-card {
    background: var(--bg-surface); 
    border: 1px solid var(--border);
    border-radius: var(--radius-md); 
    padding: 44px 20px;
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.score-ring {
    width: 140px; height: 140px; border-radius: 50%;
    background: conic-gradient(var(--blue) calc(var(--pct) * 1%), var(--border) 0%);
    display: flex; align-items: center; justify-content: center; margin-bottom: 22px;
}
.score-inner { width: 112px; height: 112px; border-radius: 50%; background: var(--bg-surface); display: flex; align-items: center; justify-content: center; }
.score-num { font-family: var(--ff-display); font-size: 56px; font-style: italic; color: var(--text-main); line-height: 1; }
.score-verdict { font-family: var(--ff-mono); font-size: 11px; text-transform: uppercase; padding: 6px 16px; border-radius: 20px; font-weight: 600; letter-spacing: 1px; }
.sv-excellent { background: var(--green-dim);  color: var(--green); }
.sv-good      { background: var(--blue-dim);   color: var(--blue); }
.sv-average   { background: var(--amber-dim);  color: var(--amber); }
.sv-poor      { background: var(--rose-dim);   color: var(--rose); }

/* Buttons and Form inputs overrides */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    padding: 12px 28px !important;
    border-radius: 6px !important;
    font-family: var(--ff-sans) !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
