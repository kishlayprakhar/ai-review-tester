import streamlit as st
import requests
from datetime import datetime
import time

# ══════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="CodeSentry — Instant AI Reviews",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar for a true website feel
)

# ══════════════════════════════════════════════════════
# SESSION STATE ROUTING
# ══════════════════════════════════════════════════════
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'repo' not in st.session_state:
    st.session_state.repo = 'scikit-learn/scikit-learn'
if 'pr' not in st.session_state:
    st.session_state.pr = 2600

def go_to_input():
    st.session_state.page = 'input'

def go_to_results(repo_url, pr_num):
    st.session_state.repo = repo_url
    st.session_state.pr = pr_num
    st.session_state.page = 'results'

def go_to_landing():
    st.session_state.page = 'landing'

# ══════════════════════════════════════════════════════
# CSS — MODERN LIGHT THEME (Inspired by Image 1)
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400;1,9..144,500&family=Inter:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg-base:       #F7F8FA;
    --bg-surface:    #FFFFFF;
    --bg-raised:     #FFFFFF;
    --border:        #E2E8F0;
    --border-hover:  #CBD5E1;
    
    --text-main:     #0F172A;
    --text-muted:    #64748B;
    --text-light:    #94A3B8;
    
    --accent:        #1E293B;
    --accent-hover:  #334155;
    
    --blue:          #3B82F6;
    --blue-dim:      rgba(59, 130, 246, 0.1);
    --green:         #10B981;
    --green-dim:     rgba(16, 185, 129, 0.1);
    --amber:         #F59E0B;
    --amber-dim:     rgba(245, 158, 11, 0.1);
    --rose:          #F43F5E;
    --rose-dim:      rgba(244, 63, 94, 0.1);

    --ff-display:    'Fraunces', serif;
    --ff-sans:       'Inter', sans-serif;
    --ff-mono:       'Fira Code', monospace;
    
    --radius-md:     12px;
    --radius-lg:     24px;
    --shadow:        0 10px 40px -10px rgba(0,0,0,0.08);
}

/* Base resets */
html, body, [data-testid="stAppViewContainer"], .main .block-container {
    background-color: var(--bg-base) !important;
    color: var(--text-main) !important;
    font-family: var(--ff-sans) !important;
}
.main .block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"], header, footer { display: none !important; }

/* ── CUSTOM NAVBAR ── */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 60px;
    background: transparent;
    position: absolute;
    top: 0; left: 0; right: 0;
    z-index: 100;
}
.nav-brand {
    font-family: var(--ff-sans);
    font-weight: 600;
    font-size: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.nav-brand-icon { color: var(--rose); font-size: 20px; }
.nav-links {
    display: flex;
    gap: 40px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-muted);
}
.nav-links span:hover { color: var(--text-main); cursor: pointer; }
.nav-actions { display: flex; gap: 16px; align-items: center; font-size: 14px; font-weight: 500; }
.btn-outline { border: 1px solid var(--border); padding: 8px 16px; border-radius: 8px; }
.btn-solid { background: var(--text-main); color: white; padding: 8px 16px; border-radius: 8px; }

/* ── LANDING PAGE HERO ── */
.hero-wrapper {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: radial-gradient(circle at 50% 40%, #E8E5DE 0%, #D8E4DF 30%, #F7F8FA 70%);
    padding: 0 20px;
}
.hero-title {
    font-family: var(--ff-display);
    font-size: 90px;
    font-weight: 300;
    line-height: 1.1;
    color: var(--text-main);
    margin-bottom: 24px;
    max-width: 900px;
}
.hero-title i { font-style: italic; color: #FFFFFF; text-shadow: 0 4px 20px rgba(0,0,0,0.15); }
.hero-subtitle {
    font-family: var(--ff-sans);
    font-size: 18px;
    color: var(--text-muted);
    max-width: 600px;
    line-height: 1.6;
    margin-bottom: 40px;
}
.hero-sphere {
    position: absolute;
    width: 600px; height: 600px;
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.8), rgba(150,160,170,0.2));
    border-radius: 50%;
    z-index: 0;
    box-shadow: inset -20px -20px 60px rgba(0,0,0,0.05), 0 30px 60px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
}
.hero-content { z-index: 10; position: relative; display: flex; flex-direction: column; align-items: center;}

/* ── INPUT PAGE ── */
.input-page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--bg-base);
}
.input-card {
    background: var(--bg-surface);
    padding: 50px;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    width: 100%;
    max-width: 500px;
    text-align: center;
}
.input-card h2 { font-family: var(--ff-display); font-size: 32px; font-style: italic; margin-bottom: 10px;}
.input-card p { color: var(--text-muted); margin-bottom: 30px; }

