import streamlit as st
import json
import os
import tempfile
import uuid
from datetime import datetime
from html import escape
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from agent.graph import create_agent_graph
from agent.audit import log_override
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from resume_model.text_extract import extract_text_and_links

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexHire AI | Agentic Screener",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Geist:wght@400;500;600;700&display=swap');

:root {
    --primary: #ffffff;
    --bg-dark: #000000;
    --card-bg: #09090b;
    --card-border: #27272a;
    --text-main: #fafafa;
    --text-muted: #a1a1aa;
    --hire-color: #10b981;
}

.stApp {
    background-color: var(--bg-dark);
    color: var(--text-main);
    font-family: 'Geist', sans-serif;
    letter-spacing: -0.01em;
}

/* Grid background effect mimicking pure pro layout */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMSIgY3k9IjEiIHI9IjEiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4wNCkiLz48L3N2Zz4=');
    pointer-events: none;
    z-index: 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #09090b !important;
    border-right: 1px solid var(--card-border);
}

/* Hide headers and standard menu */
[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

h1, h2, h3, h4 {
    font-family: 'Geist', sans-serif;
    font-weight: 600;
    letter-spacing: -0.02em;
}

.hero-container {
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid var(--card-border);
    margin-bottom: 3rem;
    position: relative;
    z-index: 1;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: transparent;
    border: 1px solid var(--card-border);
    color: var(--text-muted);
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
    margin: 0 0 0.5rem;
    letter-spacing: -0.03em;
}

.hero-subtitle {
    color: var(--text-muted);
    font-size: 1rem;
    font-weight: 400;
    max-width: 600px;
    margin: 0;
}

/* Uploader Strict styling */
div[data-testid="stFileUploadDropzone"] {
    background: var(--bg-dark) !important;
    border: 1px dashed var(--card-border) !important;
    border-radius: 8px !important;
}
div[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--text-muted) !important;
}

/* Strict Button */
div.stButton > button {
    background: white !important;
    color: black !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1rem !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    width: 100% !important;
    transition: opacity 0.1s ease !important;
}
div.stButton > button:hover {
    opacity: 0.9 !important;
}

/* Clean Pro Grid Matrix */
.candidate-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid var(--card-border);
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.candidate-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: white;
    margin: 0 0 4px;
    font-family: 'Geist Mono', monospace;
}

.status-badge {
    display: inline-flex;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    border: 1px solid var(--card-border);
    background: rgba(255,255,255,0.05);
}
.status-hire { color: #10b981; border-color: rgba(16, 185, 129, 0.3); }
.status-maybe { color: #f59e0b; border-color: rgba(245, 158, 11, 0.3); }

.score-container {
    text-align: right;
}
.score-main {
    font-family: 'Geist Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
}

.summary-text {
    color: #d4d4d8;
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
    line-height: 1.5;
}

.metrics-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1px;
    background: var(--card-border);
    border: 1px solid var(--card-border);
    border-radius: 6px;
    overflow: hidden;
}

.metric-item {
    background: var(--card-bg);
    padding: 0.75rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.8rem;
}

.metric-label {
    color: var(--text-muted);
    font-weight: 500;
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
}
.metric-val {
    font-weight: 600;
    color: white;
    font-family: 'Geist Mono', monospace;
}

.metric-justification {
    display: none; /* Hidden in dense mode */
}

.prog-bar-bg { display: none; } /* Simplified */
</style>
""", unsafe_allow_html=True)

# ── Sidebar Configurations ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <h2 style='margin-bottom:0.5rem;'>⚡ Engine Config</h2>
    <p style='font-size:0.85rem; color:#94a3b8; margin-bottom:1.5rem;'>Configure your API integrations here.</p>
    """, unsafe_allow_html=True)
    
    api_key_input = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Required to run text extraction and grading."
    )
    
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
    
    st.markdown("---")
    st.markdown("""
    ### Talent Pool Index
    The vector store was pre-cached. 
    Active Entries: **Indexed Resumes**
    """)
    
    st.info("💡 Tip: If no resumes are uploaded, the system intelligently falls back to the internal talent pool search.")

# ── Init Agent ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_agent():
    return create_agent_graph()

agent = get_agent()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# ── Helper functions ──────────────────────────────────────────────────────────

def get_rec_styles(rec):
    if rec == "Hire": return "status-hire", "score-hire"
    if rec == "Maybe": return "status-maybe", "score-maybe"
    return "status-nohire", "score-nohire"

