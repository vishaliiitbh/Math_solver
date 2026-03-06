# 🧮 Math Mentor AI
### Multimodal JEE Math Solver · RAG + Multi-Agent + HITL + Memory

A production-ready AI tutoring application that solves JEE-style math problems from text, images, or audio — powered by Groq (LLaMA 3.3 70B + Whisper), Pinecone, and a 5-agent pipeline.

---

## 🏗️ Architecture

```
Input (Text/Image/Audio)
    ↓
Multimodal Parser (OCR / ASR)
    ↓
Parser Agent → Router Agent → Solver Agent (RAG) → Verifier Agent → Explainer Agent
                                    ↑
                          Pinecone Knowledge Base
                                    ↑
                          Memory: Similar Past Problems
```

See `architecture.mermaid` for the full diagram.

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/math-mentor
cd math-mentor
pip install -r requirements.txt
```

### 2. Set API Keys

```bash
cp .env.example .env
# Edit .env and fill in:
# GROQ_API_KEY=gsk_...
# PINECONE_API_KEY=pcsk_...
```

Get keys from:
- Groq: https://console.groq.com
- Pinecone: https://app.pinecone.io

### 3. Ingest Knowledge Base

On first run, click **📚 Ingest Knowledge Base** in the sidebar. This embeds 10 math documents into Pinecone (~1 minute).

### 4. Run the App

```bash
streamlit run app.py
```

Open http://localhost:8501

---

## 🤖 Agent Pipeline

| Agent | Role |
|-------|------|
| 🔍 **Parser Agent** | Cleans raw input, extracts topic/variables/goal |
| 🧭 **Router Agent** | Classifies problem type, generates RAG query |
| ⚙️ **Solver Agent** | Solves using RAG context + memory |
| ✅ **Verifier Agent** | Checks correctness, domain validity, triggers HITL |
| 💬 **Explainer Agent** | Creates student-friendly step-by-step explanation |

---

## 📚 Knowledge Base

10 curated documents covering:
- Algebra identities & formulas
- Probability theorems
- Calculus derivatives & limits
- Linear algebra basics
- Solution templates (algebra, calculus, probability)
- Common JEE mistakes
- JEE tips & tricks

---

## 🧠 Memory System

- **JSON log**: stores every solved problem locally
- **Pinecone memory namespace**: semantic search over past correct solutions
- At solve-time, retrieves similar past problems to reuse patterns
- Feedback (correct/incorrect) determines what gets stored in Pinecone

---

## ⚠️ Human-in-the-Loop (HITL)

HITL triggers automatically when:
- OCR confidence < 75%
- ASR transcription looks unreliable
- Parser detects ambiguity
- Verifier is not confident

User can: ✅ Approve / ✏️ Edit & Resubmit / ❌ Reject

---

## 📦 Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq (LLaMA 3.3 70B Versatile) |
| Speech-to-Text | Groq Whisper Large v3 |
| OCR | EasyOCR |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | Pinecone (Serverless) |
| Frontend | Streamlit |
| Memory | JSON + Pinecone namespace |

---

## 🌐 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect repo, set `app.py` as main file
4. Add secrets: `GROQ_API_KEY`, `PINECONE_API_KEY`

### HuggingFace Spaces
1. Create a Space with Streamlit SDK
2. Upload files
3. Set env vars in Space settings

---

## 📁 Project Structure

```
math-mentor/
├── app.py                      # Streamlit UI
├── pipeline.py                 # Main orchestrator
├── agents/
│   ├── parser_agent.py         # Parses raw input
│   ├── router_agent.py         # Routes to strategy
│   ├── solver_agent.py         # Solves with RAG
│   ├── verifier_agent.py       # Verifies correctness
│   └── explainer_agent.py      # Generates explanation
├── rag/
│   ├── embedder.py             # Pinecone ingestion
│   ├── retriever.py            # Semantic retrieval
│   └── knowledge_base/         # 10 math .txt docs
├── memory/
│   └── memory_store.py         # Memory CRUD + search
├── tools/
│   ├── ocr_tool.py             # EasyOCR wrapper
│   └── audio_tool.py           # Whisper wrapper
├── utils/
│   └── groq_client.py          # Groq API wrapper
├── requirements.txt
├── .env.example
```
