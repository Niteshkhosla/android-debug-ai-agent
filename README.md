#  Android Debugging AI Agent

> AI-powered Android crash analyzer — Built by a 13+ Year Android Expert | Principal Android Engineer

##  What it does
- **Agent 1** — Automatically classifies Android crashes (NPE, ANR, OOM)
- **RAG Pipeline** — Searches Android knowledge base for relevant solutions
- **Agent 2** — Severity-based routing (LOW/MEDIUM/HIGH) with specialized agents
- **Agent 3** — Generates professional crash analysis report in table format
- **File Input** — Real crash logs loaded from .txt files — production-ready workflow

##  Flow
\```
Crash Log (.txt file)
      ↓
Agent 1: Classify (NPE / ANR / OOM)
      ↓
RAG: Search Android Knowledge Base (ChromaDB)
      ↓
Agent 2: Severity Routing → Specialized Fix
         NPE  → LOW severity agent
         ANR  → MEDIUM severity agent
         OOM  → HIGH severity agent
      ↓
Agent 3: Professional Table Report
      ↓
Complete Analysis! 
\```

##  Tech Stack
| Technology | Purpose |
|---|---|
| Python | Core language |
| LangGraph | Multi-Agent orchestration |
| LangChain | AI chains and prompts |
| Groq LLM (llama-3.3-70b) | Language model |
| ChromaDB | Vector store for RAG |
| SentenceTransformers | Embeddings |
| python-dotenv | API key management |

## How to run

**1. Clone the repo**
\```
git clone https://github.com/Niteshkhosla/android-debug-ai-agent
cd android-debug-ai-agent
\```

**2. Install dependencies**
\```
pip install -r requirements.txt
\```

**3. Add API key — create .env file**
\```
GROQ_API_KEY=your-groq-api-key-here
\```

**4. Setup Android Knowledge Base (run once)**
\```
python rag_setup.py
\```

**5. Add your crash log**
\```
# Paste your Android crash log in crash_log.txt
\```

**6. Run**
\```
python main.py
\```

##  Sample Output
\```
 Crash log loaded! — 230 characters

Crash Type : NPE
Severity   : LOW

Solution:
- Use Kotlin safe call operator ?.
- Use Elvis operator ?: for default values
- Use lateinit for late initialization

Report:
| Category   | Description                    |
|------------|--------------------------------|
| Crash Type | NullPointerException (NPE)     |
| Severity   | Low                            |
| Root Cause | Null object reference          |
| Solution   | Safe call operator, Elvis op   |
| Prevention | Always initialize variables    |
\```

##  Why this project is unique
- Built by a **13+ year Android expert** — domain knowledge baked in
- **RAG** makes solutions accurate — not just generic AI answers
- **Severity routing** — different agents for different crash types
- **Production-ready** — file input, structured output, modular agents

##  Author
**Nitesh Khosla**
Principal Android Engineer | AI Agent Developer | 13+ Years Experience

 [GitHub](https://github.com/Niteshkhosla)
 ntsh10khosla@gmail.com
