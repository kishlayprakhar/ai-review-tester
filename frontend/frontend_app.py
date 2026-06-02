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
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght=0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400;1,9..144,500&family=Inter:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap');

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
    overflow-y: auto; /* Allow scrolling ONLY if absolutely forced by ultra-low resolution screens */
}
.main .block-container { padding: 10px 0px 0px 0px !important; max-width: 100% !important; margin: 0 !important; }
[data-testid="stSidebar"], footer { display: none !important; }
[data-testid="stHeader"], header { display: none !important; height: 0px !important; padding: 0 !important; }

/* Custom Scrollbar styling for a cleaner look */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

/* ── NAV ARCHITECTURE ── */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 60px; /* Reduced padding */
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
.btn-solid { background: var(--text-main); color: white !important; padding: 8px 18px; border-radius: 30px; }

/* ── HERO BACKGROUND CONTAINER ── */
.hero-container {
    padding: 60px 20px 40px 20px; /* Reduced vertical gaps */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    z-index: 10;
    background: radial-gradient(circle at 50% 45%, #E2E8F0 0%, #EBF1FA 20%, #F8FAFC 55%) !important;
}
.hero-title {
    font-family: var(--ff-display);
    font-size: 80px; /* Slightly tighter font size to prevent view pushing */
    font-weight: 300;
    line-height: 1.08;
    color: var(--text-main) !important;
    margin-bottom: 20px;
    max-width: 900px;
    letter-spacing: -2px;
}
.hero-title i { font-style: italic; color: #334155 !important; font-weight: 400; }
.hero-subtitle {
    font-family: var(--ff-sans);
    font-size: 17px;
    color: var(--text-muted) !important;
    max-width: 540px;
    line-height: 1.6;
    margin-bottom: 20px;
}

/* ── FORM CONTAINER CONTROL ── */
.form-screen {
    padding: 40px 20px; /* Tighter padding */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.input-card {
    background: var(--bg-surface);
    padding: 34px 44px;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    width: 100%;
    max-width: 520px;
    text-align: center;
    margin-bottom: 16px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.02);
}
.input-card h2 { font-family: var(--ff-display); font-size: 34px; font-style: italic; margin-bottom: 8px; color: var(--text-main); }
.input-card p { color: var(--text-muted); font-size: 13.5px; margin-bottom: 0; }

/* ── RESULTS CONTAINER ── */
.results-container { 
    padding: 15px 40px 40px; /* Reduced inner margins */
}
.ctx-bar {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 20px; /* Compact padding */
    display: flex; 
    align-items: center; 
    justify-content: space-between;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.ctx-repo { font-family: var(--ff-mono); font-weight: 600; color: var(--text-main); font-size: 16px; letter-spacing: -0.3px;}
.ctx-pr { font-size: 11.5px; color: var(--text-light); margin-top: 2px; font-family: var(--ff-mono); }

.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }
.tile {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 20px; /* Tighter tiles */
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.tile-label { font-family: var(--ff-mono); font-size: 10px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 1px; margin-bottom: 6px; }
.tile-val { font-family: var(--ff-display); font-size: 38px; font-style: italic; line-height: 1; color: var(--text-main); }
.tv-score { color: var(--blue); }
.tv-bugs { color: var(--green); }
.tv-perf { color: var(--amber); }
.tv-sec { color: var(--rose); }

.summary-box {
    background: var(--bg-surface); 
    border: 1px solid var(--border); 
    padding: 18px 24px; 
    border-radius: var(--radius-md); 
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.summary-box h4 { margin: 0 0 6px; font-family: var(--ff-display); font-size: 19px; font-style: italic; color: var(--text-main); }
.summary-box p { color: var(--text-muted); font-size: 14px; margin: 0; line-height: 1.55; }

/* ── ⚡ FIXED HEIGHT SCROLLABLE CARD MATRIX ── */
.findings-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px;
    height: 310px; /* ⚡ Set a strict fixed height constraint */
    overflow-y: auto; /* ⚡ Turn on independent vertical scrolling inside the box */
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.findings-card h4 { 
    font-family: var(--ff-display); 
    font-style: italic; 
    font-size: 20px; 
    margin: 0 0 14px 0; 
    color: var(--text-main); 
    border-bottom: 1px solid var(--border); 
    padding-bottom: 8px;
    position: sticky; /* Keep headers static at top of scrolling area */
    top: 0;
    background: var(--bg-surface);
    z-index: 5;
}

.finding {
    background: var(--bg-base); 
    border: 1px solid var(--border);
    border-radius: 8px; 
    padding: 12px; 
    margin-bottom: 8px;
    display: flex; 
    gap: 12px; 
    align-items: flex-start; 
}
.f-icon { width: 30px; height: 30px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;}
.fi-bug  { background: var(--green-dim); color: var(--green); }
.fi-perf { background: var(--amber-dim); color: var(--amber); }
.fi-sec  { background: var(--rose-dim); color: var(--rose); }
.f-desc { font-size: 13px; color: var(--text-muted); line-height: 1.5; }
.f-desc code { font-family: var(--ff-mono); background: var(--bg-surface); color: var(--text-main); padding: 2px 6px; border-radius: 4px; font-size: 11.5px; word-break: break-word; white-space: normal;}
.f-empty { background: transparent; border: 1px dashed var(--border); padding: 24px; text-align: center; border-radius: 8px; color: var(--text-light); font-family: var(--ff-mono); font-size: 11.5px;}

.score-card {
    background: var(--bg-surface); 
    border: 1px solid var(--border);
    border-radius: var(--radius-md); 
    padding: 30px 20px;
    height: 310px; /* Match the findings card height */
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    justify-content: center;
    box-shadow: 0 4px 12px rgba(15,23,42,0.01);
}
.score-ring {
    width: 120px; height: 120px; border-radius: 50%;
    background: conic-gradient(var(--blue) calc(var(--pct) * 1%), var(--border) 0%);
    display: flex; align-items: center; justify-content: center; margin-bottom: 16px;
}
.score-inner { width: 96px; height: 96px; border-radius: 50%; background: var(--bg-surface); display: flex; align-items: center; justify-content: center; }
.score-num { font-family: var(--ff-display); font-size: 48px; font-style: italic; color: var(--text-main); line-height: 1; }
.score-verdict { font-family: var(--ff-mono); font-size: 10px; text-transform: uppercase; padding: 4px 12px; border-radius: 20px; font-weight: 600; letter-spacing: 1px; }
.sv-excellent { background: var(--green-dim);  color: var(--green); }
.sv-good      { background: var(--blue-dim);   color: var(--blue); }
.sv-average   { background: var(--amber-dim);  color: var(--amber); }
.sv-poor      { background: var(--rose-dim);   color: var(--rose); }

/* Buttons and Form inputs overrides */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    padding: 10px 28px !important;
    border-radius: 30px !important;
    font-family: var(--ff-sans) !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover { background: var(--accent-hover) !important; transform: translateY(-1px) !important; box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important; }
.stTextInput input, .stNumberInput input {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    font-family: var(--ff-mono) !important;
    color: var(--text-main) !important;
    font-size: 13px !important;
}
</style>
""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════
# NETWORK RUNTIME WRAPPERS
# ══════════════════════════════════════════════════════
API_URL = "https://ai-reviewer-backend-sz5k.onrender.com"

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
    if not items: return f'<div class="f-empty">◈ &nbsp; No {kind}s detected in this pull request.</div>'
    out = ""
    for it in items:
        desc = it.get("description", "") if isinstance(it, dict) else str(it)
        out += f"""<div class="finding"><div class="f-icon {cls}">{icon}</div>
                   <div class="f-desc">{desc}</div></div>"""
    return out

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
# MULTI-PAGE CONTROLLER ROUTING LOGIC
# ══════════════════════════════════════════════════════

# PAGE 1: REFINED LANDING
if st.session_state.page == 'landing':
    st.markdown('<div class="bg-canvas"></div>', unsafe_allow_html=True)
    render_navbar()
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Your code, reviewed.<br><i>Instantly.</i></div>
            <div class="hero-subtitle">
                AI-powered pull request analysis that catches bugs, security holes, 
                and performance issues before they reach production.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1.2, 1, 1.2])
    with c2:
        if st.button("Connect GitHub Free", use_container_width=True):
            go_to_input()
            st.rerun()
        st.markdown("<p style='font-size:12px; text-align:center; color:#64748B; margin-top:14px;'>No credit card required · Setup in 60 seconds</p>", unsafe_allow_html=True)

# PAGE 2: INPUT SCREEN
elif st.session_state.page == 'input':
    render_navbar()
    st.markdown('<div class="form-screen">', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        st.markdown("""
            <div class="input-card">
                <h2>New Analysis</h2>
                <p>Target an active repository and PR reference index to begin your automated code review sequence.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='padding: 0 16px;'>", unsafe_allow_html=True)
        repo = st.text_input("Repository path (e.g., scikit-learn/scikit-learn)", placeholder="username/repository-name")
        pr = st.number_input("Pull Request Number", min_value=1, step=1, value=1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run AI Analysis", use_container_width=True):
            if not repo.strip():
                st.warning("⚠️ Please provide a valid repository target layout.")
            else:
                go_to_results(repo, pr)
                st.rerun()
            
        if st.button("← Back to Home", type="secondary", use_container_width=True):
            go_to_landing()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# PAGE 3: HIGH-END RESULTS INTERFACE (FIXED TOP GAP & CONVERTED SEARCH BUTTON TEXT TO BACK)
elif st.session_state.page == 'results':
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    c_back, _ = st.columns([1.5, 8.5])
    with c_back:
        # Fixed: Text changed from "← Search" to "← Back"
        if st.button("← Back", use_container_width=True):
            go_to_input()
            st.rerun()
        
    st.markdown(f"""
        <div class="ctx-bar">
            <div>
                <div class="ctx-repo">{st.session_state.repo} / pull / {st.session_state.pr}</div>
                <div class="ctx-pr">PR #{st.session_state.pr} · Automated AI Review</div>
            </div>
            <a href="https://github.com/{st.session_state.repo}/pull/{st.session_state.pr}" 
               target="_blank" style="text-decoration:none; background:#0F172A; color:#FFFFFF; padding:10px 18px; border-radius:6px; font-weight:500; font-size:13px;">
               View on GitHub ↗
            </a>
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Analyzing Pull Request Matrix..."):
        result, err = get_review(st.session_state.repo, st.session_state.pr)

    if err == "conn":
        st.error("🔌 Backend offline. Please ensure your FastAPI engine parameters are executed safely.")
    elif err:
        st.error(f"❌ {err}")
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
                    <div class="tile-val tv-score">{score}<span style='font-size:16px;color:var(--text-light);font-family:var(--ff-sans);font-style:normal;'> /10</span></div>
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
            
            <div class="summary-box">
                <h4>AI Summary</h4>
                <p>{summ}</p>
            </div>
        """, unsafe_allow_html=True)

        # Columns Layout
        c1, c2, c3, c4 = st.columns([3, 3, 3, 2.5])
        with c1:
            st.markdown('<div class="findings-card"><h4>Bugs</h4>', unsafe_allow_html=True)
            st.markdown(findings_html("🪲", "fi-bug", bugs, "bug"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="findings-card"><h4>Performance</h4>', unsafe_allow_html=True)
            st.markdown(findings_html("⚡", "fi-perf", imps, "suggestion"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="findings-card"><h4>Security</h4>', unsafe_allow_html=True)
            st.markdown(findings_html("🔒", "fi-sec", secs, "security issue"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
                <div class="score-card" style="--pct:{pct};">
                    <div class="score-ring">
                        <div class="score-inner">
                            <div class="score-num">{score}</div>
                        </div>
                    </div>
                    <div style="font-family:'Fira Code'; font-size:11px; color:var(--text-light); margin-bottom:12px; letter-spacing:0.5px;">QUALITY METRIC</div>
                    <div class="score-verdict {sv_c}">{sv_t}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
