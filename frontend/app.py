import streamlit as st
import requests
import time
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(
    page_title="Agentic Threat Intel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── DARK CYBER CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background-color: #08080E;
        background-image:
            radial-gradient(ellipse at 20% 50%, rgba(0, 255, 204, 0.03) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(0, 100, 255, 0.03) 0%, transparent 50%);
        color: #E0E0E0;
    }
    h1, h2, h3 { color: #00FFCC !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    h1 { font-size: 2.8rem !important; }
    h2 { font-size: 1.8rem !important; }
    .stTextInput>div>div>input {
        background-color: #12121A;
        color: #00FFCC;
        border: 1px solid #00FFCC44;
        border-radius: 10px;
        padding: 12px 16px;
        font-family: 'JetBrains Mono', monospace;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #00FFCC;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.15);
    }
    .stButton>button {
        background: linear-gradient(135deg, #00FFCC, #00CCAA);
        color: #08080E;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        padding: 8px 24px;
        transition: all 0.3s ease;
        letter-spacing: 0.01em;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 255, 204, 0.35);
    }
    .stButton>button:active { transform: translateY(0); }
    .stRadio>div { gap: 8px; }
    .stRadio label {
        background: #12121A;
        border: 1px solid #00FFCC22;
        border-radius: 8px;
        padding: 8px 16px;
        color: #888;
        transition: all 0.2s;
    }
    .stRadio label:hover { border-color: #00FFCC66; color: #ccc; }
    .stRadio [data-testid="stMarkdownContainer"] p { font-size: 14px; }
    header { visibility: hidden; }
    .stSuccess {
        background: rgba(0, 255, 204, 0.08) !important;
        color: #00FFCC !important;
        border: 1px solid #00FFCC44 !important;
        border-radius: 8px !important;
    }
    .stError {
        background: rgba(255, 51, 102, 0.08) !important;
        color: #FF3366 !important;
        border: 1px solid #FF336644 !important;
        border-radius: 8px !important;
    }
    .stInfo {
        background: rgba(0, 150, 255, 0.08) !important;
        color: #00AAFF !important;
        border: 1px solid #00AAFF44 !important;
        border-radius: 8px !important;
    }
    .stWarning {
        background: rgba(255, 200, 0, 0.08) !important;
        color: #FFCC00 !important;
        border: 1px solid #FFCC0044 !important;
        border-radius: 8px !important;
    }
    .stMarkdown { font-family: 'Inter', sans-serif; line-height: 1.7; }
    .stExpander {
        background: #12121A;
        border: 1px solid #00FFCC22;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    .stExpander:hover { border-color: #00FFCC44; }
    div[data-testid="stExpander"] details summary p {
        font-weight: 600;
        color: #00FFCC;
    }
    hr { border-color: #00FFCC22 !important; }
    .report-card {
        background: linear-gradient(135deg, #12121A, #0E0E16);
        border: 1px solid #00FFCC22;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .badge-completed { background: rgba(0, 255, 204, 0.15); color: #00FFCC; border: 1px solid #00FFCC44; }
    .badge-processing { background: rgba(0, 150, 255, 0.15); color: #00AAFF; border: 1px solid #00AAFF44; animation: pulse 1.5s infinite; }
    .badge-failed { background: rgba(255, 51, 102, 0.15); color: #FF3366; border: 1px solid #FF336644; }
    .badge-pending { background: rgba(255, 200, 0, 0.15); color: #FFCC00; border: 1px solid #FFCC0044; }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(0, 255, 204, 0.2); }
        50% { box-shadow: 0 0 25px rgba(0, 255, 204, 0.5); }
    }
    .agent-card {
        background: #12121A;
        border: 1px solid #00FFCC22;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .agent-card.active {
        border-color: #00FFCC;
        animation: glow 1.5s infinite;
    }
    .agent-card.done { border-color: #00FFCC88; }
    .agent-card.pending { border-color: #333; opacity: 0.5; }
    .agent-icon { font-size: 2rem; margin-bottom: 8px; }
    .agent-label { font-size: 14px; font-weight: 600; color: #888; }
    .agent-card.active .agent-label { color: #00FFCC; }
    .agent-card.done .agent-label { color: #00FFCCAA; }
    .hero-section {
        text-align: center;
        padding: 60px 20px 40px;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00FFCC, #00AAFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #888;
        max-width: 600px;
        margin: 0 auto 32px;
        line-height: 1.6;
    }
    .feature-card {
        background: linear-gradient(135deg, #12121A, #0E0E16);
        border: 1px solid #00FFCC22;
        border-radius: 12px;
        padding: 24px;
        transition: all 0.3s;
        height: 100%;
    }
    .feature-card:hover { border-color: #00FFCC44; transform: translateY(-4px); }
    .feature-icon { font-size: 2.2rem; margin-bottom: 12px; }
    .feature-title { font-weight: 700; color: #00FFCC; margin-bottom: 8px; font-size: 1.1rem; }
    .feature-desc { color: #999; font-size: 0.9rem; line-height: 1.6; }
    .tech-badge {
        display: inline-block;
        background: #12121A;
        border: 1px solid #333;
        border-radius: 20px;
        padding: 6px 16px;
        margin: 4px;
        font-size: 13px;
        color: #aaa;
        transition: all 0.2s;
    }
    .tech-badge:hover { border-color: #00FFCC44; color: #00FFCC; }
    div.stButton > button[data-testid="baseButton-secondary"] {
        background: transparent !important;
        border: 1px solid #00FFCC33 !important;
        color: #aaa !important;
        font-size: 13px !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
        transition: all 0.2s ease !important;
        font-weight: 400 !important;
    }
    div.stButton > button[data-testid="baseButton-secondary"]:hover {
        border-color: #00FFCC !important;
        color: #00FFCC !important;
        background: rgba(0, 255, 204, 0.05) !important;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ───
if "username" not in st.session_state:
    st.session_state.username = None
if "show_landing" not in st.session_state:
    st.session_state.show_landing = True

# ─── AUTH HELPERS ───
def login_user(username, password):
    try:
        res = requests.post(f"{BACKEND_URL}/api/v1/login", json={"username": username, "password": password})
        if res.status_code == 200:
            st.session_state.username = username
            st.session_state.show_landing = False
            st.rerun()
        else:
            st.error("Invalid credentials.")
    except Exception as e:
        st.error(f"Connection error: {e}")

def signup_user(username, password):
    try:
        res = requests.post(f"{BACKEND_URL}/api/v1/signup", json={"username": username, "password": password})
        if res.status_code == 200:
            st.success("Signup successful! Please log in.")
        else:
            st.error(f"Signup failed: {res.json().get('detail')}")
    except Exception as e:
        st.error(f"Connection error: {e}")

# ─── LANDING PAGE ───
if st.session_state.show_landing and not st.session_state.username:
    st.markdown("<div class='hero-section'>", unsafe_allow_html=True)
    st.markdown("<div class='hero-title'>🛡️ Agentic Threat Intel</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-sub'>An autonomous multi-agent OSINT workflow that scouts, verifies, and reports on cyber threats — powered by Gemini AI and real-time threat intelligence.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class='feature-card'><div class='feature-icon'>🔍</div><div class='feature-title'>Scout Agent</div><div class='feature-desc'>Searches live threat intel via Tavily API, extracts IOCs, TTPs, and active campaigns with source citations.</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='feature-card'><div class='feature-icon'>✅</div><div class='feature-title'>Critic Agent</div><div class='feature-desc'>Applies the Two-Source Rule — cross-references findings across independent sources before accepting as verified.</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='feature-card'><div class='feature-icon'>📝</div><div class='feature-title'>Reporter Agent</div><div class='feature-desc'>Generates a Diamond Model threat report with CWE mappings, MITRE ATT&CK tactics, and prioritized remediation.</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🏗️ Architecture")
    st.markdown("""
```mermaid
graph LR
    U[User Query] --> A[Query Parser]
    A --> S[🔍 Scout Agent]
    S --> C[✅ Critic Agent]
    C -->|Unverified & retries < 2| S
    C -->|Verified| R[📝 Reporter Agent]
    R --> D[📊 Diamond Model Report]
    style U fill:#12121A,stroke:#00FFCC,color:#00FFCC
    style A fill:#12121A,stroke:#00FFCC,color:#00FFCC
    style S fill:#12121A,stroke:#00FFCC,color:#00FFCC
    style C fill:#12121A,stroke:#FFCC00,color:#FFCC00
    style R fill:#12121A,stroke:#00FFCC,color:#00FFCC
    style D fill:#12121A,stroke:#00FFCC,color:#00FFCC
```
""")

    st.markdown("### 🛠️ Tech Stack")
    techs = ["Gemini 2.0 Flash", "Tavily API", "FastAPI", "PostgreSQL", "Redis", "Celery", "Streamlit", "Docker", "Python 3.11"]
    html = "<div style='text-align:center;'>" + " ".join(f"<span class='tech-badge'>{t}</span>" for t in techs) + "</div>"
    st.markdown(html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.show_landing = False
            st.rerun()

    st.markdown("---")
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown("**Already have an account?**")
    with col_r:
        if st.button("Sign In", use_container_width=True):
            st.session_state.show_landing = False
            st.rerun()
    st.markdown("<br><br>", unsafe_allow_html=True)

else:
    # ─── AUTH / MAIN APP ───
    if not st.session_state.username:
        st.markdown("<h2 style='text-align:center;margin-top:40px;'>🛡️ Agentic Threat Intel</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#888;margin-bottom:32px;'>Sign in or create an account</p>", unsafe_allow_html=True)

        col_l, col_m, col_r = st.columns([1, 2, 1])
        with col_m:
            auth_mode = st.radio("", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
            u_input = st.text_input("Username", placeholder="Enter your username")
            p_input = st.text_input("Password", type="password", placeholder="Enter your password")

            if st.button("Submit", use_container_width=True):
                if u_input and p_input:
                    if auth_mode == "Login":
                        login_user(u_input, p_input)
                    else:
                        signup_user(u_input, p_input)
                else:
                    st.warning("Please fill in both fields.")

    else:
        # ─── MAIN APP ───
        st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'><span style='font-size:1.5rem;font-weight:700;color:#00FFCC;'>🛡️ Agentic Threat Intel</span><span style='color:#888;font-size:14px;'>Welcome, <strong style='color:#00FFCC;'>{st.session_state.username}</strong></span></div>", unsafe_allow_html=True)

        col_logout, col_landing = st.columns([1, 1])
        with col_logout:
            if st.button("Logout", use_container_width=True):
                st.session_state.username = None
                st.rerun()
        with col_landing:
            if st.button("About", use_container_width=True):
                st.session_state.show_landing = True
                st.rerun()

        st.markdown("---")

        # ─── NEW HUNT ───
        st.subheader("🔍 New OSINT Hunt")

        # Example query chips
        if "example_query" not in st.session_state:
            st.session_state.example_query = ""

        examples = [
            "What are the latest ransomware threats targeting healthcare in 2025?",
            "APT groups using AI-driven phishing campaigns against the finance sector",
            "Zero-day vulnerabilities in cloud infrastructure targeting energy companies",
            "Supply chain attacks on DevOps pipelines — recent campaigns and IOCs",
            "State-sponsored threat actors targeting critical infrastructure in NATO countries",
            "Emerging IoT botnet threats in the manufacturing sector",
            "Ransomware-as-a-Service groups active against education institutions",
            "Social engineering trends using deepfake audio against corporate executives",
            "Threats to 5G network infrastructure from advanced persistent threats",
            "Cyber-espionage campaigns targeting defense contractors in 2025",
        ]

        chips_cols = st.columns(2)
        for i, ex in enumerate(examples):
            with chips_cols[i % 2]:
                if st.button(ex, key=f"ex_{i}", use_container_width=True, type="secondary"):
                    st.session_state.example_query = ex
                    st.rerun()

        query = st.text_input("", value=st.session_state.example_query, placeholder="e.g. What are the latest ransomware threats targeting healthcare in 2025?", label_visibility="collapsed")

        col_run, col_clear = st.columns([3, 1])
        with col_run:
            run_clicked = st.button("🚀 Initialize Agents", use_container_width=True, type="primary")
        with col_clear:
            if st.button("✕ Clear", use_container_width=True):
                st.session_state.example_query = ""
                st.rerun()

        if run_clicked:
            if query:
                with st.spinner("Dispatching agents..."):
                    try:
                        res = requests.post(f"{BACKEND_URL}/api/v1/run_osint", json={
                            "username": st.session_state.username,
                            "query": query
                        })
                        if res.status_code == 200:
                            st.success("Agents dispatched! Monitoring pipeline...")
                            report_id = res.json()["id"]

                            # ─── AGENT PIPELINE VISUALIZATION ───
                            pipeline_placeholder = st.empty()
                            phase_statuses = {
                                "parsing": {"label": "Parsing Query", "icon": "🔎", "done": False},
                                "scouting": {"label": "Scout Agent", "icon": "🔍", "done": False},
                                "critiquing": {"label": "Critic Agent", "icon": "✅", "done": False},
                                "reporting": {"label": "Reporter Agent", "icon": "📝", "done": False},
                            }
                            phase_order = ["parsing", "scouting", "critiquing", "reporting"]

                            status = "pending"
                            phase = "pending"
                            placeholder = st.empty()

                            while status in ["pending", "processing"]:
                                time.sleep(2)
                                status_res = requests.get(f"{BACKEND_URL}/api/v1/reports/{st.session_state.username}")
                                if status_res.status_code == 200:
                                    reports = status_res.json()
                                    for r in reports:
                                        if r["id"] == report_id:
                                            status = r["status"]
                                            phase = r.get("phase", "pending")

                                            # Render pipeline
                                            with pipeline_placeholder.container():
                                                cols = st.columns(len(phase_order))
                                                for i, p in enumerate(phase_order):
                                                    if status == "completed":
                                                        is_done = True
                                                        is_active = False
                                                    elif status == "failed":
                                                        is_done = False
                                                        is_active = False
                                                    else:
                                                        is_active = phase == p
                                                        try:
                                                            is_done = phase_order.index(phase) > i
                                                        except ValueError:
                                                            is_done = False

                                                    cls = "done" if is_done else ("active" if is_active else "pending")
                                                    icon = phase_statuses[p]["icon"]
                                                    label = phase_statuses[p]["label"]
                                                    with cols[i]:
                                                        st.markdown(f"<div class='agent-card {cls}'><div class='agent-icon'>{icon}</div><div class='agent-label'>{label}</div></div>", unsafe_allow_html=True)

                                            if status == "completed":
                                                placeholder.empty()
                                                pipeline_placeholder.empty()
                                                st.markdown("### 📊 Threat Intelligence Report")
                                                st.markdown(f"<div class='report-card'>{r['findings']}</div>", unsafe_allow_html=True)
                                                break
                                            elif status == "failed":
                                                pipeline_placeholder.empty()
                                                placeholder.error("Agent workflow failed.")
                                                st.error(r.get("findings", "Unknown error"))
                                                break
                                            else:
                                                placed = {
                                                    "parsing": "Parsing your query...",
                                                    "scouting": "🔍 Scout is gathering OSINT data from threat feeds...",
                                                    "critiquing": "✅ Critic is verifying findings using the Two-Source Rule...",
                                                    "reporting": "📝 Reporter is compiling the Diamond Model report..."
                                                }
                                                placeholder.info(placed.get(phase, "Processing..."))
                                            break
                            else:
                                st.error(f"Failed to start: {res.text}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
            else:
                st.warning("Please enter a query.")

        st.markdown("---")

        # ─── REPORT HISTORY ───
        st.subheader("📁 Intelligence Reports")
        if st.button("Refresh History", use_container_width=True):
            try:
                res = requests.get(f"{BACKEND_URL}/api/v1/reports/{st.session_state.username}")
                if res.status_code == 200:
                    reports = res.json()
                    for r in reports:
                        badge_class = {
                            "completed": "badge-completed",
                            "processing": "badge-processing",
                            "failed": "badge-failed",
                            "pending": "badge-pending"
                        }.get(r["status"], "badge-pending")
                        badge = f"<span class='badge {badge_class}'>{r['status'].upper()}</span>"
                        phase = r.get("phase", r["status"]).capitalize()
                        with st.expander(f"Query: {r['query']} {badge}"):
                            st.caption(f"Phase: {phase}  •  Task ID: {r.get('task_id', 'N/A')}")
                            if r["findings"]:
                                st.markdown(f"<div class='report-card'>{r['findings']}</div>", unsafe_allow_html=True)
                            else:
                                st.write("No findings yet.")
            except Exception as e:
                st.error("Could not load history.")
