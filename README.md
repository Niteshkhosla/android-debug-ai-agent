# Android Debugging AI Agent

> AI-powered Android crash analyzer — Built by a 13+ Year Android Expert

##  What it does
- **Agent 1** — Classifies Android crashes (NPE, ANR, OOM)
- **RAG** — Searches Android knowledge base for relevant solutions
- **Agent 2** — Suggests specific Kotlin fixes using AI + Docs
- **Agent 3** — Generates professional crash report in table format

##  Flow
Crash Log Input
↓
Agent 1: Classify (NPE/ANR/OOM)
↓
RAG: Search Android Knowledge Base
↓
Agent 2: Generate Kotlin Fix
↓
Agent 3: Professional Report
↓
Complete Analysis! 

## 🛠️ Tech Stack
- Python
- LangGraph — Multi Agent System
- LangChain — AI Chains
- Groq LLM — llama-3.3-70b
- ChromaDB — Vector Store
- RAG — Android Knowledge Base
- python-dotenv — API Key Management

##  How to run

**1. Install dependencies**
pip install -r requirements.txt

**2. Add API key — create .env file**
GROQ_API_KEY=your-key-here

**3. Setup Android Knowledge Base**
python rag_setup.py

**4. Run**
python main.py

##  Sample Output
Crash Type: NPE
Relevant Docs: Use safe call operator ?. ...
Solution: Initialize variable before use...
Report: Professional table with severity,
root cause, prevention

##  Author
**Nitesh Khosla**
13+ Years Android Experience | Principal Android Architect
LinkedIn: linkedin.com/in/nitesh-khosla-57574637
GitHub: github.com/Niteshkhosla
