from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph,END
from typing import TypedDict

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile")

# State - saare agents ka shared data
class CrashState(TypedDict):
      crash_log:str
      crash_type:str
      solution:str
      report: str
    
    
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
graph.add_node("solution",suggest_solution)
graph.add_node("report",report_generator)

graph.set_entry_point("classify")
graph.add_edge("classify","solution")
graph.add_edge("solution", "report")
graph.add_edge("report", END)
    
# Compile karo
app=graph.compile()
    
# Run karo
result=app.invoke(
{
"crash_log": """
java.lang.OutOfMemoryError"
"ANR in com.example.app
""",
"crash_type": "",
"solution": "",
"report": ""
})
    
print(f"Crash Type: {result['crash_type']}")
print(f"Solution:{result['solution']}")
print(f"\nReport:\n{result['report']}")