/* ── RESULTS DASHBOARD ── */
.results-page { padding: 100px 60px 60px; background: var(--bg-base); min-height: 100vh; }
.ctx-bar {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 24px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
}
.ctx-repo { font-family: var(--ff-mono); font-weight: 600; color: var(--text-main); font-size: 16px;}
.ctx-pr { font-size: 13px; color: var(--text-muted); margin-top: 4px; }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 30px; }
.tile {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
}
.tile-label { font-family: var(--ff-mono); font-size: 11px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 12px; }
.tile-val { font-family: var(--ff-display); font-size: 42px; font-style: italic; line-height: 1; color: var(--text-main); }
.tv-score { color: var(--blue); }
.tv-bugs { color: var(--green); }
.tv-perf { color: var(--amber); }
.tv-sec { color: var(--rose); }

.finding {
    background: var(--bg-surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 16px; margin-bottom: 12px;
    display: flex; gap: 16px; align-items: flex-start;
}
.f-icon { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0;}
.fi-bug  { background: var(--green-dim); }
.fi-perf { background: var(--amber-dim); }
.fi-sec  { background: var(--rose-dim); }
.f-desc { font-size: 14px; color: var(--text-muted); line-height: 1.6; }
.f-desc code { font-family: var(--ff-mono); background: var(--border); color: var(--text-main); padding: 2px 6px; border-radius: 4px; font-size: 12px;}
.f-empty { background: transparent; border: 1px dashed var(--border); padding: 30px; text-align: center; border-radius: var(--radius-md); color: var(--text-light); font-family: var(--ff-mono); font-size: 12px;}

.score-card {
    background: var(--bg-surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 40px 20px;
    display: flex; flex-direction: column; align-items: center;
}
.score-ring {
    width: 140px; height: 140px; border-radius: 50%;
    background: conic-gradient(var(--blue) calc(var(--pct) * 1%), var(--border) 0%);
    display: flex; align-items: center; justify-content: center; margin-bottom: 20px;
}
.score-inner { width: 110px; height: 110px; border-radius: 50%; background: var(--bg-surface); display: flex; align-items: center; justify-content: center; }
.score-num { font-family: var(--ff-display); font-size: 56px; font-style: italic; color: var(--text-main); }
.score-verdict { font-family: var(--ff-mono); font-size: 11px; text-transform: uppercase; padding: 6px 16px; border-radius: 20px; font-weight: 600; }
.sv-excellent { background: var(--green-dim);  color: var(--green); }
.sv-good      { background: var(--blue-dim);   color: var(--blue); }
.sv-average   { background: var(--amber-dim);  color: var(--amber); }
.sv-poor      { background: var(--rose-dim);   color: var(--rose); }

/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    padding: 14px 32px !important;
    border-radius: 30px !important;
    font-family: var(--ff-sans) !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { background: var(--accent-hover) !important; transform: translateY(-2px) !important; box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;}
.stTextInput input, .stNumberInput input {
    background: var(--bg-base) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    font-family: var(--ff-mono) !important;
    color: var(--text-main) !important;
}
.stTextInput input:focus, .stNumberInput input:focus { border-color: var(--blue) !important; box-shadow: 0 0 0 3px var(--blue-dim) !important;}
div[data-testid="stSpinner"] p { font-family: var(--ff-mono); color: var(--text-muted); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# API CONFIG & HELPERS
# ══════════════════════════════════════════════════════
API_URL = "https://ai-reviewer-backend-sz5k.onrender.com" # Using your live URL

def get_review(repo, pr_num):
    try:
        r = requests.post(f"{API_URL}/review", json={"repo": repo, "pr_number": int(pr_num)}, timeout=60)
        return (r.json(), None) if r.status_code == 200 else (None, f"Error {r.status_code}: {r.text}")
    except requests.exceptions.ConnectionError:
        return (None, "conn")
    except Exception as e:
        return (None, str(e))

def score_info(s):
    if s >= 9: return "EXCELLENT", "sv-excellent"
    if s >= 7: return "GOOD",      "sv-good"
    if s >= 5: return "AVERAGE",   "sv-average"
    return            "NEEDS WORK", "sv-poor"

def findings_html(icon, cls, items, kind):
    if not items: return f'<div class="f-empty">No {kind}s detected in this pull request.</div>'
    out = ""
    for it in items:
        desc = it.get("description", "") if isinstance(it, dict) else str(it)
        out += f"""<div class="finding"><div class="f-icon {cls}">{icon}</div>
                   <div class="f-desc">{desc}</div></div>"""
    return out


# ══════════════════════════════════════════════════════
# COMMON NAVBAR COMPONENT
# ══════════════════════════════════════════════════════
def render_navbar():
    st.markdown("""
        <div class="navbar">
            <div class="nav-brand"><span class="nav-brand-icon">◈</span> CodeSentry</div>
            <div class="nav-links">
                <span>Features</span>
                <span>How it Works</span>
                <span>Pricing</span>
                <span>Changelog</span>
            </div>
            <div class="nav-actions">
                <span style="cursor:pointer;">Log in</span>
                <span class="btn-solid" style="cursor:pointer;">Sign up free</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# PAGE 1: LANDING PAGE
# ══════════════════════════════════════════════════════
if st.session_state.page == 'landing':
    render_navbar()
    st.markdown("""
        <div class="hero-wrapper">
            <div class="hero-sphere"></div>
            <div class="hero-content">
                <div class="hero-title">Your code, reviewed.<br><i>Instantly.</i></div>
                <div class="hero-subtitle">
                    AI-powered pull request analysis that catches bugs, security holes, 
                    and performance issues before they reach production.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # We place the button perfectly centered using columns over the background
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='margin-top: -280px; text-align: center; position: relative; z-index: 20;'>", unsafe_allow_html=True)
        if st.button("Connect GitHub Free", use_container_width=True):
            go_to_input()
            st.rerun()
        st.markdown("<p style='font-size:12px; color:#64748B; margin-top:10px;'>No credit card required · Setup in 60 seconds</p></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# PAGE 2: INPUT FORM
# ══════════════════════════════════════════════════════
elif st.session_state.page == 'input':
    render_navbar()
    st.markdown('<div class="input-page">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="input-card">
                <h2>New Analysis</h2>
                <p>Target a repository and PR to begin your automated review.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Pulling the form slightly up so it overlays the CSS card nicely
        st.markdown("<div style='margin-top: -150px; padding: 0 40px; position:relative; z-index:10;'>", unsafe_allow_html=True)
        repo = st.text_input("Repository path", value="scikit-learn/scikit-learn")
        pr = st.number_input("Pull Request Number", min_value=1, step=1, value=2600)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run AI Analysis", use_container_width=True):
            go_to_results(repo, pr)
            st.rerun()
            
        if st.button("← Back to Home", type="secondary", use_container_width=True):
            go_to_landing()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# PAGE 3: RESULTS DASHBOARD
# ══════════════════════════════════════════════════════
elif st.session_state.page == 'results':
    st.markdown('<div class="results-page">', unsafe_allow_html=True)
    
    if st.button("← Back to Search"):
        go_to_input()
        st.rerun()
        
    st.markdown(f"""
        <div class="ctx-bar">
            <div>
                <div class="ctx-repo">{st.session_state.repo} / pull / {st.session_state.pr}</div>
                <div class="ctx-pr">PR #{st.session_state.pr} · Automated AI Review</div>
            </div>
            <a href="https://github.com/{st.session_state.repo}/pull/{st.session_state.pr}" 
               target="_blank" style="text-decoration:none; background:#F1F5F9; color:#0F172A; padding:8px 16px; border-radius:8px; font-weight:500; font-size:13px; border:1px solid #E2E8F0;">
               View on GitHub ↗
            </a>
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Analyzing Pull Request..."):
        result, err = get_review(st.session_state.repo, st.session_state.pr)

    if err == "conn":
        st.error("Backend offline. Please start the FastAPI server.")
    elif err:
        st.error(f"Error: {err}")
    else:
        review = result.get("review", {})
        bugs   = review.get("bugs", [])
        imps   = review.get("improvements", [])
        secs   = review.get("security_issues", [])
        score  = int(review.get("quality_score", 0))
        summ   = review.get("summary", "")
        sv_t, sv_c = score_info(score)
        pct = score * 10

        st.markdown(f"""
            <div class="tiles">
                <div class="tile">
                    <div class="tile-label">Quality Score</div>
                    <div class="tile-val tv-score">{score}</div>
                </div>
                <div class="tile">
                    <div class="tile-label">Bugs Found</div>
                    <div class="tile-val tv-bugs">{len(bugs)}</div>
                </div>
                <div class="tile">
                    <div class="tile-label">Improvements</div>
                    <div class="tile-val tv-perf">{len(imps)}</div>
                </div>
                <div class="tile">
                    <div class="tile-label">Security</div>
                    <div class="tile-val tv-sec">{len(secs)}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='background:#FFFFFF; border:1px solid #E2E8F0; padding:24px; border-radius:12px; margin-bottom:30px;'><h4 style='margin:0 0 10px; font-family:Fraunces;'>AI Summary</h4><p style='color:#64748B; font-size:15px; margin:0;'>{summ}</p></div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([3, 3, 3, 2.5])
        with c1:
            st.markdown("<h4 style='font-family:Fraunces; margin-bottom:15px;'>Bugs</h4>", unsafe_allow_html=True)
            st.markdown(findings_html("🪲", "fi-bug", bugs, "bug"), unsafe_allow_html=True)
        with c2:
            st.markdown("<h4 style='font-family:Fraunces; margin-bottom:15px;'>Performance</h4>", unsafe_allow_html=True)
            st.markdown(findings_html("⚡", "fi-perf", imps, "suggestion"), unsafe_allow_html=True)
        with c3:
            st.markdown("<h4 style='font-family:Fraunces; margin-bottom:15px;'>Security</h4>", unsafe_allow_html=True)
            st.markdown(findings_html("🔒", "fi-sec", secs, "security issue"), unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
                <div class="score-card" style="--pct:{pct};">
                    <div class="score-ring">
                        <div class="score-inner">
                            <div class="score-num">{score}</div>
                        </div>
                    </div>
                    <div style="font-family:'Fira Code'; font-size:12px; color:#64748B; margin-bottom:10px;">/ 10 QUALITY SCORE</div>
                    <div class="score-verdict {sv_c}">{sv_t}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
