import streamlit as st
import requests
from datetime import datetime
import urllib.parse
import os

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
# how to run: streamlit run frontend/frontend_app.py

st.set_page_config(
    page_title="CodeSentry — AI Code Reviews",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GitHub OAuth Config ────────────────────────────────────────────────────────
# 1. Go to GitHub → Settings → Developer Settings → OAuth Apps → New OAuth App
# 2. Set Homepage URL: http://localhost:8501
# 3. Set Authorization callback URL: http://localhost:8501
# 4. Copy Client ID and Client Secret into .env or environment variables
# 5. Set these env vars before running:
#    export GITHUB_CLIENT_ID=your_client_id
#    export GITHUB_CLIENT_SECRET=your_client_secret

GITHUB_CLIENT_ID     = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
REDIRECT_URI         = "http://localhost:8501"
API_URL              = "http://localhost:8000"

# ── Session state init ─────────────────────────────────────────────────────────
DEFAULTS = {
    "page":         "landing",
    "gh_token":     None,
    "gh_user":      None,
    "gh_avatar":    None,
    "repo":         "",
    "pr":           1,
    "result":       None,
    "prs":          [],
    "auth_error":   "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Handle GitHub OAuth callback ───────────────────────────────────────────────
params = st.query_params
if "code" in params and st.session_state.gh_token is None:
    code = params["code"]
    try:
        token_resp = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id":     GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code":          code,
                "redirect_uri":  REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
            timeout=15
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token")

        if access_token:
            user_resp = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            user_data = user_resp.json()
            st.session_state.gh_token  = access_token
            st.session_state.gh_user   = user_data.get("login", "github_user")
            st.session_state.gh_avatar = user_data.get("avatar_url", "")
            st.session_state.page      = "input"
            st.query_params.clear()
            st.rerun()
        else:
            st.session_state.auth_error = token_data.get("error_description", "OAuth failed")
    except Exception as e:
        st.session_state.auth_error = str(e)

def github_oauth_url():
    params = urllib.parse.urlencode({
        "client_id":    GITHUB_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope":        "repo read:user",
        "state":        "codesentry",
    })
    return f"https://github.com/login/oauth/authorize?{params}"

def fetch_prs(repo, token=None):
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        r = requests.get(f"{API_URL}/prs", params={"repo": repo, "limit": 10}, timeout=10, headers=headers)
        return r.json().get("prs", []) if r.status_code == 200 else []
    except:
        return []

def get_review(repo, pr_num):
    try:
        r = requests.post(f"{API_URL}/review", json={"repo": repo, "pr_number": int(pr_num)}, timeout=60)
        return (r.json(), None) if r.status_code == 200 else (None, f"Error {r.status_code}: {r.text}")
    except requests.exceptions.ConnectionError:
        return (None, "conn")
    except Exception as e:
        return (None, str(e))

def score_meta(s):
    if s >= 9: return "EXCELLENT","sv-e"
    if s >= 7: return "GOOD","sv-g"
    if s >= 5: return "AVERAGE","sv-a"
    return "NEEDS WORK","sv-p"

def sev_badge(sev):
    s = (sev or "low").lower()
    c = {"critical":"s-cr","high":"s-hi","medium":"s-me","low":"s-lo"}.get(s,"s-lo")
    return f'<span class="sev {c}">{s}</span>'

def findings_html(icon, cls, items, kind):
    if not items:
        return f'<div class="f-empty">◈ &nbsp; No {kind}s detected in this pull request</div>'
    out = ""
    for it in items:
        if isinstance(it, dict): desc,loc,sev = it.get("description",""),it.get("line",""),it.get("severity","")
        else: desc,loc,sev = str(it),"",""
        badge_html = sev_badge(sev) if sev else ""
        loc_html = f'<span class="f-loc">◍ {loc}</span>' if loc else ""
        
        out += f"""<div class="finding">
                    <div class="f-icon {cls}">{icon}</div>
                    <div class="f-body">
                        <div class="f-desc">{desc}</div>
                        <div class="f-foot">{badge_html}{loc_html}</div>
                    </div>
                  </div>"""
    return out

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;1,9..144,300;1,9..144,400;1,9..144,500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --white:#FFFFFF; --off:#F8F9FB; --off2:#F1F4F8;
    --border:#E4E8EF; --border-2:#CDD5DF;
    --ink:#0F172A; --ink-2:#334155; --ink-3:#64748B; --ink-4:#94A3B8;
    --blue:#2563EB; --blue-lt:#EFF4FF; --blue-md:#BFDBFE;
    --red:#E11D48; --green:#059669; --green-lt:#ECFDF5;
    --amber:#D97706; --amber-lt:#FFFBEB;
    --ff-d:'Fraunces',Georgia,serif; --ff-s:'Inter',system-ui,sans-serif; --ff-m:'JetBrains Mono',monospace;
    --r:8px; --r-lg:16px; --r-xl:24px;
}

*,*::before,*::after{box-sizing:border-box;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],.main,.block-container{
    background:var(--off)!important;color:var(--ink)!important;font-family:var(--ff-s)!important;padding:0!important;max-width:100%!important;}
.main .block-container{padding-top:0!important;}
[data-testid="stSidebar"]{display:none!important;}
#MainMenu,footer,header,[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important;}
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-track{background:transparent;}::-webkit-scrollbar-thumb{background:var(--border-2);border-radius:3px;}

/* ── NAV ── */
.topnav{height:64px;background:rgba(255,255,255,0.85);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 60px;position:sticky;top:0;z-index:999;}
.nav-logo{font-family:var(--ff-s);font-weight:700;font-size:18px;color:var(--ink);display:flex;align-items:center;gap:8px;letter-spacing:-0.3px;}
.nav-gem{color:var(--red);}
.nav-links{display:flex;align-items:center;gap:36px;font-size:14px;font-weight:500;color:var(--ink-3);}
.nav-links a{color:var(--ink-3);text-decoration:none;transition:color 0.15s;}
.nav-links a:hover{color:var(--ink);}
.nav-actions{display:flex;align-items:center;gap:10px;}
.btn-ghost{font-family:var(--ff-s);font-size:14px;font-weight:500;color:var(--ink-3);padding:8px 16px;border-radius:var(--r);background:transparent;border:none;cursor:pointer;transition:color 0.15s;}
.btn-dark{font-family:var(--ff-s);font-size:14px;font-weight:600;color:white;padding:9px 20px;border-radius:30px;background:var(--ink);border:none;cursor:pointer;transition:opacity 0.15s;}
.btn-dark:hover{opacity:0.85;}
.nav-avatar{width:32px;height:32px;border-radius:50%;border:2px solid var(--border-2);object-fit:cover;}
.nav-username{font-family:var(--ff-m);font-size:12px;color:var(--ink-2);font-weight:500;}

/* ── ANIMATIONS ── */
@keyframes fadeUp{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes scaleIn{from{opacity:0;transform:scale(0.96)}to{opacity:1;transform:scale(1)}}
@keyframes slideRight{from{opacity:0;transform:translateX(-24px)}to{opacity:1;transform:translateX(0)}}
@keyframes countUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes shimmer{0%{background-position:-200% center}100%{background-position:200% center}}
@keyframes dotPulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.4);opacity:0.6}}
@keyframes borderGlow{0%,100%{box-shadow:0 0 0 0 rgba(37,99,235,0)}50%{box-shadow:0 0 0 4px rgba(37,99,235,0.12)}}

