from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph,END
from typing import TypedDict
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile")

# File se crash log padhna
with open("crash_log.txt", "r") as file:
     crash_log = file.read()

print("✅ Crash log loaded!")
print(f"Log size: {len(crash_log)} characters\n")


# RAG - Knowledge Base load karo
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="./android_knowledge",
    embedding_function=embeddings
)

# State - saare agents ka shared data
class CrashState(TypedDict):
      crash_log:str
      crash_type:str
      solution:str
      report: str
      relevant_docs: str
    
    
# Node 1 - Crash classify karo
def Classify_crash(state:CrashState):
    prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are an Android expert. Classify the crash type only in one word: NPE, ANR, OOM, or OTHER."),
        ("human", "Classify this crash: {crash_log}")
    ])
        
    chain =prompt|llm
    result=chain.invoke({"crash_log":state['crash_log']})
    return {"crash_type": result.content}


# Node 2-Solution
def suggest_solution(state:CrashState):
    prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are an Android expert. Give a short Kotlin fix."),
        ("human","Crash type is {crash_type}. Give fix.")
    ])
    
    chain=prompt|llm
    result=chain.invoke({"crash_type",state['crash_type']})
    return {"solution":result.content}


# RAG Node - Docs search karo
def search_docs(state:CrashState):
    docs=vectorstore.similarity_search(state["crash_type"], k=1)
    relevant=docs[0].page_content if(docs) else "No docs found"
    return {"relevant_docs":relevant}



# Node 3-Report Generator
def report_generator(state:CrashState):
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system","""You are an Android expert. 
                    Generate a professional crash analysis report in table format.
                    Include: Crash Type, Severity, Root Cause, Solution, Prevention."""),
            
            ("human","""Generate report for:
                        Crash Type: {crash_type}
                        Solution: {solution}""")
        ])
    
    chain=prompt|llm    
    result = chain.invoke({
        "crash_type": state["crash_type"],
        "solution": state["solution"]
    })
    return {"report":result.content}
    
# Graph banao
graph=StateGraph(CrashState)

graph.add_node("classify",Classify_crash)
graph.add_node("search_docs", search_docs)
graph.add_node("solution",suggest_solution)
graph.add_node("report",report_generator)

graph.set_entry_point("classify")
graph.add_edge("classify", "search_docs")
graph.add_edge("search_docs", "solution")
graph.add_edge("solution", "report")
graph.add_edge("report", END)
    
# Compile karo
app=graph.compile()
    
# Run karo
result=app.invoke(
{
"crash_log": crash_log,
"crash_type": "",
"solution": "",
"report": "",
"relevant_docs": "",
})
    
print(f"Crash Type: {result['crash_type']}")
print(f"Solution:{result['solution']}")
print(f"\nReport:\n{result['report']}")
print(f"\nRelevant Docs: {result['relevant_docs']}")
