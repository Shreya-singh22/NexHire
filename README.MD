# NexHire

**The Advanced Agentic Recruiter Suite for Modern HR Operations.**

NexHire is a rigorous, low-latency talent intelligence dashboard constructed specifically for professional semantic audits. Driven by a native LangGraph state machine and robust Google Gemini ingestion pipelines, it enforces categorical, dimension-based auditing across distributed resume repositories.

---

## High-Level Architectural Directives

- **⚡ Native Recruiter Dashboard**: Single-pane, high-density analytical environment. Direct injection of job constraints coupled with dynamic sortable assessment leaderboards.
- ** High-Order Orchestration**: Constructed with LangGraph to ensure cyclic state integrity, handling ingest branch forks and asynchronous human-in-the-loop validation stages.
- ** Enterprise Data Privacy**: Automatic algorithmic redaction of PII vectors before transit to external LLM endpoints. No local persistent caches of raw identifiers.
- ** Dense 5D Matrix Evaluation**: Algorithmic weighting protocol dissecting candidates across distinct scoring boundaries:
  - **Core Skills Array** (30%)
  - **Contextual Relevance** (25%)
  - **Standard Credentials** (15%)
  - **Production Architecture** (20%)
  - **Linguistic Precision** (10%)

---

## Deployment Stack

- **State Processor**: LangGraph
- **Reasoning Core**: Google Gemini Runtime
- **Search Engines**: Linear FAISS + Rank-BM25 Fusion
- **Render Engine**: Streamlit Custom Chassis
- **Distribution**: Production Docker Containers Ready

---

## Operational Installation

### 1. Source Acquisition
Clone the secure repository definition:
```bash
git clone https://github.com/Shreya-singh22/NexHire.git
cd NexHire
```

### 2. Dependency Configuration
Configure standard python runtime packages:
```bash
pip install -r requirements.txt
```

### 3. Authentication Trigger
Establish secure environment keys. Create a root `.env` record and apply your authorization token:
```dotenv
GEMINI_API_KEY=your_active_secure_token_here
```

---

## Execution Guidelines

Launch the production dashboard cluster locally:
```bash
streamlit run streamlit_app.py
```

**Console Access Protocol**:
1. Drop standard `PDF` or `TXT` requirement specs into the primary vault.
2. Feed candidate datasets (`DOCX`, `PDF`, `JSON` exported streams).
3. Initialize **Audit Pipeline** to engage the agent flow.
4. Analyze telemetry via the **Leaderboard** and override dimensional matrices.

---

## Project Blueprint

```plaintext
NexHire/
├── agent/             # Semantic Control Unit & Graph Trees
├── resume_model/      # Vector Engineering & Ingestion logic
├── templates/         # Final Export Rendering Schema
├── index_store/       # Optimized Search Index Storage
├── Dockerfile         # Containerized Runtime Profile
└── streamlit_app.py   # Application Entrance Node
```

*All code definitions within this system are confidential and reserved solely for NexHire operation workflows.*