.anim-hero{animation:fadeUp 0.7s cubic-bezier(0.16,1,0.3,1) forwards;}
.anim-hero-delayed{animation:fadeUp 0.7s 0.15s cubic-bezier(0.16,1,0.3,1) both;}
.anim-hero-delayed-2{animation:fadeUp 0.7s 0.28s cubic-bezier(0.16,1,0.3,1) both;}
.anim-hero-delayed-3{animation:fadeUp 0.7s 0.4s cubic-bezier(0.16,1,0.3,1) both;}
.anim-fade{animation:fadeIn 0.6s ease forwards;}
.anim-scale{animation:scaleIn 0.5s cubic-bezier(0.16,1,0.3,1) forwards;}

.feat-card{animation:fadeUp 0.6s cubic-bezier(0.16,1,0.3,1) both;}
.feat-card:nth-child(1){animation-delay:0.1s;}
.feat-card:nth-child(2){animation-delay:0.2s;}
.feat-card:nth-child(3){animation-delay:0.3s;}

.step-card{animation:slideRight 0.6s cubic-bezier(0.16,1,0.3,1) both;}
.step-card:nth-child(1){animation-delay:0.05s;}
.step-card:nth-child(2){animation-delay:0.15s;}
.step-card:nth-child(3){animation-delay:0.25s;}

.metric{animation:countUp 0.5s cubic-bezier(0.16,1,0.3,1) both;}
.metric:nth-child(1){animation-delay:0.05s;}
.metric:nth-child(2){animation-delay:0.12s;}
.metric:nth-child(3){animation-delay:0.19s;}
.metric:nth-child(4){animation-delay:0.26s;}

.finding{animation:fadeUp 0.4s cubic-bezier(0.16,1,0.3,1) both;}