def generate_report(candidates):
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('report.html')
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return template.render(candidates=candidates, date=date_str)

# ── UI Layout ─────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-container">
    <div class="hero-badge">System Operational</div>
    <h1 class="hero-title">NexHire AI</h1>
    <p class="hero-subtitle">Direct execution panel for semantic deep audits utilizing standard state machines.</p>
</div>
""", unsafe_allow_html=True)

# Main action box (Uploader area)
st.markdown("""
<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); border-radius:20px; padding:2rem; margin-bottom:2.5rem;">
    <h3 style="margin-top:0; margin-bottom:1.5rem; color:white; display:flex; align-items:center; gap:10px;">📥 Upload Submissions</h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Job Description**")
    jd_file = st.file_uploader("Drop job requirements (.txt, .pdf)", type=["txt", "pdf"], label_visibility="collapsed")
    
with col2:
    st.markdown("**Resumes**")
    resume_files = st.file_uploader("Drop PDFs or DOCX files", type=["pdf", "docx"], accept_multiple_files=True, label_visibility="collapsed")
    
with col3:
    st.markdown("**LinkedIn Data**")
    linkedin_files = st.file_uploader("Drop exported JSONs", type=["json"], accept_multiple_files=True, label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 1, 1])

with btn_col:
    trigger_btn = st.button("🚀 Analyze & Rank Talent")

if trigger_btn:
    if not jd_file:
        st.warning("⚠️ Please upload a Job Description to proceed.")
        st.stop()
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ API KEY MISSING: Please enter your Google Gemini API Key in the sidebar to continue.")
        st.stop()
        
    with st.status("🕵️ Agent working behind the scenes...", expanded=True) as status:
        # Save files to temp
        temp_dir = tempfile.mkdtemp()
        paths = []
        all_files = (resume_files or []) + (linkedin_files or [])
        for f in all_files:
            path = os.path.join(temp_dir, f.name)
            with open(path, "wb") as out:
                out.write(f.read())
            paths.append(path)
            
        jd_temp_path = os.path.join(temp_dir, f"JD_{jd_file.name}")
        with open(jd_temp_path, "wb") as f:
            f.write(jd_file.getvalue())
            
        try:
            jd_text, _ = extract_text_and_links(jd_temp_path)
        except Exception as ex:
            # Fallback
            try:
                jd_text = jd_file.read().decode("utf-8")
            except:
                st.error(f"Error extracting JD text: {ex}")
                st.stop()
        
        initial_state = {
            "jd_text": jd_text,
            "uploaded_file_paths": paths,
            "search_triggered": False,
            "all_candidates": [],
            "scored_candidates": []
        }
        
        # Invoke agent
        for event in agent.stream(initial_state, config):
            for k, v in event.items():
                st.write(f"✅ Step **{k}** executed.")
                if v and "error" in v:
                    st.error(f"Error during agent workflow: {v['error']}")
                    st.stop()
                
                if k == "score_candidates":
                    current_state = agent.get_state(config).values
                    if not current_state.get("has_strong_fit", False) and not current_state.get("search_triggered", False):
                        st.info("🔍 No direct matches above threshold in upload list. Activating Talent Pool Neural Search.", icon="⚡")
        
        status.update(label="Analysis Complete!", state="complete", expanded=False)
        st.session_state.agent_state = agent.get_state(config).values
        st.toast("Analysis successful! Scroll down for human review.", icon="🎉")

# ── HIL Review UI ─────────────────────────────────────────────────────────────

