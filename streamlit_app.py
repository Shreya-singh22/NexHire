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
    page_title="NexHire AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed" # collapsed to optimize dual-col space
)

# ── Strict Recruiter Dashboard CSS ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;700&family=Geist:wght@400;500;600;700&display=swap');

:root {
    --zinc-950: #09090b;
    --zinc-900: #18181b;
    --zinc-800: #27272a;
    --zinc-400: #a1a1aa;
    --zinc-100: #f4f4f5;
    --emerald-500: #10b981;
    --amber-500: #f59e0b;
    --rose-500: #f43f5e;
}

.stApp {
    background-color: var(--zinc-950);
    color: var(--zinc-100);
    font-family: 'Geist', -apple-system, sans-serif;
    letter-spacing: -0.01em;
}

/* Custom Top Nav */
.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--zinc-800);
    margin-bottom: 2rem;
}
.nav-logo {
    font-weight: 700;
    font-size: 1.1rem;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.nav-pill {
    font-size: 0.7rem;
    font-family: 'Geist Mono', monospace;
    padding: 0.2rem 0.6rem;
    border-radius: 99px;
    border: 1px solid var(--zinc-800);
    background: var(--zinc-900);
    color: var(--emerald-500);
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.nav-pill::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--emerald-500);
}

/* Typography defaults override */
h1, h2, h3, h4, h5 {
    font-family: 'Geist', sans-serif;
    font-weight: 600;
    color: white;
    letter-spacing: -0.02em;
}

/* Minimalist Staged Area */
.section-header {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--zinc-400);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
}

/* Column Divider/Spacing */
div[data-testid="stHorizontalBlock"] > div {
    gap: 2rem;
}

/* Table Leaderboard Base */
.table-row {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    background: var(--zinc-950);
    border-bottom: 1px solid var(--zinc-800);
    transition: background 0.1s;
}
.table-row:hover {
    background: var(--zinc-900);
}
.table-header {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--zinc-400);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.5rem 1rem;
    background: var(--zinc-900);
    border: 1px solid var(--zinc-800);
    border-radius: 6px 6px 0 0;
}

/* Common metrics styles */
div[data-testid="stMetric"] {
    background: var(--zinc-900);
    border: 1px solid var(--zinc-800);
    border-radius: 8px;
    padding: 1rem;
}

/* Forms buttons */
div.stButton > button {
    background: white !important;
    color: black !important;
    font-family: 'Geist', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    border: none !important;
    font-size: 0.85rem !important;
}
div.stButton > button:hover {
    background: #e4e4e7 !important;
}

/* Badge class utils */
.verdict-badge {
    font-family: 'Geist Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    border: 1px solid transparent;
}
.v-hire { background: rgba(16, 185, 129, 0.1); color: var(--emerald-500); border-color: rgba(16, 185, 129, 0.2); }
.v-maybe { background: rgba(245, 158, 11, 0.1); color: var(--amber-500); border-color: rgba(245, 158, 11, 0.2); }
.v-nohire { background: rgba(244, 63, 94, 0.1); color: var(--rose-500); border-color: rgba(244, 63, 94, 0.2); }

