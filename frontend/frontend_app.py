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
html, body, 
[data-testid="stAppViewContainer"], 
[data-testid="stMain"], 
.main, 
.block-container {
    background-color: #F7F8FA !important;
    background: #F7F8FA !important;
    color: #0F172A !important;
    font-family: 'Inter', sans-serif !important;
}

/* Framework Clean Up Overrides */
.main .block-container { padding: 20px 0 0 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"], header, footer { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; height: 0px !important; }

/* ── NATIVE NAVBAR BUTTON RESET OVERRIDES ── */
div[data-testid="stHorizontalBlock"] .stButton > button {
    background: transparent !important;
    color: #475569 !important;
    border: none !important;
    padding: 6px 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transform: none !important;
    transition: color 0.15s ease !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    color: #0F172A !important;
    background: transparent !important;
}

/* ── STATIC LIGHT NAVBAR EMBEDDED STYLES ── */
.navbar-static {
    display: flex; justify-content: space-between; align-items: center; padding: 10px 60px; background: transparent;
}
.nav-brand {
    font-family: 'Inter', sans-serif; font-weight: 600; font-size: 19px; display: flex; align-items: center; gap: 8px; color: #0F172A !important;
}
.nav-brand-icon { color: #E11D48; font-size: 22px; line-height: 1; }
.btn-solid { background: #0F172A !important; color: white !important; padding: 10px 22px; border-radius: 30px; }

/* ── HERO GRAPHIC CANVAS STYLING ── */
.hero-container {
    padding-top: 50px; padding-bottom: 70px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: transparent;
}
.hero-title {
    font-family: 'Fraunces', serif; font-size: 84px; font-weight: 300; line-height: 1.1; color: #0F172A !important; margin-bottom: 24px; letter-spacing: -2px;
}
.hero-title i { font-style: italic; color: #1E293B !important; font-weight: 400; }
.hero-subtitle {
    font-family: 'Inter', sans-serif; font-size: 17px; color: #475569 !important; max-width: 580px; line-height: 1.6; margin-bottom: 30px;
}
.bg-canvas {
    position: absolute; top: 0; left: 0; right: 0; height: 580px;
    background: radial-gradient(circle at 50% 25%, #EBF1FA 0%, #F1F5F9 35%, #F7F8FA 70%) !important; z-index: -1;
}

/* ── INPUT LAYOUT FORM SCREEN ── */
.form-screen { padding: 40px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.input-card {
    background: #FFFFFF !important; padding: 40px; border-radius: 24px; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; width: 100%; max-width: 520px; text-align: center; margin-bottom: 24px;
}
.input-card h2 { font-family: 'Fraunces', serif; font-size: 36px; font-style: italic; margin-bottom: 12px; color: #0F172A !important; }
.input-card p { color: #475569 !important; font-size: 14px; margin-bottom: 0; }

/* ── SECTION TARGET MATRIX DISPLAYED ELEMENTS ── */
.section-anchor {
    padding: 50px 44px; background: #FFFFFF !important; border-radius: 12px; margin-top: 24px; border: 1px solid #E2E8F0; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05); text-align: left !important;
}
.section-anchor h2 { font-family: 'Fraunces', serif; font-style: italic; font-size: 32px; color: #0F172A !important; margin-bottom: 12px; text-align: left !important;}
.section-anchor p { color: #475569 !important; line-height: 1.65; font-size: 14.5px; text-align: left !important;}

/* ── GLOBAL WORKSPACE FORM ENGINES ── */
.stTextInput input, .stNumberInput input {
    background: #FFFFFF !important; border: 1px solid #E2E8F0 !important; border-radius: 6px !important; padding: 10px 14px !important; font-family: 'Fira Code', monospace !important; color: #0F172A !important;
}
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




# ══════════════════════════════════════════════════════
# ROUTER — VIEW CONTROLLER ARCHITECTURE
# ══════════════════════════════════════════════════════


# PAGE 1: REFINED LIGHT LANDING
if st.session_state.page == 'landing':
    st.markdown('<div class="bg-canvas"></div>', unsafe_allow_html=True)
    
    # ── NATIVE LINK NAVIGATION BAR ──
    nav_cols = st.columns([2.5, 1, 1.2, 1, 1.2, 2.5, 1.1])
    
    with nav_cols[0]:
        st.markdown('<div class="nav-brand" style="margin-top:5px;"><span class="nav-brand-icon">◈</span> CodeSentry</div>', unsafe_allow_html=True)
    
    with nav_cols[1]:
        if st.button("Features", key="nav_feat"):
            st.markdown("<script>window.scrollTo({top: 520, behavior: 'smooth'});</script>", unsafe_allow_html=True)
            
    with nav_cols[2]:
        if st.button("How it Works", key="nav_how"):
            st.markdown("<script>window.scrollTo({top: 760, behavior: 'smooth'});</script>", unsafe_allow_html=True)
            
    with nav_cols[3]:
        if st.button("Pricing", key="nav_price"):
            st.markdown("<script>window.scrollTo({top: 1000, behavior: 'smooth'});</script>", unsafe_allow_html=True)
            
    with nav_cols[4]:
        if st.button("Changelog", key="nav_change"):
            st.markdown("<script>window.scrollTo({top: 1240, behavior: 'smooth'});</script>", unsafe_allow_html=True)
            
    with nav_cols[5]:
        st.markdown('<div style="text-align:right; margin-top:5px; font-size:14px; font-weight:500; color:#475569; cursor:pointer;">Log in</div>', unsafe_allow_html=True)
        
    with nav_cols[6]:
        st.markdown('<div class="btn-solid" style="text-align:center; font-size:14px; font-weight:500; cursor:pointer;">Sign up</div>', unsafe_allow_html=True)

    # ── HERO BANNER ──
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
        st.markdown("""
            <div style="background: #FFFFFF !important;
                        border: 1px solid #E2E8F0 !important;
                        border-radius: 16px !important;
                        padding: 32px 40px !important;
                        text-align: center !important;
                        margin-top: -10px !important;
                        margin-bottom: 20px !important;
                        box-shadow: 0 10px 30px -15px rgba(15, 23, 42, 0.08) !important;">
        """, unsafe_allow_html=True)
        if st.button("Connect GitHub Free", use_container_width=True):
            go_to_input()
            st.rerun()
        st.markdown("<p>style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                          font-size: 13px !important; 
                          color: #64748B !important; 
                          margin: 16px 0 0 0 !important; 
                          text-align: center !important;
                          font-weight: 400 !important;
                          letter-spacing: -0.1px !important;">
                    No credit card required · Setup in 60 seconds</p></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 150px; padding: 0 60px;'>", unsafe_allow_html=True)
    
    # Features Section

    st.markdown("""
        <div id="features" class="section-anchor">
            <h2>Features</h2>
            <p>
                • <b>Deep Bug Detection:</b> Locates complex logical fallacies and functional math bugs instantly.<br>
                • <b>Performance Validation:</b> Recommends code validation changes to keep your algorithms hyper-fast.<br>
                • <b>Zero-Trust Security:</b> Scans dependencies and checks for exposed access tokens or dangerous parameters.
            </p>
        </div>
        <div style="height: 100px;"></div>
    """, unsafe_allow_html=True)
    
    # 2. How it Works Section (Target pixel: ~760)
    st.markdown("""
        <div id="how-it-works" class="section-anchor">
            <h2>How it Works</h2>
            <p>
                1. Provide your public or private GitHub repository path.<br>
                2. Input the pull request target sequence number identifier.<br>
                3. Our LLaMA-powered intelligence parses the code delta to yield structured analytics.
            </p>
        </div>
        <div style="height: 100px;"></div>
    """, unsafe_allow_html=True)

    # 3. Pricing Section (Target pixel: ~1000)
    st.markdown("""
        <div id="pricing" class="section-anchor">
            <h2>Pricing</h2>
            <p>
                • <b>Developer Tier:</b> Free forever for up to 50 review analyses per month.<br>
                • <b>Startup Tier ($19/mo):</b> Unlimited repo scans with deep historical tracking pipelines.
            </p>
        </div>
        <div style="height: 100px;"></div>
    """, unsafe_allow_html=True)

    # 4. Changelog Section (Target pixel: ~1240)
    st.markdown("""
        <div id="changelog" class="section-anchor">
            <h2>Changelog</h2>
            <p>
                • <b>v1.0 (Current):</b> Shifted to clean light landing templates with high contrast dark workspace dashboard components.<br>
                • <b>v0.8:</b> Added multi-page routing state trackers and support for Groq LLaMA 3 inference endpoints.
            </p>
        </div>
        <div style='margin-bottom: 250px;'></div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── ⚡ PAGE 2: FIXED HIGHER CONTRAST INPUT CARD SCREEN ──
elif st.session_state.page == 'input':
    # Replaced render_navbar() with static high-contrast brand bar
    st.markdown("""
        <div class="navbar-static" style="padding: 24px 60px;">
            <div class="nav-brand"><span class="nav-brand-icon">◈</span> CodeSentry</div>
        </div>
        <div class="form-screen">
    """, unsafe_allow_html=True)
    
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

# ── ⚡ PAGE 3: COMPACT LIGHT METRIC WORKSPACE ──
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
               target="_blank" style="text-decoration:none; background:#3B82F6; color:#FFFFFF; padding:10px 18px; border-radius:6px; font-weight:600; font-size:13px; font-family: 'Fira Code', monospace;">
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
                    <div class="tile-val tv-score">{score}<span style='font-size:14px; color:#94A3B8; font-family:var(--ff-mono); font-style:normal;'> out of 10</span></div>
                </div>
                <div class="tile tile-bugs">
                    <div class="tile-label">Bugs Found</div>
                    <div class="tile-val tv-bugs">{len(bugs)}<span style='font-size:14px; color:#94A3B8; font-family:var(--ff-mono); font-style:normal;'> issues detected</span></div>
                </div>
                <div class="tile tile-perf">
                    <div class="tile-label">Improvements</div>
                    <div class="tile-val tv-perf">{len(imps)}<span style='font-size:14px; color:#94A3B8; font-family:var(--ff-mono); font-style:normal;'> suggestions</span></div>
                </div>
                <div class="tile tile-sec">
                    <div class="tile-label">Security</div>
                    <div class="tile-val tv-sec">{len(secs)}<span style='font-size:14px; color:#94A3B8; font-family:var(--ff-mono); font-style:normal;'> vulnerabilities</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if summ:
            st.markdown(f"""
                <div style="background-color: #FFFFFF !important; 
                            border: 1px solid #E2E8F0 !important; 
                            padding: 24px 28px !important; 
                            border-radius: 12px !important; 
                            margin-top: 15px !important;
                            margin-bottom: 25px !important;
                            display: block !important;
                            box-shadow: 0 4px 12px rgba(15,23,42,0.015) !important;">
                    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                                font-size: 13px !important; 
                                text-transform: uppercase !important; 
                                letter-spacing: 1.5px !important; 
                                color: #0F172A !important; 
                                font-weight: 700 !important;
                                margin-bottom: 12px !important;
                                display: block !important;
                                visibility: visible !important;">
                        AI Summary
                    </div>
                    <p style="color: #475569 !important; 
                              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                              font-size: 14.5px !important; 
                              margin: 0 !important; 
                              line-height: 1.65 !important; 
                              font-style: normal !important;
                              font-weight: 400 !important;
                              display: block !important;">
                        {review.get("summary", "No summary text returned.")}
                    </p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        # ── COLUMN GRID ──
        c1, c2, c3, c4 = st.columns([3, 3, 3, 2.5])
        
        with c1:
            st.markdown(f"""
                <h4 style="font-family:var(--ff-display); font-style:italic; font-size:28px; color:var(--text-main-light); margin:0 0 16px 0; display:flex; align-items:center; gap:12px;">
                    Bugs <span class="sec-count" style="font-style:normal; font-family:var(--ff-mono); font-size:11px; color:#475569; background:#FFFFFF; padding:3px 10px; border-radius:20px; border:1px solid #E2E8F0;">{len(bugs)} found</span>
                </h4>
                <div style="height:260px; overflow-y:auto; padding-right:4px;">
                    {findings_html("🪲", "fi-bug", bugs, "bug")}
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <h4 style="font-family:var(--ff-display); font-style:italic; font-size:28px; color:var(--text-main-light); margin:0 0 16px 0; display:flex; align-items:center; gap:12px;">
                    Performance <span class="sec-count" style="font-style:normal; font-family:var(--ff-mono); font-size:11px; color:#475569; background:#FFFFFF; padding:3px 10px; border-radius:20px; border:1px solid #E2E8F0;">{len(imps)} suggestions</span>
                </h4>
                <div style="height:260px; overflow-y:auto; padding-right:4px;">
                    {findings_html("⚡", "fi-perf", imps, "suggestion")}
                </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
                <h4 style="font-family:var(--ff-display); font-style:italic; font-size:28px; color:var(--text-main-light); margin:0 0 16px 0; display:flex; align-items:center; gap:12px;">
                    Security <span class="sec-count" style="font-style:normal; font-family:var(--ff-mono); font-size:11px; color:#475569; background:#FFFFFF; padding:3px 10px; border-radius:20px; border:1px solid #E2E8F0;">{len(secs)} issues</span>
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