/* ── HERO ── */
.hero-wrap{padding:100px 60px 88px;text-align:center;background:radial-gradient(ellipse at 50% -10%,#E0EAFF 0%,var(--off) 55%);}
.hero-eyebrow{display:inline-flex;align-items:center;gap:8px;background:var(--white);border:1px solid var(--border);border-radius:30px;padding:6px 16px;font-size:12px;font-weight:500;color:var(--ink-3);letter-spacing:0.3px;margin-bottom:32px;animation:fadeIn 0.5s ease forwards;}
.hero-dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 0 2px #ECFDF5;animation:dotPulse 2s ease-in-out infinite;}
.hero-h1{font-family:var(--ff-d);font-size:84px;font-weight:300;line-height:1.04;color:var(--ink);letter-spacing:-2.5px;margin-bottom:24px;}
.hero-h1 i{font-style:italic;color:var(--ink-2);}
.hero-sub{font-size:18px;color:var(--ink-3);max-width:580px;margin:0 auto 48px;line-height:1.65;font-weight:400;}
.hero-note{font-size:13px;color:var(--ink-4);margin-top:14px;}

/* Shimmer CTA */
.btn-hero{font-family:var(--ff-s);font-size:15px;font-weight:600;color:var(--white);background:var(--ink);border:none;border-radius:40px;padding:16px 40px;cursor:pointer;position:relative;overflow:hidden;transition:transform 0.2s,box-shadow 0.2s;box-shadow:0 4px 20px rgba(15,23,42,0.18);}
.btn-hero::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.12),transparent);background-size:200% auto;animation:shimmer 2.5s linear infinite;}
.btn-hero:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(15,23,42,0.22);}

/* GitHub OAuth button */
.btn-github{font-family:var(--ff-s);font-size:14px;font-weight:600;color:var(--white);background:#24292F;border:none;border-radius:var(--r-lg);padding:14px 24px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;width:100%;transition:opacity 0.15s;text-decoration:none;}
.btn-github:hover{opacity:0.88;}
.gh-icon{width:20px;height:20px;fill:white;flex-shrink:0;}

/* ── FEATURES ── */
.section{padding:80px 60px;}
.section-label{font-family:var(--ff-m);font-size:11px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:var(--blue);margin-bottom:14px;}
.section-h2{font-family:var(--ff-d);font-style:italic;font-size:48px;font-weight:300;color:var(--ink);letter-spacing:-1.2px;margin-bottom:14px;}
.section-p{font-size:16px;color:var(--ink-3);max-width:540px;line-height:1.7;}
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:52px;}
.feat-card{background:var(--white);border:1px solid var(--border);border-radius:var(--r-lg);padding:28px 28px 24px;transition:border-color 0.2s,transform 0.2s,box-shadow 0.2s;}
.feat-card:hover{border-color:var(--border-2);transform:translateY(-3px);box-shadow:0 12px 40px rgba(15,23,42,0.06);}
.feat-icon{width:42px;height:42px;border-radius:var(--r);background:var(--blue-lt);display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:18px;}
.feat-title{font-size:15px;font-weight:600;color:var(--ink);margin-bottom:8px;}
.feat-desc{font-size:14px;color:var(--ink-3);line-height:1.6;}

/* ── HOW IT WORKS ── */
.how-wrap{background:var(--white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);}
.step-grid{display:grid;grid-template-columns:repeat(3,1fr);}
.step-card{padding:44px 40px;border-right:1px solid var(--border);transition:background 0.2s;}
.step-card:last-child{border-right:none;}
.step-card:hover{background:var(--off);}
.step-num{font-family:var(--ff-m);font-size:11px;font-weight:500;letter-spacing:2px;color:var(--ink-4);margin-bottom:18px;}
.step-title{font-family:var(--ff-d);font-style:italic;font-size:26px;font-weight:300;color:var(--ink);margin-bottom:10px;letter-spacing:-0.3px;}
.step-desc{font-size:14px;color:var(--ink-3);line-height:1.6;}

/* ── SOCIAL PROOF ── */
.proof-wrap{padding:72px 60px;text-align:center;}
.proof-nums{display:grid;grid-template-columns:repeat(3,1fr);gap:0;max-width:680px;margin:48px auto 0;background:var(--white);border:1px solid var(--border);border-radius:var(--r-xl);}
.proof-num{padding:32px;border-right:1px solid var(--border);}
.proof-num:last-child{border-right:none;}
.proof-val{font-family:var(--ff-d);font-style:italic;font-size:44px;font-weight:300;color:var(--ink);letter-spacing:-1.5px;line-height:1;}
.proof-lbl{font-size:13px;color:var(--ink-3);margin-top:6px;}