/* Dense lists inside dialog */
.dialog-stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.stat-box {
    background: var(--zinc-900);
    border: 1px solid var(--zinc-800);
    border-radius: 6px;
    padding: 1rem;
}
.stat-box-lbl {
    font-size: 0.7rem;
    color: var(--zinc-400);
    font-family: 'Geist Mono', monospace;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.stat-box-val {
    font-size: 1.1rem;
    font-weight: 700;
    color: white;
}
.stat-box-desc {
    font-size: 0.75rem;
    color: var(--zinc-400);
    margin-top: 0.5rem;
    line-height: 1.4;
}

/* Strict input styling */
div[data-testid="stFileUploadDropzone"] {
    background: var(--zinc-900) !important;
    border: 1px dashed var(--zinc-800) !important;
    border-radius: 6px !important;
}

/* Sidebar forced minimal dark */
[data-testid="stSidebar"] {
    background-color: var(--zinc-950) !important;
    border-right: 1px solid var(--zinc-800);
}
</style>
""", unsafe_allow_html=True)

# ── Top Nav Component ────────────────────────────────────────────────────────
st.markdown("""
<div class="top-nav">
    <div class="nav-logo">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
        NexHire AI
    </div>
    <div class="nav-pill">System Operational</div>
</div>
""", unsafe_allow_html=True)

# ── Init Agent Cache ─────────────────────────────────────────────────────────
@st.cache_resource
def get_agent():
    return create_agent_graph()

agent = get_agent()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# ── Utility / Helpers ─────────────────────────────────────────────────────────

def get_verdict_html(rec):
    if rec == "Hire": return f'<span class="verdict-badge v-hire">{rec}</span>'
    if rec == "Maybe": return f'<span class="verdict-badge v-maybe">{rec}</span>'
    return f'<span class="verdict-badge v-nohire">Pass</span>'

def get_score_color(val):
    if val >= 7.0: return "#10b981" # emerald
    if val >= 5.0: return "#f59e0b" # amber
    return "#f43f5e" # rose

def generate_report(candidates):
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('report.html')
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return template.render(candidates=candidates, date=date_str)

@st.dialog("Candidate Intelligence Assessment", width="large")
def show_candidate_detail(c, idx):
    # Safe values extraction
    dims = c.get("dimensions", {})
    def get_safe(k): return dims.get(k, {}).get('score', 0)
    
    c_id = c.get('candidate_id')
    weighted = c.get('weighted_total', 0)
    rec = c.get('recommendation', 'No Hire')
    
    score_col = get_score_color(weighted)
    
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:1rem; margin-bottom:1rem;">
        <div>
            <h2 style="margin:0; font-family:'Geist Mono', monospace;">{escape(c_id)}</h2>
            <div style="margin-top:0.5rem;">{get_verdict_html(rec)}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:2.5rem; font-weight:700; color:{score_col}; font-family:'Geist Mono'; line-height:1;">{weighted:.2f}</div>
            <div style="font-size:0.7rem; color:#a1a1aa; font-family:'Geist Mono';">OVERALL SCORE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Executive Summary**")
    st.markdown(f"<div style='background:#18181b; padding:1rem; border-radius:6px; border:1px solid #27272a; font-size:0.9rem; margin-bottom:1.5rem;'>{escape(c.get('summary', ''))}</div>", unsafe_allow_html=True)
    
    st.markdown("**Dimension Breakdown**")
    
    c1, c2, c3 = st.columns(3)
    
    def render_box(col, label, score, just):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-box-lbl">{label}</div>
                <div class="stat-box-val">{score} / 10</div>
                <div class="stat-box-desc">{escape(just)}</div>
            </div>
            """, unsafe_allow_html=True)

    render_box(c1, "Skills Match", get_safe('skills_match'), dims.get('skills_match', {}).get('justification', ''))
    render_box(c2, "Experience", get_safe('experience_relevance'), dims.get('experience_relevance', {}).get('justification', ''))
    render_box(c3, "Education", get_safe('education_certs'), dims.get('education_certs', {}).get('justification', ''))
    
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    
    c4, c5, _ = st.columns(3)
    render_box(c4, "Projects", get_safe('project_portfolio'), dims.get('project_portfolio', {}).get('justification', ''))
    render_box(c5, "Communication", get_safe('communication_quality'), dims.get('communication_quality', {}).get('justification', ''))

    st.markdown("---")
    st.markdown("**Human Override Control**")
    with st.form(key=f"dialog_form_{idx}"):
        ca, cb, cc = st.columns(3)
        s1 = ca.slider("Skills Override", 0, 10, get_safe('skills_match'))
        s2 = cb.slider("Exp Override", 0, 10, get_safe('experience_relevance'))
        s3 = cc.slider("Edu Override", 0, 10, get_safe('education_certs'))
        
        cd, ce, _ = st.columns(3)
        s4 = cd.slider("Project Override", 0, 10, get_safe('project_portfolio'))
        s5 = ce.slider("Comm Override", 0, 10, get_safe('communication_quality'))
        
        reason = st.text_area("Log rationale for adjustment", placeholder="e.g., confirmed via manual vetting...")
        
        if st.form_submit_button("Persist Overrides", type="primary"):
            if not reason.strip():
                st.error("Audit log required.")
            else:
                log_override(st.session_state.thread_id, c_id, "manual_edit", dims['skills_match']['score'], "", s1, reason)
                
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
                
                st.session_state.agent_state["scored_candidates"][idx] = c
                agent.update_state(config, {"scored_candidates": st.session_state.agent_state["scored_candidates"]})
                st.success("Updating state layer...")
                import time
                time.sleep(0.3)
                st.rerun()