if "agent_state" in st.session_state:
    state = st.session_state.agent_state
    scored = state.get("scored_candidates", [])
    
    st.markdown("""
    <div style="margin: 3rem 0 2rem;">
        <h2 style="font-size:2rem; margin-bottom:0.5rem;">🔬 Decision Intelligence View</h2>
        <p style="color:#94a3b8;">Review and refine evaluation rubrics using human-in-the-loop overrides.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render candidates
    for i, c in enumerate(scored):
        rec = c.get("recommendation", "No Hire")
        status_cls, score_cls = get_rec_styles(rec)
        
        dims = c.get("dimensions", {})
        
        # Map dimensions and safely get numbers
        def get_safe(d_key): return dims.get(d_key, {}).get('score', 0)
        def get_pct(val): return (val / 10.0) * 100
        
        sk = get_safe('skills_match')
        ex = get_safe('experience_relevance')
        ed = get_safe('education_certs')
        pr = get_safe('project_portfolio')
        cm = get_safe('communication_quality')

        st.markdown(f"""
        <div class="candidate-card">
            <div class="card-header">
                <div>
                    <h2 class="candidate-name">{escape(c.get('candidate_id'))}</h2>
                    <span class="status-badge {status_cls}">{rec}</span>
                </div>
                <div class="score-container">
                    <div class="score-main {score_cls}">{c.get('weighted_total', 0):.2f}</div>
                    <div style="font-size:0.75rem; color:#94a3b8; font-weight:500; margin-top:4px; text-transform:uppercase; letter-spacing:1px;">Normalized Score / 10</div>
                </div>
            </div>
            
            <div class="summary-text">{escape(c.get('summary', ''))}</div>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <span class="metric-label">Skills Match (30%)</span>
                    <span class="metric-val">{sk} / 10</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Relevance (25%)</span>
                    <span class="metric-val">{ex} / 10</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Education (15%)</span>
                    <span class="metric-val">{ed} / 10</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Projects (20%)</span>
                    <span class="metric-val">{pr} / 10</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Communication (10%)</span>
                    <span class="metric-val">{cm} / 10</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Override Expander styled with streamlit native expander inside the iterative loop
        with st.expander(f"🛠️ Modify Assessment Scores: {c.get('candidate_id')}"):
            with st.form(key=f"form_{i}"):
                st.markdown("#### Override Weights")
                colA, colB, colC = st.columns(3)
                s1 = colA.slider("Skills Match", 0, 10, get_safe('skills_match'), key=f"s1_{i}")
                s2 = colB.slider("Experience", 0, 10, get_safe('experience_relevance'), key=f"s2_{i}")
                s3 = colC.slider("Education", 0, 10, get_safe('education_certs'), key=f"s3_{i}")
                
                colD, colE, _ = st.columns(3)
                s4 = colD.slider("Projects", 0, 10, get_safe('project_portfolio'), key=f"s4_{i}")
                s5 = colE.slider("Communication", 0, 10, get_safe('communication_quality'), key=f"s5_{i}")
                
                reason = st.text_area("Audit Logging: Reason for override", placeholder="e.g., Spoke to candidate, confirmed AWS certification not on resume...", key=f"reason_{i}")
                
                st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
                submit = st.form_submit_button("Confirm Overrides")
                
                if submit:
                    if not reason.strip():
                        st.error("Mandatory: Please log a reason for change.")
                    else:
                        log_override(st.session_state.thread_id, c.get('candidate_id'), "skills_match", dims['skills_match']['score'], dims['skills_match']['justification'], s1, reason)
                        
                        dims['skills_match']['score'] = s1
                        dims['experience_relevance']['score'] = s2
                        dims['education_certs']['score'] = s3
                        dims['project_portfolio']['score'] = s4
                        dims['communication_quality']['score'] = s5
                        
                        w_tot = (s1*0.3) + (s2*0.25) + (s3*0.15) + (s4*0.2) + (s5*0.1)
                        c['weighted_total'] = w_tot
                        if w_tot >= 7.0: c['recommendation'] = "Hire"
                        elif w_tot >= 5.0: c['recommendation'] = "Maybe"
                        else: c['recommendation'] = "No Hire"
                        
                        st.session_state.agent_state["scored_candidates"][i] = c
                        agent.update_state(config, {"scored_candidates": st.session_state.agent_state["scored_candidates"]})
                        st.success("Successfully persisted local cache. Rerendering graph...")
                        import time
                        time.sleep(0.5)
                        st.rerun()

    st.markdown("<hr style='opacity:0.1; margin: 3rem 0;'>", unsafe_allow_html=True)
    _, btn_finalize_col, _ = st.columns([1,2,1])
    
    with btn_finalize_col:
        if st.button("📜 Export Intelligence Report", type="primary", use_container_width=True):
            with st.spinner("Generating Rendered HTML Pipeline..."):
                # Resume graph
                agent.invoke(Command(resume="continue"), config)
                
                html_content = generate_report(st.session_state.agent_state["scored_candidates"])
                st.session_state.report_html = html_content
                st.toast("Intelligence report generated successfully!", icon="📈")
            
if "report_html" in st.session_state:
    st.markdown("<div style='margin: 20px auto; text-align:center;'>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Final Audit Report",
        data=st.session_state.report_html,
        file_name=f"NexHire_Report_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html",
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)