/* ── PRICING ── */
.price-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;max-width:740px;margin:48px auto 0;}
.price-card{background:var(--white);border:1px solid var(--border);border-radius:var(--r-xl);padding:32px 32px 28px;transition:transform 0.2s;}
.price-card:hover{transform:translateY(-2px);}
.price-card.featured{border-color:#2563EB;box-shadow:0 0 0 3px rgba(37,99,235,0.08);}
.price-badge{display:inline-block;font-family:var(--ff-m);font-size:10px;font-weight:500;letter-spacing:1px;text-transform:uppercase;background:var(--blue-lt);color:var(--blue);padding:4px 10px;border-radius:20px;margin-bottom:18px;}
.price-name{font-size:15px;font-weight:600;color:var(--ink);margin-bottom:8px;}
.price-val{font-family:var(--ff-d);font-size:44px;font-style:italic;font-weight:300;color:var(--ink);letter-spacing:-1.5px;margin-bottom:4px;}
.price-per{font-size:13px;color:var(--ink-4);margin-bottom:24px;}
.price-feat{font-size:13px;color:var(--ink-3);padding:9px 0;border-top:1px solid var(--border);display:flex;align-items:flex-start;gap:10px;}
.price-check{color:var(--green);font-weight:700;flex-shrink:0;}

/* ── FOOTER ── */
.footer{padding:40px 60px;border-top:1px solid var(--border);background:var(--white);display:flex;align-items:center;justify-content:space-between;}
.footer-brand{font-size:15px;font-weight:700;color:var(--ink);display:flex;align-items:center;gap:8px;}
.footer-note{font-size:13px;color:var(--ink-4);}

/* ── PAGE 2: INPUT ── */
.input-shell{min-height:auto;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding:0 20px 3px 20px;background:radial-gradient(ellipse at 50% 0%,#E8F0FF 0%,var(--off) 55%);}
    .input-card{
    background:transparent;
    border:none;
    padding:0 40px;
    box-shadow:none;
    width:100%;
    max-width:500px;
    animation:scaleIn 0.45s cubic-bezier(0.16,1,0.3,1) forwards;
    margin:0 auto;
}

.input-h1{font-family:var(--ff-d);font-style:italic;font-size:36px;font-weight:300;color:var(--ink);letter-spacing:-1px;margin:0 40px 6px 10px;padding:0;}
.input-sub{font-size:14px;color:var(--ink-3);line-height:1.5;margin-bottom:28px;padding:0 10px;}
.f-label{font-family:var(--ff-m);font-size:10px;font-weight:500;letter-spacing:1.5px;text-transform:uppercase;color:var(--ink-4);margin-bottom:7px;padding:0 10px;}
.f-hint{font-size:12px;color:var(--ink-4);margin-top:5px;padding:0 10px;}
.input-divider{height:1px;background:var(--border);margin:22px 40px;padding:0;}
.auth-status{display:flex;align-items:center;gap:10px;background:var(--green-lt);border:1px solid #BBF7D0;border-radius:var(--r);padding:12px 16px;margin-bottom:20px;}
.auth-avatar{width:28px;height:28px;border-radius:50%;border:1px solid #BBF7D0;}
.auth-name{font-family:var(--ff-m);font-size:12px;font-weight:500;color:#166534;}
.auth-check{font-size:14px;color:var(--green);margin-left:auto;}

/* ── PAGE 3: RESULTS ── */
.results-bar{background:rgba(255,255,255,0.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:0 52px;height:56px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:900;animation:fadeIn 0.3s ease forwards;}
.tb-pr{font-family:var(--ff-m);font-size:13px;font-weight:500;color:var(--ink);}
.tb-sub{font-size:12px;color:var(--ink-4);margin-left:6px;}
.tag{font-family:var(--ff-m);font-size:10px;font-weight:500;letter-spacing:0.8px;text-transform:uppercase;padding:5px 12px;border-radius:20px;}
.tag-date{background:var(--off);color:var(--ink-3);border:1px solid var(--border);}
.tag-gh{background:var(--ink);color:var(--white);text-decoration:none;display:inline-block;margin-left:8px;}

.results-wrap{padding:8px 45px 64px 52px;background:var(--off);max-width:1400px;margin:0 auto;}
.sum-card{background:var(--white);border:1px solid var(--border);border-radius:var(--r-lg);padding:24px 28px;margin:0 auto 24px auto;;position:relative;overflow:hidden;animation:fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) forwards;}
.sum-card::after{content:'"';font-family:var(--ff-d);font-size:120px;color:rgba(15,23,42,0.03);position:absolute;top:-20px;right:16px;line-height:1;pointer-events:none;}
.sum-lbl{font-family:var(--ff-m);font-size:9px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:var(--ink-4);margin-bottom:10px;}
.sum-body{font-size:15px;color:var(--ink-2);line-height:1.72;font-style:italic;}

.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px;max-width:1200px;margin-left:auto;margin-right:auto;}
.metric{background:var(--white);border:1px solid var(--border);border-radius:var(--r-lg);padding:20px 22px 18px;position:relative;overflow:hidden;transition:transform 0.18s,box-shadow 0.18s;}
.metric:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(15,23,42,0.06);}
.metric::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;}
.m-sc::after{background:linear-gradient(90deg,#2563EB,#7C3AED);}
.m-bu::after{background:linear-gradient(90deg,#059669,#0D9488);}
.m-pe::after{background:linear-gradient(90deg,#D97706,#F59E0B);}
.m-se::after{background:linear-gradient(90deg,#E11D48,#F87171);}
.metric-lbl{font-family:var(--ff-m);font-size:9px;font-weight:500;letter-spacing:1.8px;text-transform:uppercase;color:var(--ink-4);margin-bottom:10px;}
.metric-val{font-family:var(--ff-d);font-style:italic;font-size:40px;font-weight:300;line-height:1;letter-spacing:-1.5px;}
.mv-sc{color:#2563EB;}.mv-bu{color:#059669;}.mv-pe{color:#D97706;}.mv-se{color:#E11D48;}
.metric-hint{font-size:11px;color:var(--ink-4);margin-top:6px;font-family:var(--ff-m);}
.rule{height:1px;background:var(--border);margin:28px 0;}
.sec-h{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;padding:0 20px;}
.sec-title{font-family:var(--ff-d);font-style:italic;font-size:22px;font-weight:300;color:var(--ink);letter-spacing:-0.3px;}
.sec-badge{font-family:var(--ff-m);font-size:10px;color:var(--ink-3);background:var(--white);border:1px solid var(--border);padding:3px 10px;border-radius:20px;}
.findings-wrapper{
    background:var(--white);
    border:1px solid var(--border);
    border-radius:var(--r-lg);
    padding:20px;
    margin-bottom:20px;
}
.finding{background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:14px 16px;margin-bottom:9px;display:flex;gap:12px;align-items:flex-start;transition:border-color 0.12s,box-shadow 0.12s;}
.finding:hover{border-color:var(--border-2);box-shadow:0 4px 12px rgba(15,23,42,0.04);}
.f-icon{width:30px;height:30px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;margin-top:1px;}
.fi-b{background:#F0FDF4;}.fi-p{background:#FFFBEB;}.fi-s{background:#FFF1F2;}
.f-body{flex:1;min-width:0;}
.f-desc{font-size:13px;color:var(--ink-2);line-height:1.58;}
.f-foot{margin-top:8px;display:flex;align-items:center;gap:7px;flex-wrap:wrap;}
.sev{font-family:var(--ff-m);font-size:9px;font-weight:500;letter-spacing:0.8px;text-transform:uppercase;padding:2px 7px;border-radius:4px;}
.s-cr{background:#FFF1F2;color:#BE123C;border:1px solid #FECDD3;}
.s-hi{background:#FFF7ED;color:#C2410C;border:1px solid #FED7AA;}
.s-me{background:#FFFBEB;color:#B45309;border:1px solid #FDE68A;}
.s-lo{background:#F0FDF4;color:#166534;border:1px solid #BBF7D0;}
.f-loc{font-family:var(--ff-m);font-size:10px;color:var(--ink-4);}
.f-empty{background:var(--white);border:1px dashed var(--border-2);border-radius:var(--r);padding:22px;text-align:center;font-family:var(--ff-m);font-size:11px;color:var(--ink-4);}
.score-card{background:var(--white);border:1px solid var(--border);border-radius:var(--r-lg);padding:32px 20px;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:290px;position:relative;overflow:hidden;animation:scaleIn 0.5s 0.3s cubic-bezier(0.16,1,0.3,1) both;}
.score-card::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(37,99,235,0.04) 0%,transparent 65%);pointer-events:none;}
.score-ring{width:110px;height:110px;border-radius:50%;background:conic-gradient(#2563EB calc(var(--pct) * 1%),#E4E8EF 0%);display:flex;align-items:center;justify-content:center;margin-bottom:18px;}
.score-inner{width:86px;height:86px;border-radius:50%;background:var(--white);display:flex;align-items:center;justify-content:center;}
.score-n{font-family:var(--ff-d);font-style:italic;font-size:46px;font-weight:300;color:#2563EB;letter-spacing:-2px;line-height:1;}
.score-den{font-size:12px;font-family:var(--ff-m);color:var(--ink-4);margin-bottom:12px;}
.score-v{font-family:var(--ff-m);font-size:10px;font-weight:500;letter-spacing:2px;text-transform:uppercase;padding:5px 14px;border-radius:20px;}
.sv-e{background:#F0FDF4;color:#166534;border:1px solid #BBF7D0;}
.sv-g{background:var(--blue-lt);color:var(--blue);border:1px solid var(--blue-md);}
.sv-a{background:#FFFBEB;color:#B45309;border:1px solid #FDE68A;}
.sv-p{background:#FFF1F2;color:#BE123C;border:1px solid #FECDD3;}

/* Streamlit overrides */
.stButton {
    margin:0!important;
    padding:0!important;
}
.stButton>button{background:var(--ink)!important;color:white!important;border:none!important;border-radius:var(--r)!important;font-family:var(--ff-s)!important;font-weight:500!important;font-size:14px!important;padding:12px 24px!important;transition:opacity 0.15s!important;box-shadow:none!important;margin:0!important;margin-bottom:20px!important;}
.stButton>button:hover{opacity:0.85!important;transform:none!important;}
.stTextInput>label,.stNumberInput>label,.stSelectbox>label{display:none!important;padding:0 10px!important;}
.stTextInput input,.stNumberInput input{background:var(--white)!important;border:1px solid var(--border)!important;border-radius:var(--r)!important;color:var(--ink)!important;font-family:var(--ff-m)!important;font-size:13px!important;padding:11px 14px!important;}
.stTextInput input:focus,.stNumberInput input:focus{border-color:#2563EB!important;box-shadow:0 0 0 3px rgba(37,99,235,0.1)!important;outline:none!important;}
[data-testid="stMetricValue"]{color:var(--ink)!important;font-family:var(--ff-d)!important;font-style:italic!important;}
[data-testid="stMetricLabel"]{color:var(--ink-3)!important;font-family:var(--ff-m)!important;font-size:10px!important;text-transform:uppercase!important;letter-spacing:1px!important;}
[data-testid="stSelectboxPopoverContainer"]{background:var(--white)!important;border:1px solid var(--border)!important;}
[data-baseweb="select"] {width:100%!important;}
[data-testid="baseButton-secondary"]{background:var(--white)!important;border:1px solid var(--border)!important;color:var(--ink)!important;}
div[data-testid="stSpinner"] p{font-family:var(--ff-m)!important;font-size:13px!important;color:var(--ink-3)!important;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SHARED NAV
# ══════════════════════════════════════════════════════════════════════════════

def top_nav(show_links=True):
    user_html = ""
    if st.session_state.gh_user:
        avatar = st.session_state.gh_avatar or ""
        img    = f'<img class="nav-avatar" src="{avatar}" />' if avatar else ""
        user_html = f'<div style="display:flex;align-items:center;gap:8px;">{img}<span class="nav-username">@{st.session_state.gh_user}</span></div>'

    links = '<div class="nav-links"><a href="#">Features</a><a href="#">How it Works</a><a href="#">Pricing</a><a href="#">Changelog</a></div>' if show_links else '<div></div>'

    right = user_html if user_html else '<button class="btn-dark">Sign up</button>'

    st.markdown(f"""
        <div class="topnav">
            <div class="nav-logo"><span class="nav-gem">◈</span> CodeSentry</div>
            {links}
            <div class="nav-actions">{right}</div>
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — LANDING
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.page == "landing":
    top_nav(show_links=True)

    st.markdown("""
        <div class="hero-wrap">
            <div class="hero-eyebrow">
                <div class="hero-dot"></div>
                Powered by Groq LLaMA 3 · Free to start
            </div>
            <div class="hero-h1 anim-hero">Your code, reviewed.<br><i>Instantly.</i></div>
            <div class="hero-sub anim-hero-delayed">
                AI-powered pull request analysis that catches bugs, security holes,
                and performance issues before they reach production.
            </div>
        </div>
    """, unsafe_allow_html=True)

    _, c2, _ = st.columns([2, 1, 2])
    with c2:
        st.markdown("""
            <style>
            .hero-btn-wrap .stButton>button{
                background:var(--ink)!important;color:white!important;border-radius:40px!important;
                font-size:15px!important;font-weight:600!important;padding:16px 36px!important;
                box-shadow:0 4px 20px rgba(15,23,42,0.18)!important;width:100%!important;
                transition:transform 0.2s,box-shadow 0.2s!important;
            }
            .hero-btn-wrap .stButton>button:hover{opacity:1!important;transform:translateY(-2px)!important;box-shadow:0 8px 30px rgba(15,23,42,0.22)!important;}
            </style>
            <div class="hero-btn-wrap anim-hero-delayed-2">
        """, unsafe_allow_html=True)
        if st.button("Connect GitHub Free", use_container_width=True, key="hero_cta"):
            st.session_state.page = "input"; st.rerun()
        st.markdown('</div><p class="hero-note anim-hero-delayed-3" style="text-align:center;">No credit card required · Setup in 60 seconds</p>', unsafe_allow_html=True)

    # Features section
    st.markdown("""
        <div class="section">
            <div class="section-label anim-fade">What we do</div>
            <div class="section-h2 anim-hero">Automated reviews,<br>zero friction</div>
            <div class="section-p anim-hero-delayed">Drop in your GitHub PR and get back a structured AI analysis in seconds — bugs, performance, security, all in one report.</div>
            <div class="feat-grid">
                <div class="feat-card">
                    <div class="feat-icon">🪲</div>
                    <div class="feat-title">Deep Bug Detection</div>
                    <div class="feat-desc">Locates complex logical fallacies and edge-case bugs before they reach your main branch.</div>
                </div>
                <div class="feat-card">
                    <div class="feat-icon">⚡</div>
                    <div class="feat-title">Performance Analysis</div>
                    <div class="feat-desc">Identifies bottlenecks, inefficient loops, and memory issues with concrete fix suggestions.</div>
                </div>
                <div class="feat-card">
                    <div class="feat-icon">🔒</div>
                    <div class="feat-title">Security Scanning</div>
                    <div class="feat-desc">Zero-trust scanning for exposed credentials, injection vulnerabilities, and insecure patterns.</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # How it works
    st.markdown("""
        <div class="how-wrap">
            <div class="section" style="padding-bottom:0;">
                <div class="section-label">Process</div>
                <div class="section-h2" style="margin-bottom:40px;">Three steps to clarity</div>
            </div>
            <div class="step-grid">
                <div class="step-card">
                    <div class="step-num">STEP 01</div>
                    <div class="step-title">Sign in with GitHub</div>
                    <div class="step-desc">One-click OAuth login connects your account securely. No passwords stored.</div>
                </div>
                <div class="step-card">
                    <div class="step-num">STEP 02</div>
                    <div class="step-title">Choose a PR</div>
                    <div class="step-desc">Enter a repo path and pick from a live list of open pull requests.</div>
                </div>
                <div class="step-card">
                    <div class="step-num">STEP 03</div>
                    <div class="step-title">Get your review</div>
                    <div class="step-desc">LLaMA 3 analyses the code delta and returns a structured, actionable report.</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Social proof numbers
    st.markdown("""
        <div class="proof-wrap">
            <div class="section-label" style="text-align:center;">By the numbers</div>
            <div class="section-h2" style="text-align:center;margin-bottom:0;">Built for scale</div>
            <div class="proof-nums">
                <div class="proof-num">
                    <div class="proof-val">12k+</div>
                    <div class="proof-lbl">PRs reviewed</div>
                </div>
                <div class="proof-num">
                    <div class="proof-val">2.4s</div>
                    <div class="proof-lbl">Avg review time</div>
                </div>
                <div class="proof-num">
                    <div class="proof-val">98%</div>
                    <div class="proof-lbl">Detection accuracy</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Pricing
    st.markdown("""
        <div class="section" style="background:var(--white);border-top:1px solid var(--border);text-align:center;">
            <div class="section-label" style="text-align:center;">Pricing</div>
            <div class="section-h2" style="text-align:center;">Simple, honest pricing</div>
            <div class="price-grid">
                <div class="price-card">
                    <div class="price-name">Developer</div>
                    <div class="price-val">Free</div>
                    <div class="price-per">forever</div>
                    <div class="price-feat"><span class="price-check">✓</span>Up to 50 reviews/month</div>
                    <div class="price-feat"><span class="price-check">✓</span>Bug, perf & security analysis</div>
                    <div class="price-feat"><span class="price-check">✓</span>Public repositories</div>
                </div>
                <div class="price-card featured">
                    <div class="price-badge">Most Popular</div>
                    <div class="price-name">Startup</div>
                    <div class="price-val">$19</div>
                    <div class="price-per">per month</div>
                    <div class="price-feat"><span class="price-check">✓</span>Unlimited reviews</div>
                    <div class="price-feat"><span class="price-check">✓</span>Private repositories</div>
                    <div class="price-feat"><span class="price-check">✓</span>Review history & analytics</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer">
            <div class="footer-brand"><span style="color:#E11D48;">◈</span> CodeSentry</div>
            <div class="footer-note">© 2026 CodeSentry · Built with Groq + FastAPI + Streamlit</div>
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — INPUT / AUTH
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.page == "input":
    top_nav(show_links=False)

    st.markdown('<div class="input-shell">', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    # If already authenticated show status
    if st.session_state.gh_user:
        avatar = st.session_state.gh_avatar or ""
        img = f'<img class="auth-avatar" src="{avatar}" />' if avatar else ""
        st.markdown(f"""
            <div class="auth-status">
                {img}
                <span class="auth-name">Signed in as @{st.session_state.gh_user}</span>
                <span class="auth-check">✓</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Not authenticated — show options
        st.markdown("""
            <div class="input-h1">Get started</div>
            <div class="input-sub">Sign in with GitHub to access private repositories, or continue with a public repo.</div>
        """, unsafe_allow_html=True)

        # GitHub OAuth button
        if GITHUB_CLIENT_ID:
            oauth_url = github_oauth_url()
            st.markdown(f"""
                <a class="btn-github" href="{oauth_url}">
                    <svg class="gh-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
                    </svg>
                    Continue with GitHub
                </a>
                <div style="margin-top:10px;text-align:center;font-size:12px;color:var(--ink-4);">
                    Grants access to repo & user info
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:#EFF4FF;border:1px solid #BFDBFE;border-radius:8px;padding:10px 12px;margin-bottom:12px;font-size:12px;color:#1e40af;"><span style="font-weight:600;">Demo Mode:</span> GitHub OAuth not configured. Set env vars to enable.</div>', unsafe_allow_html=True)

        st.markdown('<div class="input-divider" style="margin:20px 0;"></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;font-family:var(--ff-m);font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--ink-4);margin-bottom:16px;">or continue without signing in</div>', unsafe_allow_html=True)

    # Repo input
    st.markdown("""
        <div class="input-h1" style="margin-top:8px;">New Analysis</div>
        <div class="input-sub">Enter a GitHub repository and pull request number.</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="f-label">Repository Path</div>', unsafe_allow_html=True)
    repo = st.text_input(
        label="Repository",
        label_visibility="collapsed",
        placeholder="e.g. psf/requests",
        value=st.session_state.repo,
        key="repo_input_field"
    )
    st.markdown('<div class="f-hint">Format: username / repository-name</div>', unsafe_allow_html=True)

    if repo and repo != st.session_state.repo:
        st.session_state.repo = repo
        st.session_state.prs = []

    if repo and not st.session_state.get("prs"):
        with st.spinner("Loading open PRs..."):
            st.session_state.prs = fetch_prs(repo, st.session_state.gh_token)

    st.markdown('<div class="f-label" style="margin-top:18px;">Pull Request Number</div>', unsafe_allow_html=True)

    if st.session_state.prs:
        pr_options = {f"#{p['number']}  {p['title'][:40]}...": p["number"] for p in st.session_state.prs}
        selected_pr = st.selectbox(
            label="Select PR",
            options=list(pr_options.keys()),
            label_visibility="collapsed",
            key="pr_selector"
        )
        st.session_state.pr = pr_options[selected_pr]
    else:
        pr_num = st.number_input(
            label="PR Number",
            min_value=1,
            step=1,
            value=int(st.session_state.pr),
            label_visibility="collapsed",
            key="pr_manual_input"
        )
        st.session_state.pr = int(pr_num)

    st.markdown('<div class="input-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Run AI Analysis →", use_container_width=True, key="run_analysis_btn"):
            if not repo.strip():
                st.error("Please enter a repository path.")
            else:
                st.session_state.page = "results"
                st.rerun()

    with col2:
        if st.button("← Home", use_container_width=True, key="home_btn"):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)  # input-card
    st.markdown("</div>", unsafe_allow_html=True)  # input-shell




    


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.page == "results":
    repo   = st.session_state.repo
    pr_num = st.session_state.pr

    st.markdown(f"""
        <div class="results-bar">
            <div style="display:flex;align-items:center;">
                <span class="tb-pr">{repo} / pull / {pr_num}</span>
                <span class="tb-sub">· PR #{pr_num}</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <span class="tag tag-date">{datetime.now().strftime('%b %d, %Y')}</span>
                <a class="tag tag-gh" href="https://github.com/{repo}/pull/{pr_num}" target="_blank">View on GitHub ↗</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="results-wrap">', unsafe_allow_html=True)

    if st.button("← New Analysis", use_container_width=False, key="new_analysis_btn"):
        st.session_state.page = "input"
        st.session_state.result = None
        st.session_state.prs = []
        st.rerun()

    with st.spinner("Fetching diff and invoking AI model..."):
        result, err = get_review(repo, pr_num)

    if err == "conn":
        st.error("🔌 **Backend offline.** Run: `uvicorn backend.api:app --reload`")
    elif err:
        st.error(f"❌ **Error:** {err}")
    elif result:
        review  = (result or {}).get("review", {})
        bugs    = review.get("bugs", [])
        imps    = review.get("improvements", [])
        secs    = review.get("security_issues", [])
        score   = int(review.get("quality_score", 0))
        summ    = review.get("summary", "")
        sv_t, sv_c = score_meta(score)
        pct = score * 10

        if summ:
            st.markdown(f'<div class="sum-card"><div class="sum-lbl">AI Summary</div><div class="sum-body">{summ}</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
            <div class="metrics">
                <div class="metric m-sc"><div class="metric-lbl">Quality Score</div><div class="metric-val mv-sc">{score}</div><div class="metric-hint">out of 10</div></div>
                <div class="metric m-bu"><div class="metric-lbl">Bugs Found</div><div class="metric-val mv-bu">{len(bugs)}</div><div class="metric-hint">issues detected</div></div>
                <div class="metric m-pe"><div class="metric-lbl">Improvements</div><div class="metric-val mv-pe">{len(imps)}</div><div class="metric-hint">suggestions</div></div>
                <div class="metric m-se"><div class="metric-lbl">Security</div><div class="metric-val mv-se">{len(secs)}</div><div class="metric-hint">vulnerabilities</div></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([3, 3, 3, 2])
        with c1:
            st.markdown(f'<div class="sec-h"><div class="sec-title">Bugs</div><div class="sec-badge">{len(bugs)} found</div></div>{findings_html("🪲","fi-b",bugs,"bug")}', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="sec-h"><div class="sec-title">Performance</div><div class="sec-badge">{len(imps)} suggestions</div></div>{findings_html("⚡","fi-p",imps,"suggestion")}', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="sec-h"><div class="sec-title">Security</div><div class="sec-badge">{len(secs)} issues</div></div>{findings_html("🔒","fi-s",secs,"security issue")}', unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
                <div class="score-card" style="--pct:{pct};">
                    <div class="score-ring"><div class="score-inner"><div class="score-n">{score}</div></div></div>
                    <div class="score-den">/ 10 quality score</div>
                    <div class="score-v {sv_c}">{sv_t}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No review data available.")

    st.markdown("</div>", unsafe_allow_html=True)
