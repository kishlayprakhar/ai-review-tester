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
    --bg-base:       #F7F8FA;
    --bg-surface:    #FFFFFF;
    --bg-raised:     #FFFFFF;
    --border:        #E2E8F0;
    --border-hover:  #CBD5E1;
    
    --text-main:     #0F172A;
    --text-muted:    #475569;
    --text-light:    #94A3B8;
    
    --accent:        #1E293B;
    --accent-hover:  #334155;
    
    --blue:          #3B82F6;
    --blue-dim:      rgba(59, 130, 246, 0.08);
    --green:         #10B981;
    --green-dim:     rgba(16, 185, 129, 0.08);
    --amber:         #D97706;
    --amber-dim:     rgba(217, 119, 6, 0.08);
    --rose:          #E11D48;
    --rose-dim:      rgba(225, 29, 72, 0.08);

    --ff-display:    'Fraunces', serif;
    --ff-sans:       'Inter', sans-serif;
    --ff-mono:       'Fira Code', monospace;
    
    --radius-md:     12px;
    --radius-lg:     24px;
    --shadow:        0 10px 40px -10px rgba(0,0,0,0.05);
}

/* Framework Clean Up Overrides */
html, body, [data-testid="stAppViewContainer"], .main .block-container {
    background-color: var(--bg-base) !important;
    color: var(--text-main) !important;
    font-family: var(--ff-sans) !important;
}
.main .block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"], header, footer { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }

/* ── NAV ARCHITECTURE ── */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 60px;
    background: transparent;
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
.nav-links span { transition: color 0.15s ease; }
.nav-links span:hover { color: var(--text-main); cursor: pointer; }
.nav-actions { display: flex; gap: 20px; align-items: center; font-size: 14px; font-weight: 500; }
.btn-solid { background: var(--text-main); color: white !important; padding: 10px 20px; border-radius: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }

/* ── LANDING STYLING MATRIX ── */
.hero-container {
    padding-top: 40px;
    padding-bottom: 80px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: transparent;
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
/* Fixed Text Visibility: "Instantly" is now a sharp dark tone */
.hero-title i { font-style: italic; color: #2A364F; font-weight: 400; }
.hero-subtitle {
    font-family: var(--ff-sans);
    font-size: 18px;
    color: var(--text-muted);
    max-width: 58px;
    line-width: 100%;
    max-width: 580px;
    line-height: 1.65;
    margin-bottom: 44px;
}
.bg-canvas {
    position: absolute;
    top: -120px; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at 50% 35%, #E5E9E7 0%, #DFE4E8 25%, #F7F8FA 65%);
    z-index: -1;
}

/* ── FORM CONTAINER CONTROL ── */
.form-screen {
    padding: 60px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.input-card {
    background: var(--bg-surface);
    padding: 44px;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    width: 100%;
    max-width: 520px;
    text-align: center;
    margin-bottom: 24px;
}
.input-card h2 { font-family: var(--ff-display); font-size: 36px; font-style: italic; margin-bottom: 12px; color: var(--text-main); }
.input-card p { color: var(--text-muted); font-size: 14px; margin-bottom: 0; }

/* ── ANALYSIS OUTPUT LAYOUT ── */
.results-container { padding: 40px 60px 80px; background: var(--bg-base); }
.ctx-bar {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px 24px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 30px;
    box-shadow: var(--shadow);
}
.ctx-repo { font-family: var(--ff-mono); font-weight: 600; color: var(--text-main); font-size: 16px; letter-spacing: -0.3px;}
.ctx-pr { font-size: 12px; color: var(--text-light); margin-top: 4px; font-family: var(--ff-mono); }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 30px; }
.tile {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 22px;
    box-shadow: var(--shadow);
}
.tile-label { font-family: var(--ff-mono); font-size: 10px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 1px; margin-bottom: 12px; }
.tile-val { font-family: var(--ff-display); font-size: 44px; font-style: italic; line-height: 1; color: var(--text-main); }
.tv-score { color: var(--blue); }
.tv-bugs { color: var(--green); }
.tv-perf { color: var(--amber); }
.tv-sec { color: var(--rose); }

.finding {
    background: var(--bg-surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 16px; margin-bottom: 12px;
    display: flex; gap: 14px; align-items: flex-start; box-shadow: 0 2px 8px rgba(0,0,0,0.01);
}
.f-icon { width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0;}
.fi-bug  { background: var(--green-dim); }
.fi-perf { background: var(--amber-dim); }
.fi-sec  { background: var(--rose-dim); }
.f-desc { font-size: 13.5px; color: var(--text-muted); line-height: 1.6; font-weight: 400; }
.f-desc code { font-family: var(--ff-mono); background: var(--bg-base); color: var(--text-main); padding: 2px 6px; border-radius: 4px; font-size: 12px; word-break: break-all; white-space: normal;}
.f-empty { background: transparent; border: 1px dashed var(--border); padding: 32px; text-align: center; border-radius: var(--radius-md); color: var(--text-light); font-family: var(--ff-mono); font-size: 12px;}

.score-card {
    background: var(--bg-surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 44px 20px;
    display: flex; flex-direction: column; align-items: center; box-shadow: var(--shadow);
}
.score-ring {
    width: 130px; height: 130px; border-radius: 50%;
    background: conic-gradient(var(--blue) calc(var(--pct) * 1%), var(--border) 0%);
    display: flex; align-items: center; justify-content: center; margin-bottom: 20px;
}
.score-inner { width: 104px; height: 104px; border-radius: 50%; background: var(--bg-surface); display: flex; align-items: center; justify-content: center; }
.score-num { font-family: var(--ff-display); font-size: 52px; font-style: italic; color: var(--text-main); line-height: 1; }
.score-verdict { font-family: var(--ff-mono); font-size: 10px; text-transform: uppercase; padding: 5px 14px; border-radius: 20px; font-weight: 600; letter-spacing: 1px; }
.sv-excellent { background: var(--green-dim);  color: var(--green); border: 1px solid rgba(16,185,129,0.2); }
.sv-good      { background: var(--blue-dim);   color: var(--blue); border: 1px solid rgba(59,130,246,0.2); }
.sv-average   { background: var(--amber-dim);  color: var(--amber); border: 1px solid rgba(217,119,6,0.2); }
.sv-poor      { background: var(--rose-dim);   color: var(--rose); border: 1px solid rgba(225,29,72,0.2); }

/* ── FORM CONTROL LAYOUT ALIGNMENTS ── */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    padding: 12px 30px !important;
    border-radius: 8px !important;
    font-family: var(--ff-sans) !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover { background: var(--accent-hover) !important; transform: translateY(-1px) !important; box-shadow: 0 8px 24px rgba(0,0,0,0.08) !important;}
.stTextInput input, .stNumberInput input {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 10px 14px !important;
    font-family: var(--ff-mono) !important;
    color: var(--text-main) !important;
    font-size: 13px !important;
}
.stTextInput input:focus, .stNumberInput input:focus { border-color: var(--blue) !important; box-shadow: 0 0 0 3px var(--blue-dim) !important;}
div[data-testid="stSpinner"] p { font-family: var(--ff-mono); color: var(--text-muted); font-size: 13px; }
.stAlert { background: var(--bg-surface) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; color: var(--text-main) !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# NETWORK WRAPPERS
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
                   <div class="f-body"><div class="f-desc">{desc}</div></div></div>"""
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
# ROUTER — VIEW CONTROLLER ARCHITECTURE
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
        st.markdown("<div style='margin-top: -30px; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Connect GitHub Free", use_container_width=True):
            go_to_input()
            st.rerun()
        st.markdown("<p style='font-size:12px; color:#64748B; margin-top:14px;'>No credit card required · Setup in 60 seconds</p></div>", unsafe_allow_html=True)

# PAGE 2: FOCUSED SEARCH LAYER
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

# PAGE 3: COMPACT SYSTEM METRIC VIEWER
# PAGE 3: PREMIUM DARK REVIEW INTERFACE
# PAGE 3: REFINED DARK REVIEW INTERFACE (NO CARD COLORS - FLUID TEXT MATRIX)
elif st.session_state.page == 'results':
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    
    c_back, _ = st.columns([1.2, 8.8])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go_to_input()
            st.rerun()
        
    st.markdown(f"""
        <div class="ctx-bar">
            <div>
                <div class="ctx-repo">{st.session_state.repo} / pull / {st.session_state.pr}</div>
                <div class="ctx-pr">PR #{st.session_state.pr} · GitHub Repository</div>
            </div>
            <a href="https://github.com/{st.session_state.repo}/pull/{st.session_state.pr}" 
               target="_blank" style="text-decoration:none; background:#4A9EFF; color:#060910; padding:10px 18px; border-radius:6px; font-weight:600; font-size:13px; font-family: 'Fira Code', monospace;">
               VIEW ON GITHUB ↗
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
                <div class="tile tile-score">
                    <div class="tile-label">Quality Score</div>
                    <div class="tile-val tv-score" style="color:var(--accent-blue);">{score}<span style='font-size:14px;color:var(--text-muted-dark);font-family:var(--ff-mono);font-style:normal;'> out of 10</span></div>
                </div>
                <div class="tile tile-bugs">
                    <div class="tile-label">Bugs Found</div>
                    <div class="tile-val tv-bugs" style="color:var(--accent-green);">{len(bugs)}<span style='font-size:14px;color:var(--text-muted-dark);font-family:var(--ff-mono);font-style:normal;'> issues detected</span></div>
                </div>
                <div class="tile tile-perf">
                    <div class="tile-label">Improvements</div>
                    <div class="tile-val tv-perf" style="color:var(--accent-amber);">{len(imps)}<span style='font-size:14px;color:var(--text-muted-dark);font-family:var(--ff-mono);font-style:normal;'> suggestions</span></div>
                </div>
                <div class="tile tile-sec">
                    <div class="tile-label">Security</div>
                    <div class="tile-val tv-sec" style="color:var(--accent-rose);">{len(secs)}<span style='font-size:14px;color:var(--text-muted-dark);font-family:var(--ff-mono);font-style:normal;'> vulnerabilities</span></div>
                </div>
            </div>
            
            <div class="summary-box">
                <h4>AI Summary</h4>
                <p>{summ}</p>
            </div>
        """, unsafe_allow_html=True)

        # ── ⚡ RECONSTRUCTED FLAT COLUMN GRID (Matches image_2e4cdd / Screenshot 025125 exactly) ──
        c1, c2, c3, c4 = st.columns([3, 3, 3, 2.5])
        
        with c1:
            # Title Row with flat container execution
            st.markdown(f"""
                <h4 style="font-family:var(--ff-editor-display); font-style:italic; font-size:28px; color:var(--text-primary-dark); margin:0 0 16px 0; display:flex; align-items:center; gap:12px;">
                    Bugs <span class="sec-count" style="font-style:normal; font-family:var(--ff-mono); font-size:11px; color:var(--text-secondary-dark); background:rgba(74,158,255,0.06); padding:3px 10px; border-radius:20px; border:1px solid var(--border-dark);">{len(bugs)} found</span>
                </h4>
                <div style="height:260px; overflow-y:auto; padding-right:4px;">
                    {findings_html("🪲", "fi-bug", bugs, "bug")}
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <h4 style="font-family:var(--ff-editor-display); font-style:italic; font-size:28px; color:var(--text-primary-dark); margin:0 0 16px 0; display:flex; align-items:center; gap:12px;">
                    Performance <span class="sec-count" style="font-style:normal; font-family:var(--ff-mono); font-size:11px; color:var(--text-secondary-dark); background:rgba(74,158,255,0.06); padding:3px 10px; border-radius:20px; border:1px solid var(--border-dark);">{len(imps)} suggestions</span>
                </h4>
                <div style="height:260px; overflow-y:auto; padding-right:4px;">
                    {findings_html("⚡", "fi-perf", imps, "suggestion")}
                </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
                <h4 style="font-family:var(--ff-editor-display); font-style:italic; font-size:28px; color:var(--text-primary-dark); margin:0 0 16px 0; display:flex; align-items:center; gap:12px;">
                    Security <span class="sec-count" style="font-style:normal; font-family:var(--ff-mono); font-size:11px; color:var(--text-secondary-dark); background:rgba(74,158,255,0.06); padding:3px 10px; border-radius:20px; border:1px solid var(--border-dark);">{len(secs)} issues</span>
                </h4>
                <div style="height:260px; overflow-y:auto; padding-right:4px;">
                    {findings_html("🔒", "fi-sec", secs, "security issue")}
                </div>
            """, unsafe_allow_html=True)
            
        with c4:
            st.markdown(f"""
                <div class="score-card" style="--pct:{pct}; height:290px; margin-top:10px;">
                    <div class="score-ring">
                        <div class="score-inner">
                            <div class="score-num">{score}</div>
                        </div>
                    </div>
                    <div class="score-den">/ 10 quality score</div>
                    <div class="score-verdict {sv_c}">{sv_t}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 50px;'></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
