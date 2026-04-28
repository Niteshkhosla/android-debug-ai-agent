#  Android Debugging AI Agent

> AI-powered Android crash analyzer — Built by Nitesh Khosla | 13+ Years Android Expert

## What it does
- **Agent 1** — Automatically classifies Android crashes (NPE, ANR, OOM)
- **RAG Pipeline** — Searches Android knowledge base for relevant solutions
- **Agent 2** — Severity-based routing (LOW/MEDIUM/HIGH) with specialized agents
- **Agent 3** — Generates professional crash analysis report in table format
- **Streamlit UI** — Beautiful web interface to analyze crashes in browser!

## Flow
\```
Crash Log Input (Web UI)
      ↓
Agent 1: Classify (NPE / ANR / OOM)
      ↓
RAG: Search Android Knowledge Base (ChromaDB)
      ↓
Agent 2: Severity Routing
         NPE  → 🟢 LOW severity agent
         ANR  → 🟡 MEDIUM severity agent
         OOM  → 🔴 HIGH severity agent
      ↓
Agent 3: Professional Table Report
      ↓
 Download Report!
\```

##  Web UI Preview
\```
🤖 Android Debugging AI Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Paste your crash log...
[🔍 Analyze Crash Button]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐛 Crash Type : 🔵 NPE
⚠️ Severity   : 🟢 LOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Solution + 📊 Report Table
[💾 Download Report]
\```

## 🛠️ Tech Stack
| Technology | Purpose |
|---|---|
| Python | Core language |
| LangGraph | Multi-Agent orchestration |
| LangChain | AI chains and prompts |
| Groq LLM (llama-3.3-70b) | Language model |
| ChromaDB | Vector store for RAG |
| HuggingFace Embeddings | Text embeddings |
| Streamlit | Web UI |
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

**5. Run Web UI**
\```
streamlit run app.py
\```

**6. Or run Terminal version**
\```
python main.py
\```

## Sample Output
\```
Crash Type : 🔵 NPE
Severity   : 🟢 LOW

Solution:
- Use Kotlin safe call operator ?.
- Use Elvis operator ?: for default values
- Use lateinit for late initialization

Report:
| Category   | Description                 |
|------------|-----------------------------|
| Crash Type | NullPointerException (NPE)  |
| Severity   | Low                         |
| Root Cause | Null object reference       |
| Solution   | Safe call operator          |
| Prevention | Always initialize variables |

 Report saved: crash_report_2026-04-28_10-30.txt
\```

## Project Structure
\```
android-debug-ai-agent/
├── app.py          — Streamlit Web UI
├── main.py         — Terminal version
├── state.py        — CrashState definition
├── constants.py    — All prompts & constants
├── rag_setup.py    — Knowledge base setup
├── crash_log.txt   — Sample crash log
├── requirements.txt
├── README.md
└── .gitignore
\```

## Why this project is unique
- Built by **13+ year Android expert** — domain knowledge baked in
- **RAG** makes solutions accurate — not just generic AI answers
- **Severity routing** — different agents for different crash types
- **Web UI** — paste crash log, get analysis instantly!
- **Production-ready** — modular, clean architecture

## 👨‍💻 Author
**Nitesh Khosla**
Principal Android Engineer | AI Agent Developer | 13+ Years

🔗 [LinkedIn](https://linkedin.com/in/nitesh-khosla-57574637)
🐙 [GitHub](https://github.com/Niteshkhosla)
📧 ntsh10khosla@gmail.com
