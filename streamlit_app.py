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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --primary: #6366f1;
    --primary-glow: rgba(99, 102, 241, 0.5);
    --bg-dark: #050508;
    --card-bg: rgba(255, 255, 255, 0.03);
    --card-border: rgba(255, 255, 255, 0.08);
    --text-main: #e2e8f0;
    --text-muted: #94a3b8;
    --hire-color: #10b981;
    --maybe-color: #f59e0b;
    --nohire-color: #ef4444;
}

/* Main Container and Background Styling */
.stApp {
    background-color: var(--bg-dark);
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(99, 102, 241, 0.12) 0%, transparent 35%),
        radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.1) 0%, transparent 40%),
        radial-gradient(circle at 50% 80%, rgba(236, 72, 153, 0.05) 0%, transparent 45%);
    color: var(--text-main);
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: rgba(10, 10, 15, 0.7) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid var(--card-border);
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Hide streamlit elements */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.03em;
}

/* Hero Section Enhancements */
.hero-container {
    padding: 4rem 1rem 2rem;
    text-align: center;
    position: relative;
}

.hero-glow {
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 100px;
    background: linear-gradient(90deg, #6366f1, #a855f7);
    filter: blur(80px);
    opacity: 0.4;
    z-index: -1;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    color: #818cf8;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.1);
    animation: pulse 2s infinite ease-in-out;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 0.9;}
    50% { transform: scale(1.02); opacity: 1;}
    100% { transform: scale(1); opacity: 0.9;}
}

.hero-title {
    font-size: clamp(2.8rem, 6vw, 4.5rem);
    font-weight: 800;
    background: linear-gradient(to bottom right, #ffffff 20%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    line-height: 1.1;
}

.hero-subtitle {
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto 2rem;
    font-weight: 400;
}

/* Premium Uploader Box styling override */
div[data-testid="stFileUploadDropzone"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 2px dashed rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    transition: all 0.3s ease;
}

div[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--primary) !important;
    background: rgba(99, 102, 241, 0.04) !important;
}

/* Custom styled button style */
div.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    width: 100% !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5) !important;
}

/* Candidate Card V2 */
.candidate-card {
    background: rgba(15, 15, 24, 0.6);
    backdrop-filter: blur(12px);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, border-color 0.3s ease;
}

.candidate-card:hover {
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
}

.candidate-card::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
    z-index: 0;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 1.25rem;
    margin-bottom: 1.25rem;
    position: relative;
    z-index: 1;
}

.candidate-name {
    font-size: 1.6rem;
    font-weight: 700;
    color: white;
    margin: 0 0 0.5rem 0;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-hire { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
.status-maybe { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
.status-nohire { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

.score-container {
    text-align: right;
}

.score-main {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
}
.score-hire { color: #10b981; text-shadow: 0 0 15px rgba(16, 185, 129, 0.3); }
.score-maybe { color: #f59e0b; text-shadow: 0 0 15px rgba(245, 158, 11, 0.3); }
.score-nohire { color: #ef4444; text-shadow: 0 0 15px rgba(239, 68, 68, 0.3); }

.summary-text {
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    position: relative;
    z-index: 1;
}

/* Rubric Grid and Progress Bars */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    position: relative;
    z-index: 1;
}

.metric-item {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.metric-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.metric-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-val {
    font-weight: 700;
    font-family: 'Space Grotesk';
    color: white;
}

.prog-bar-bg {
    height: 6px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 3px;
    overflow: hidden;
}

.prog-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), #8b5cf6);
    border-radius: 3px;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-justification {
    font-size: 0.75rem;
    color: #94a3b8;
    margin-top: 8px;
    font-style: italic;
    line-height: 1.4;
}
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
    <div class="hero-glow"></div>
    <div class="hero-badge"><span>✨</span> Powered by Google Gemini & LangGraph</div>
    <h1 class="hero-title">NexHire AI</h1>
    <p class="hero-subtitle">Modern agentic screening system performing deep semantic evaluations against custom job descriptions using a 5-dimension rubric.</p>
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
    jd_file = st.file_uploader("Drop job requirements (.txt)", type=["txt"], label_visibility="collapsed")
    
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
            
        jd_text = jd_file.read().decode("utf-8")
        
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
                <!-- Skills -->
                <div class="metric-item">
                    <div class="metric-top"><span class="metric-label">Skills (30%)</span><span class="metric-val">{sk} / 10</span></div>
                    <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{get_pct(sk)}%"></div></div>
                    <div class="metric-justification">{escape(dims.get('skills_match', {}).get('justification', ''))}</div>
                </div>
                <!-- Exp -->
                <div class="metric-item">
                    <div class="metric-top"><span class="metric-label">Experience (25%)</span><span class="metric-val">{ex} / 10</span></div>
                    <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{get_pct(ex)}%"></div></div>
                    <div class="metric-justification">{escape(dims.get('experience_relevance', {}).get('justification', ''))}</div>
                </div>
                <!-- Edu -->
                <div class="metric-item">
                    <div class="metric-top"><span class="metric-label">Education (15%)</span><span class="metric-val">{ed} / 10</span></div>
                    <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{get_pct(ed)}%"></div></div>
                    <div class="metric-justification">{escape(dims.get('education_certs', {}).get('justification', ''))}</div>
                </div>
                <!-- Proj -->
                <div class="metric-item">
                    <div class="metric-top"><span class="metric-label">Projects (20%)</span><span class="metric-val">{pr} / 10</span></div>
                    <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{get_pct(pr)}%"></div></div>
                    <div class="metric-justification">{escape(dims.get('project_portfolio', {}).get('justification', ''))}</div>
                </div>
                <!-- Comm -->
                <div class="metric-item">
                    <div class="metric-top"><span class="metric-label">Communication (10%)</span><span class="metric-val">{cm} / 10</span></div>
                    <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{get_pct(cm)}%"></div></div>
                    <div class="metric-justification">{escape(dims.get('communication_quality', {}).get('justification', ''))}</div>
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