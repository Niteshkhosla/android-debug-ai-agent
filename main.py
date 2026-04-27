from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from state import CrashState
from datetime import datetime

from constants import (
    CLASSIFY_SYSTEM, CLASSIFY_HUMAN,
    NPE_SYSTEM, NPE_HUMAN,
    ANR_SYSTEM, ANR_HUMAN,
    OOM_SYSTEM, OOM_HUMAN,
    OTHER_SYSTEM, OTHER_HUMAN,
    REPORT_SYSTEM, REPORT_HUMAN,
    SEVERITY_NPE, SEVERITY_ANR,
    SEVERITY_OOM, SEVERITY_OTHER,
    CRASH_LOG_FILE, KNOWLEDGE_BASE_DIR, REPORT_PREFIX
)


load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

# RAG - Knowledge Base load karo
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory=KNOWLEDGE_BASE_DIR,
    embedding_function=embeddings
)

# File se crash log padhna
with open(CRASH_LOG_FILE, "r") as file:
    crash_log = file.read()

print("✅ Crash log loaded!")
print(f"Log size: {len(crash_log)} characters\n")


# Agent 1 - Classify
def classify_crash(state: CrashState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", CLASSIFY_SYSTEM),
        ("human", CLASSIFY_HUMAN)
        ])
    
    chain = prompt | llm
    result = chain.invoke({"crash_log": state["crash_log"]})
    return {"crash_type": result.content}

# RAG Node
def search_docs(state: CrashState):
    docs = vectorstore.similarity_search(state["crash_type"], k=1)
    relevant = docs[0].page_content if docs else "No docs found"
    return {"relevant_docs": relevant}

# Router
def route_crash(state: CrashState):
    crash_type = state["crash_type"].strip()
    if crash_type in "NPE":
        return "npe_solution"
    elif  crash_type in "ANR":
        return "anr_solution"
    elif  crash_type  in "OOM":
        return "oom_solution"
    else:
        return "other_solution"

# NPE Solution Agent
def npe_solution(state: CrashState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", NPE_SYSTEM),
        ("human", NPE_HUMAN)
    ])
    chain = prompt | llm
    result = chain.invoke({
        "crash_log": state["crash_log"],
        "relevant_docs": state["relevant_docs"]
    })
    return {"solution": result.content, "severity": SEVERITY_NPE}

# ANR Solution Agent
def anr_solution(state: CrashState):
    prompt = ChatPromptTemplate.from_messages([
        ("system",ANR_SYSTEM),
        ("human", ANR_HUMAN)
    ])
    chain = prompt | llm
    result = chain.invoke({
        "crash_log": state["crash_log"],
        "relevant_docs": state["relevant_docs"]
    })
    return {"solution": result.content, "severity": SEVERITY_ANR}

# OOM Solution Agent
def oom_solution(state: CrashState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", OOM_SYSTEM),
        ("human", OOM_HUMAN)
    ])
    chain = prompt | llm
    result = chain.invoke({
        "crash_log": state["crash_log"],
        "relevant_docs": state["relevant_docs"]
    })
    return {"solution": result.content, "severity": SEVERITY_OOM}

# Other Solution Agent
def other_solution(state: CrashState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", OTHER_SYSTEM),
        ("human", OTHER_HUMAN)
    ])
    chain = prompt | llm
    result = chain.invoke({
        "crash_log": state["crash_log"],
        "relevant_docs": state["relevant_docs"]
    })
    return {"solution": result.content, "severity":SEVERITY_OTHER}

# Report Agent
def generate_report(state: CrashState):
    prompt = ChatPromptTemplate.from_messages([
        ("system",REPORT_SYSTEM),
        ("human",REPORT_HUMAN)
    ])
    chain = prompt | llm
    result = chain.invoke({
        "crash_type": state["crash_type"],
        "severity": state["severity"],
        "solution": state["solution"]
    })
    return {"report": result.content}

# Graph
graph = StateGraph(CrashState)
graph.add_node("classify", classify_crash)
graph.add_node("search_docs", search_docs)
graph.add_node("npe_solution", npe_solution)
graph.add_node("anr_solution", anr_solution)
graph.add_node("oom_solution", oom_solution)
graph.add_node("other_solution", other_solution)
graph.add_node("report", generate_report)

graph.set_entry_point("classify")
graph.add_edge("classify", "search_docs")

# Conditional Routing
graph.add_conditional_edges(
    "search_docs",
    route_crash,
    {
        "npe_solution": "npe_solution",
        "anr_solution": "anr_solution",
        "oom_solution": "oom_solution",
        "other_solution": "other_solution"
    }
)

graph.add_edge("npe_solution", "report")
graph.add_edge("anr_solution", "report")
graph.add_edge("oom_solution", "report")
graph.add_edge("other_solution", "report")
graph.add_edge("report", END)

# Compile
app = graph.compile()

# Run
result = app.invoke({
    "crash_log": crash_log,
    "crash_type": "",
    "severity": "",
    "relevant_docs": "",
    "solution": "",
    "report": ""
})

print(f"Crash Type : {result['crash_type']}")
print(f"Severity   : {result['severity']}")
print(f"\nSolution:\n{result['solution']}")
print(f"\nReport:\n{result['report']}")

# Report file mein save karo
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"crash_report_{timestamp}.txt"

with open(filename, "w") as file:
    file.write("=" * 50 + "\n")
    file.write("ANDROID CRASH ANALYSIS REPORT\n")
    file.write("=" * 50 + "\n\n")
    file.write(f"Timestamp  : {timestamp}\n")
    file.write(f"Crash Type : {result['crash_type']}\n")
    file.write(f"Severity   : {result['severity']}\n\n")
    file.write("SOLUTION:\n")
    file.write(result['solution'] + "\n\n")
    file.write("DETAILED REPORT:\n")
    file.write(result['report'] + "\n")

print(f"\nReport saved: {filename}")
