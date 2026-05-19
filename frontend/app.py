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

# ─── DARK APPLE CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    .stApp {
        background-color: #000000;
        color: #F5F5F7;
    }
    h1, h2, h3 {
        color: #F5F5F7 !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 1.6rem !important; }
    h3 { font-size: 1.2rem !important; }
    p, li, .stMarkdown { color: #F5F5F7; line-height: 1.6; }

    .stTextInput>div>div>input {
        background-color: #1C1C1E;
        color: #F5F5F7;
        border: 1.5px solid #38383A;
        border-radius: 12px;
        padding: 14px 18px;
        font-size: 15px;
        font-weight: 400;
        transition: all 0.2s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #007AFF;
        box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.2);
        background-color: #1C1C1E;
    }
    .stTextInput>div>div>input::placeholder { color: #8E8E93; }

    div.stButton > button {
        background: #007AFF;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 15px;
        border-radius: 12px;
        border: none;
        padding: 12px 28px;
        transition: all 0.2s ease;
        letter-spacing: -0.01em;
    }
    div.stButton > button:hover {
        background: #0066D6;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(0, 122, 255, 0.3);
    }
    div.stButton > button:active { transform: translateY(0); background: #0055B3; }

    div.stButton > button[data-testid="baseButton-secondary"] {
        background: #1C1C1E !important;
        color: #AEAEB2 !important;
        border: 1.5px solid #38383A !important;
        font-size: 13px !important;
        padding: 6px 16px !important;
        border-radius: 100px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[data-testid="baseButton-secondary"]:hover {
        background: #2C2C2E !important;
        border-color: #007AFF !important;
        color: #007AFF !important;
        transform: translateY(-1px);
        box-shadow: none !important;
    }

    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    .stSuccess {
        background: #1A3A2A !important;
        color: #30D158 !important;
        border: 1px solid #30D15844 !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
    }
    .stError {
        background: #3A1A1A !important;
        color: #FF453A !important;
        border: 1px solid #FF453A44 !important;
        border-radius: 12px !important;
    }
    .stInfo {
        background: #1C1C1E !important;
        color: #F5F5F7 !important;
        border: 1px solid #38383A !important;
        border-radius: 12px !important;
    }
    .stWarning {
        background: #3A2E1A !important;
        color: #FFD60A !important;
        border: 1px solid #FFD60A44 !important;
        border-radius: 12px !important;
    }

    .stExpander {
        background: #1C1C1E;
        border: 1.5px solid #38383A;
        border-radius: 14px;
        margin-bottom: 10px;
        overflow: hidden;
        transition: all 0.2s;
    }
    .stExpander:hover { border-color: #48484A; }
    div[data-testid="stExpander"] details summary p {
        font-weight: 600;
        color: #F5F5F7;
        font-size: 14px;
    }
    hr { border-color: #38383A !important; margin: 2rem 0 !important; }

    .section-label {
        font-size: 13px;
        font-weight: 600;
        color: #8E8E93;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    .report-card {
        background: #1C1C1E;
        border: 1px solid #38383A;
        border-radius: 14px;
        padding: 28px;
        margin-bottom: 20px;
        font-size: 14px;
        line-height: 1.7;
        color: #F5F5F7;
    }

    .badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .badge-completed { background: #1A3A2A; color: #30D158; border: 1px solid #30D15844; }
    .badge-processing { background: #1A2A3A; color: #007AFF; border: 1px solid #007AFF44; animation: pulse 1.5s infinite; }
    .badge-failed { background: #3A1A1A; color: #FF453A; border: 1px solid #FF453A44; }
    .badge-pending { background: #1C1C1E; color: #8E8E93; border: 1px solid #38383A; }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    @keyframes agentPulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(0, 122, 255, 0.3); }
        50% { box-shadow: 0 0 0 12px rgba(0, 122, 255, 0.08); }
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .agent-pipeline {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 6px;
        margin: 28px 0;
        animation: fadeUp 0.5s ease;
    }
    .agent-card {
        background: #1C1C1E;
        border: 1.5px solid #38383A;
        border-radius: 14px;
        padding: 20px 24px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        flex: 1;
        max-width: 160px;
    }
    .agent-card.pending { opacity: 0.35; border-color: #38383A; }
    .agent-card.active {
        border-color: #007AFF;
        background: #0A1A2A;
        animation: agentPulse 2s infinite;
    }
    .agent-card.done {
        border-color: #30D158;
        background: #0A1A0A;
        opacity: 1;
    }
    .agent-icon { font-size: 1.6rem; margin-bottom: 6px; }
    .agent-label { font-size: 12px; font-weight: 600; color: #8E8E93; letter-spacing: -0.01em; }
    .agent-card.active .agent-label { color: #007AFF; }
    .agent-card.done .agent-label { color: #30D158; }
    .agent-arrow { color: #48484A; font-size: 20px; font-weight: 300; flex-shrink: 0; }

    .hero-section {
        text-align: center;
        padding: 80px 20px 40px;
        animation: fadeUp 0.8s ease;
    }
    .hero-eyebrow {
        font-size: 13px;
        font-weight: 600;
        color: #007AFF;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #F5F5F7;
        margin-bottom: 16px;
        line-height: 1.1;
    }
    .hero-title span {
        background: linear-gradient(135deg, #007AFF, #30D158);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        font-size: 1.15rem;
        color: #8E8E93;
        max-width: 620px;
        margin: 0 auto 36px;
        line-height: 1.6;
        font-weight: 400;
    }

    .feature-grid {
        display: flex;
        gap: 16px;
        margin: 32px 0;
        animation: fadeUp 0.6s ease;
    }
    .feature-card {
        background: #1C1C1E;
        border-radius: 18px;
        padding: 28px 24px;
        transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        flex: 1;
        border: 1px solid #38383A;
    }
    .feature-card:hover {
        background: #2C2C2E;
        border-color: #48484A;
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    .feature-icon { font-size: 2rem; margin-bottom: 14px; }
    .feature-title { font-weight: 700; color: #F5F5F7; margin-bottom: 8px; font-size: 1.05rem; }
    .feature-desc { color: #AEAEB2; font-size: 0.88rem; line-height: 1.6; font-weight: 400; }

    .tech-badge {
        display: inline-block;
        background: #1C1C1E;
        border: 1px solid #38383A;
        border-radius: 100px;
        padding: 8px 20px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
        color: #F5F5F7;
        transition: all 0.2s;
    }
    .tech-badge:hover {
        border-color: #007AFF;
        color: #007AFF;
        background: #0A1A2A;
    }

    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0 8px;
    }
    .nav-brand {
        font-size: 1.2rem;
        font-weight: 700;
        color: #F5F5F7;
        letter-spacing: -0.02em;
    }

    .mermaid-wrapper {
        background: #1C1C1E;
        border-radius: 18px;
        padding: 24px;
        border: 1px solid #38383A;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─── LANDING PAGE ───
if "show_landing" not in st.session_state:
    st.session_state.show_landing = True

if st.session_state.show_landing:
    st.markdown("<div class='hero-section'>", unsafe_allow_html=True)
    st.markdown("<div class='hero-eyebrow'>Multi-Agent OSINT Platform</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-title'>Threat Intelligence,<br><span>Automated</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-sub'>An autonomous system of AI agents that scouts threat feeds, cross-verifies findings, and generates structured Diamond Model reports — all from a single query.</div>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("Get Started", use_container_width=True):
            st.session_state.show_landing = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#38383A;margin:32px 0;'>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>How It Works</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-grid'><div class='feature-card'><div class='feature-icon'>🔍</div><div class='feature-title'>Scout Agent</div><div class='feature-desc'>Searches live threat intelligence feeds via Tavily. Extracts IOCs, active campaigns, CVEs, and TTPs with source citations.</div></div><div class='feature-card'><div class='feature-icon'>✅</div><div class='feature-title'>Critic Agent</div><div class='feature-desc'>Applies the Two-Source Rule — cross-references every finding across independent sources before accepting as verified intelligence.</div></div><div class='feature-card'><div class='feature-icon'>📝</div><div class='feature-title'>Reporter Agent</div><div class='feature-desc'>Generates a Diamond Model report with CWE mappings, MITRE ATT&CK tactics, and prioritized remediation.</div></div></div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#38383A;margin:32px 0;'>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Architecture</div>", unsafe_allow_html=True)
    st.markdown("<div class='mermaid-wrapper'>", unsafe_allow_html=True)
    st.markdown("""
```mermaid
graph LR
    U[User Query] --> A[Query Parser]
    A --> S[Scout Agent]
    S --> C[Critic Agent]
    C -->|Unverified · Retry| S
    C -->|Verified| R[Reporter Agent]
    R --> D[Diamond Model Report]
```
""")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Powered By</div>", unsafe_allow_html=True)
    techs = ["Gemini 2.0 Flash", "Tavily API", "FastAPI", "PostgreSQL", "Redis", "Celery", "Streamlit", "Docker"]
    html = "<div style='text-align:center;padding:8px 0 24px;'>" + " ".join(f"<span class='tech-badge'>{t}</span>" for t in techs) + "</div>"
    st.markdown(html, unsafe_allow_html=True)

else:
    # ─── MAIN APP (no auth) ───
    st.markdown("<div class='nav-bar'><span class='nav-brand'>Agentic Threat Intel</span></div>", unsafe_allow_html=True)

    if st.button("About", use_container_width=True):
        st.session_state.show_landing = True
        st.rerun()

    st.markdown("<hr style='border-color:#38383A;margin:16px 0;'>", unsafe_allow_html=True)

    # ─── NEW HUNT ───
    st.markdown("<div class='section-label'>New Intelligence Hunt</div>", unsafe_allow_html=True)

    if "example_query" not in st.session_state:
        st.session_state.example_query = ""

    examples = [
        "Latest ransomware threats targeting healthcare in 2025",
        "APT groups using AI-driven phishing against finance",
        "Zero-day vulnerabilities in cloud infrastructure — energy sector",
        "Supply chain attacks on DevOps pipelines and IOCs",
        "State-sponsored actors targeting NATO critical infrastructure",
        "Emerging IoT botnet threats in manufacturing",
        "Ransomware-as-a-Service groups targeting education",
        "Deepfake social engineering targeting corporate executives",
        "5G network infrastructure threats from APTs",
        "Cyber-espionage campaigns against defense contractors",
    ]

    for i in range(0, len(examples), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(examples):
                with cols[j]:
                    if st.button(examples[i + j], key=f"ex_{i + j}", use_container_width=True, type="secondary"):
                        st.session_state.example_query = examples[i + j]
                        st.rerun()

    query = st.text_input("", value=st.session_state.example_query, placeholder="Describe the threat intelligence you want to investigate...", label_visibility="collapsed")

    col_run, col_clear = st.columns([3, 1])
    with col_run:
        run_clicked = st.button("Initialize Agents", use_container_width=True)
    with col_clear:
        if st.button("Clear", use_container_width=True):
            st.session_state.example_query = ""
            st.rerun()

    if run_clicked:
        if query:
            with st.spinner("Dispatching agents..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/api/v1/run_osint", json={"query": query})
                    if res.status_code == 200:
                        st.success("Agents dispatched — monitoring pipeline")
                        report_id = res.json()["id"]

                        pipeline_placeholder = st.empty()
                        phase_statuses = {
                            "parsing": {"label": "Parsing", "icon": "🔎"},
                            "scouting": {"label": "Scout", "icon": "🔍"},
                            "critiquing": {"label": "Critic", "icon": "✅"},
                            "reporting": {"label": "Reporter", "icon": "📝"},
                        }
                        phase_order = ["parsing", "scouting", "critiquing", "reporting"]

                        status = "pending"
                        phase = "pending"
                        placeholder = st.empty()

                        while status in ["pending", "processing"]:
                            time.sleep(2)
                            status_res = requests.get(f"{BACKEND_URL}/api/v1/reports")
                            if status_res.status_code == 200:
                                reports = status_res.json()
                                for r in reports:
                                    if r["id"] == report_id:
                                        status = r["status"]
                                        phase = r.get("phase", "pending")

                                        with pipeline_placeholder.container():
                                            html = "<div class='agent-pipeline'>"
                                            for i, p in enumerate(phase_order):
                                                if status == "completed":
                                                    cls, icon, label = "done", phase_statuses[p]["icon"], phase_statuses[p]["label"]
                                                elif status == "failed":
                                                    cls, icon, label = "pending", phase_statuses[p]["icon"], phase_statuses[p]["label"]
                                                else:
                                                    is_active = phase == p
                                                    is_done = False
                                                    try:
                                                        is_done = phase_order.index(phase) > i
                                                    except ValueError:
                                                        pass
                                                    cls = "done" if is_done else ("active" if is_active else "pending")
                                                    icon = phase_statuses[p]["icon"]
                                                    label = phase_statuses[p]["label"]
                                                html += f"<div class='agent-card {cls}'><div class='agent-icon'>{icon}</div><div class='agent-label'>{label}</div></div>"
                                                if i < len(phase_order) - 1:
                                                    html += "<div class='agent-arrow'>→</div>"
                                            html += "</div>"
                                            st.markdown(html, unsafe_allow_html=True)

                                        if status == "completed":
                                            pipeline_placeholder.empty()
                                            placeholder.empty()
                                            st.markdown("<div class='section-label' style='margin-top:24px;'>Threat Intelligence Report</div>", unsafe_allow_html=True)
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
                                                "scouting": "Scout is gathering OSINT data from threat feeds...",
                                                "critiquing": "Critic is verifying findings using the Two-Source Rule...",
                                                "reporting": "Reporter is compiling the Diamond Model report...",
                                            }
                                            placeholder.info(placed.get(phase, "Processing..."))
                                        break
                            else:
                                st.error(f"Failed to start: {res.text}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
        else:
            st.warning("Please enter a query.")

    st.markdown("<hr style='border-color:#38383A;margin:24px 0;'>", unsafe_allow_html=True)

    # ─── REPORT HISTORY ───
    st.markdown("<div class='section-label'>Intelligence Reports</div>", unsafe_allow_html=True)
    if st.button("Refresh", use_container_width=True):
        try:
            res = requests.get(f"{BACKEND_URL}/api/v1/reports/demo")
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
                    with st.expander(f"{r['query']}  {badge}"):
                        st.caption(f"Phase: {phase}  •  Task ID: {r.get('task_id', 'N/A')}")
                        if r["findings"]:
                            st.markdown(f"<div class='report-card'>{r['findings']}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='color:#8E8E93;font-size:14px;'>No findings yet.</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("Could not load history.")