# ── Workspace Construction ────────────────────────────────────────────────────

workspace_l, workspace_r = st.columns([1, 2])

with workspace_l:
    st.markdown('<div class="section-header">Job Context</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("**Required Credentials**")
        api_key_input = st.text_input(
            "Gemini API Token",
            value=os.getenv("GEMINI_API_KEY", ""),
            type="password",
            help="Temporary injection in process memory only."
        )
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
            
        st.divider()
        
        st.markdown("**Description Protocol**")
        jd_file = st.file_uploader("Drop job file", type=["txt", "pdf"], label_visibility="collapsed")
        
        st.markdown("**Raw Resumes**")
        resume_files = st.file_uploader("Drop resume set", type=["pdf", "docx"], accept_multiple_files=True, label_visibility="collapsed")
        
        st.markdown("**Auxiliary Data**")
        linkedin_files = st.file_uploader("Drop JSON files", type=["json"], accept_multiple_files=True, label_visibility="collapsed")
        
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        analyze_btn = st.button("Execute Audit Pipeline", type="primary", use_container_width=True)

    # Audit Trigger logic
    if analyze_btn:
        if not jd_file:
            st.warning("Mandatory parameter missing: Job Description.")
        elif not os.getenv("GEMINI_API_KEY"):
            st.error("Execution halted: Authorization token required.")
        else:
            with st.status("Initializing semantic graph flow...", expanded=True) as status:
                temp_dir = tempfile.mkdtemp()
                paths = []
                all_files = (resume_files or []) + (linkedin_files or [])
                for f in all_files:
                    fpath = os.path.join(temp_dir, f.name)
                    with open(fpath, "wb") as out: out.write(f.read())
                    paths.append(fpath)
                
                jd_temp = os.path.join(temp_dir, f"JD_{jd_file.name}")
                with open(jd_temp, "wb") as f: f.write(jd_file.getvalue())
                try:
                    jd_txt, _ = extract_text_and_links(jd_temp)
                except:
                    try: jd_txt = jd_file.read().decode("utf-8")
                    except: st.error("JD extract err"); st.stop()
                
                init_state = {
                    "jd_text": jd_txt,
                    "uploaded_file_paths": paths,
                    "search_triggered": False,
                    "all_candidates": [],
                    "scored_candidates": []
                }
                
                for ev in agent.stream(init_state, config):
                    for step, res in ev.items():
                        st.write(f"› Resolved: `{step}`")
                
                status.update(label="Flow Completed", state="complete", expanded=False)
                st.session_state.agent_state = agent.get_state(config).values
                st.rerun()

with workspace_r:
    st.markdown('<div class="section-header">Ranked Leaderboard</div>', unsafe_allow_html=True)
    
    if "agent_state" in st.session_state:
        state = st.session_state.agent_state
        raw_list = state.get("scored_candidates", [])
        
        # Sort by overall weighted score descending by default
        candidates = sorted(raw_list, key=lambda x: x.get('weighted_total', 0), reverse=True)
        
        # Top Metrics strip
        num_total = len(candidates)
        avg_score = sum(c.get('weighted_total', 0) for c in candidates) / num_total if num_total > 0 else 0
        num_hire = len([c for c in candidates if c.get('recommendation') == "Hire"])
        hire_rate = (num_hire / num_total * 100) if num_total > 0 else 0
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Candidates", f"{num_total}")
        m2.metric("Average Score", f"{avg_score:.2f}")
        m3.metric("Shortlist Rate", f"{hire_rate:.1f}%")
        
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        
        # Segmented Control for filtering
        filter_options = ["All", "Hire", "Maybe", "No Hire"]
        selected_filter = st.segmented_control("Filter by verdict", options=filter_options, default="All", selection_mode="single", label_visibility="collapsed")
        
        filtered_list = candidates
        if selected_filter and selected_filter != "All":
            filtered_list = [c for c in candidates if c.get('recommendation') == selected_filter]
        
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        
        # Manual Header Construction
        st.markdown("""
        <div class="table-header">
            <div style="display:grid; grid-template-columns: 60px 1fr 100px 100px 80px; align-items:center;">
                <div>Rank</div>
                <div>Identifier</div>
                <div style="text-align:center;">Verdict</div>
                <div style="text-align:right;">Score</div>
                <div style="text-align:right; padding-right:10px;">Action</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if not filtered_list:
            st.info("No candidate records match the set viewport filter.")
        else:
            # Iterate and render dynamic rows
            for idx, c in enumerate(filtered_list):
                
                col_wrap = st.container(border=True)
                with col_wrap:
                    # Internal grid for aligning content cleanly next to streamlit buttons
                    # Use columns to hold standard layout data
                    c_rank, c_name, c_verd, c_score, c_btn = st.columns([0.5, 2.5, 1, 1, 1])
                    
                    w_score = c.get('weighted_total', 0)
                    clr = get_score_color(w_score)
                    rec = c.get('recommendation', 'No Hire')
                    
                    with c_rank:
                        st.markdown(f"<div style='font-family:Geist Mono; font-size:0.8rem; padding-top:6px; color:#a1a1aa;'>#{idx+1}</div>", unsafe_allow_html=True)
                    with c_name:
                        st.markdown(f"<div style='font-weight:600; font-size:0.9rem; padding-top:6px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;'>{escape(c.get('candidate_id'))}</div>", unsafe_allow_html=True)
                    with c_verd:
                        st.markdown(f"<div style='text-align:center; padding-top:6px;'>{get_verdict_html(rec)}</div>", unsafe_allow_html=True)
                    with c_score:
                        st.markdown(f"<div style='text-align:right; padding-top:4px; font-weight:700; font-family:Geist Mono; color:{clr}; font-size:1rem;'>{w_score:.2f}</div>", unsafe_allow_html=True)
                    with c_btn:
                        # We locate original index in non-filtered list if state update is required
                        actual_idx = 0
                        for search_i, raw_c in enumerate(st.session_state.agent_state["scored_candidates"]):
                            if raw_c.get('candidate_id') == c.get('candidate_id'):
                                actual_idx = search_i
                                break
                        
                        if st.button("View", key=f"btn_view_{c.get('candidate_id')}", use_container_width=True):
                            show_candidate_detail(c, actual_idx)
                            
        # Finalize action
        st.markdown("<div style='margin-top:3rem'></div>", unsafe_allow_html=True)
        b1, b2 = st.columns([1,1])
        with b2:
            if st.button("Generate Export Audit Payload", type="secondary", use_container_width=True):
                agent.invoke(Command(resume="continue"), config)
                st.session_state.final_report = generate_report(candidates)
                st.success("Snapshot constructed.")
                
        if "final_report" in st.session_state:
            st.download_button("Download Rendered Assessment Data", data=st.session_state.final_report, file_name=f"export_{datetime.now().strftime('%Y%m%d')}.html", mime="text/html", use_container_width=True)
            
    else:
        # Empty state
        st.markdown("""
        <div style="text-align:center; padding: 5rem 2rem; border: 1px dashed var(--zinc-800); border-radius: 8px; background:var(--zinc-900);">
            <div style="color:var(--zinc-400); font-size:0.9rem; font-family:Geist Mono;">AWAITING_EVALUATION_STREAM</div>
            <div style="font-size:0.8rem; color:#52525b; margin-top:0.5rem;">Execute audit flow in the configuration workspace on the left to populate grid.</div>
        </div>
        """, unsafe_allow_html=True)

# ── System Settings Overlay (Fallback Hidden Sidebar) ───────────────────────
with st.sidebar:
    st.markdown("### System Details")
    st.caption(f"Active Thread Ref: `{st.session_state.thread_id}`")
    st.caption("Talent Pool Strategy: FAISS Local Matrix")
    if st.button("Hard Purge Cache"):
        st.session_state.clear()
        st.rerun()