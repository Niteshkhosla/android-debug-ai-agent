
# ─── CLASSIFY ───
CLASSIFY_SYSTEM = """You are an Android expert. 
Classify crash into EXACTLY one: NPE, ANR, OOM, OTHER. 
Reply one word only."""
CLASSIFY_HUMAN = "Classify this crash: {crash_log}"

# ─── NPE ───
NPE_SYSTEM = "You are Android expert. Fix NPE using Kotlin safe operators."
NPE_HUMAN = "Fix NPE crash: {crash_log}\nDocs: {relevant_docs}"

# ─── ANR ───
ANR_SYSTEM = "You are Android expert. Fix ANR using Coroutines and async."
ANR_HUMAN = "Fix ANR crash: {crash_log}\nDocs: {relevant_docs}"

# ─── OOM ───
OOM_SYSTEM = "You are Android expert. Fix OOM using memory management."
OOM_HUMAN = "Fix OOM crash: {crash_log}\nDocs: {relevant_docs}"

# ─── OTHER ───
OTHER_SYSTEM = "You are Android expert. Analyze and fix this crash."
OTHER_HUMAN = "Fix crash: {crash_log}\nDocs: {relevant_docs}"

# ─── REPORT ───
REPORT_SYSTEM = """You are Android expert. 
Generate professional crash report in table format.
Include: Crash Type, Severity, Root Cause, Solution, Prevention."""
REPORT_HUMAN = """Generate report for:
Crash Type: {crash_type}
Severity: {severity}
Solution: {solution}"""

# ─── SEVERITY ───
SEVERITY_NPE   = "LOW"
SEVERITY_ANR   = "MEDIUM"
SEVERITY_OOM   = "HIGH"
SEVERITY_OTHER = "UNKNOWN"

# ─── FILES ───
CRASH_LOG_FILE     = "crash_log.txt"
KNOWLEDGE_BASE_DIR = "./android_knowledge"
REPORT_PREFIX      = "crash_report_"
