import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from datetime import datetime
from state import CrashState
from constants import (
    CLASSIFY_SYSTEM, CLASSIFY_HUMAN,
    NPE_SYSTEM, NPE_HUMAN,
    ANR_SYSTEM, ANR_HUMAN,
    OOM_SYSTEM, OOM_HUMAN,
    OTHER_SYSTEM, OTHER_HUMAN,
    REPORT_SYSTEM, REPORT_HUMAN,
    SEVERITY_NPE, SEVERITY_ANR,
    SEVERITY_OOM, SEVERITY_OTHER,
    KNOWLEDGE_BASE_DIR, REPORT_PREFIX
)

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory=KNOWLEDGE_BASE_DIR,
    embedding_function=embeddings
)

def run_chain(system_msg, human_msg, variables):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human", human_msg)
    ])
    return (prompt | llm).invoke(variables).content

def classify_crash(state: CrashState):
    return {"crash_type": run_chain(
        CLASSIFY_SYSTEM, CLASSIFY_HUMAN,
        {"crash_log": state["crash_log"]}
    )}

def search_docs(state: CrashState):
    docs = vectorstore.similarity_search(state["crash_type"], k=1)
    return {"relevant_docs": docs[0].page_content if docs else "No docs found"}

def route_crash(state: CrashState):
    crash = state["crash_type"].strip()
    if "NPE" in crash:   return "npe_solution"
    elif "ANR" in crash: return "anr_solution"
    elif "OOM" in crash: return "oom_solution"
    else:                return "other_solution"

def npe_solution(state: CrashState):
    return {"severity": SEVERITY_NPE, "solution": run_chain(
        NPE_SYSTEM, NPE_HUMAN,
        {"crash_log": state["crash_log"], "relevant_docs": state["relevant_docs"]}
    )}

def anr_solution(state: CrashState):
    return {"severity": SEVERITY_ANR, "solution": run_chain(
        ANR_SYSTEM, ANR_HUMAN,
        {"crash_log": state["crash_log"], "relevant_docs": state["relevant_docs"]}
    )}

def oom_solution(state: CrashState):
    return {"severity": SEVERITY_OOM, "solution": run_chain(
        OOM_SYSTEM, OOM_HUMAN,
        {"crash_log": state["crash_log"], "relevant_docs": state["relevant_docs"]}
    )}

def other_solution(state: CrashState):
    return {"severity": SEVERITY_OTHER, "solution": run_chain(
        OTHER_SYSTEM, OTHER_HUMAN,
        {"crash_log": state["crash_log"], "relevant_docs": state["relevant_docs"]}
    )}

def generate_report(state: CrashState):
    return {"report": run_chain(
        REPORT_SYSTEM, REPORT_HUMAN,
        {"crash_type": state["crash_type"],
         "severity": state["severity"],
         "solution": state["solution"]}
    )}

@st.cache_resource
def build_graph():
    graph = StateGraph(CrashState)
    for name, fn in [
        ("classify",       classify_crash),
        ("search_docs",    search_docs),
        ("npe_solution",   npe_solution),
        ("anr_solution",   anr_solution),
        ("oom_solution",   oom_solution),
        ("other_solution", other_solution),
        ("report",         generate_report),
    ]:
        graph.add_node(name, fn)
    graph.set_entry_point("classify")
    graph.add_edge("classify", "search_docs")
    graph.add_conditional_edges("search_docs", route_crash, {
        "npe_solution":   "npe_solution",
        "anr_solution":   "anr_solution",
        "oom_solution":   "oom_solution",
        "other_solution": "other_solution"
    })
    for node in ["npe_solution", "anr_solution", "oom_solution", "other_solution"]:
        graph.add_edge(node, "report")
    graph.add_edge("report", END)
    return graph.compile()

agent = build_graph()

def severity_color(severity):
    return {
        "LOW":     "🟢 LOW",
        "MEDIUM":  "🟡 MEDIUM",
        "HIGH":    "🔴 HIGH",
        "UNKNOWN": "⚪ UNKNOWN"
    }.get(severity, severity)

def crash_color(crash_type):
    return {
        "NPE": "🔵 NPE",
        "ANR": "🟠 ANR",
        "OOM": "🔴 OOM",
    }.get(crash_type.strip(), f"⚪ {crash_type}")

st.set_page_config(
    page_title="Android Debugging AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Android Debugging AI Agent")
st.markdown("**AI-powered crash analyzer — Built by Nitesh Khosla | 13+ Years Android Expert**")
st.divider()

crash_log = st.text_area(
    "📋 Paste your Android Crash Log here:",
    height=200,
    placeholder="""AndroidRuntime: FATAL EXCEPTION: main
Process: com.example.app
java.lang.NullPointerException
at MainActivity.onCreate(MainActivity.kt:42)"""
)

if st.button("🔍 Analyze Crash", type="primary", use_container_width=True):
    if not crash_log.strip():
        st.error("⚠️ Please paste a crash log first!")
    else:
        with st.spinner("🤖 AI Agents analyzing your crash..."):
            result = agent.invoke({
                "crash_log":     crash_log,
                "crash_type":    "",
                "severity":      "",
                "relevant_docs": "",
                "solution":      "",
                "report":        ""
            })

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🐛 Crash Type", crash_color(result['crash_type']))
        with col2:
            st.metric("⚠️ Severity", severity_color(result['severity']))

        st.divider()

        st.subheader("💡 Solution")
        st.markdown(result['solution'])

        st.divider()

        st.subheader("📊 Detailed Report")
        st.markdown(result['report'])

        st.divider()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        report_content = f"""
{'='*50}
ANDROID CRASH ANALYSIS REPORT
{'='*50}

Timestamp  : {timestamp}
Crash Type : {result['crash_type']}
Severity   : {result['severity']}

SOLUTION:
{result['solution']}

DETAILED REPORT:
{result['report']}
"""
        st.download_button(
            label="💾 Download Report",
            data=report_content,
            file_name=f"{REPORT_PREFIX}{timestamp}.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.success("✅ Analysis Complete!")
