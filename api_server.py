import os
import uuid
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

from agent.graph import create_agent_graph
from agent.audit import log_override
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

load_dotenv()

app = FastAPI(title="NexHire AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = create_agent_graph()

class OverrideInput(BaseModel):
    thread_id: str
    candidate_id: str
    dimension_scores: Dict[str, int]
    reason: str

class RunInput(BaseModel):
    jd_text: str
    gemini_api_key: str

@app.get("/health")
async def root():
    return {"status": "healthy", "message": "NexHire AI Backend Running"}

@app.post("/api/analyze")
async def analyze(
    jd_text: str = Form(...),
    gemini_api_key: str = Form(...),
    resume_files: Optional[List[UploadFile]] = File(None),
    linkedin_files: Optional[List[UploadFile]] = File(None),
):
    if not gemini_api_key:
        raise HTTPException(status_code=400, detail="Gemini API Key is missing.")
        
    # Temporarily inject key into environment for this thread execution flow
    os.environ["GEMINI_API_KEY"] = gemini_api_key
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    temp_dir = tempfile.mkdtemp()
    paths = []
    
    try:
        files_to_process = []
        if resume_files:
            files_to_process.extend(resume_files)
        if linkedin_files:
            files_to_process.extend(linkedin_files)
            
        for f in files_to_process:
            if not f.filename:
                continue
            fpath = os.path.join(temp_dir, f.filename)
            with open(fpath, "wb") as out:
                content = await f.read()
                out.write(content)
            paths.append(fpath)
            
        initial_state = {
            "jd_text": jd_text,
            "uploaded_file_paths": paths,
            "search_triggered": False,
            "all_candidates": [],
            "scored_candidates": []
        }
        
        # Run the workflow synchronously
        current_values = {}
        for event in agent.stream(initial_state, config):
            pass
            
        final_state = agent.get_state(config)
        return {
            "thread_id": thread_id,
            "state": final_state.values,
            "message": "Agent analyzed successfully and is paused for review."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp files in a real scenario you might defer cleanup or maintain
        # for persistent background running, but here we keep for now, then we can cleanup after request
        # shutil.rmtree(temp_dir)
        pass

@app.post("/api/override")
async def apply_override(data: OverrideInput):
    config = {"configurable": {"thread_id": data.thread_id}}
    state = agent.get_state(config).values
    scored = state.get("scored_candidates", [])
    
    target_index = next((i for i, c in enumerate(scored) if c.get("candidate_id") == data.candidate_id), None)
    
    if target_index is None:
        raise HTTPException(status_code=404, detail="Candidate not found in current context.")
        
    c = scored[target_index]
    dims = c.get("dimensions", {})
    
    s1 = data.dimension_scores.get("skills_match", dims['skills_match']['score'])
    s2 = data.dimension_scores.get("experience_relevance", dims['experience_relevance']['score'])
    s3 = data.dimension_scores.get("education_certs", dims['education_certs']['score'])
    s4 = data.dimension_scores.get("project_portfolio", dims['project_portfolio']['score'])
    s5 = data.dimension_scores.get("communication_quality", dims['communication_quality']['score'])
    
    log_override(data.thread_id, data.candidate_id, "api_override", dims['skills_match']['score'], "Manual UI Override", s1, data.reason)
    
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
    
    scored[target_index] = c
    agent.update_state(config, {"scored_candidates": scored})
    
    return {"success": True, "updated_state": agent.get_state(config).values}

@app.post("/api/finalize")
async def finalize(thread_id: str = Form(...)):
    config = {"configurable": {"thread_id": thread_id}}
    agent.invoke(Command(resume="continue"), config)
    final_state = agent.get_state(config).values
    return {"status": "completed", "candidates": final_state.get("scored_candidates", [])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
