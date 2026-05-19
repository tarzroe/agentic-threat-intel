from datetime import datetime
from .utils import call_gemini

def reporter_node(state):
    print("\n[Reporter] Generating final markdown report...")
    findings = state.get("findings", "")
    sector = state.get("sector", "")
    threat = state.get("threat", "")
    context = state.get("context", "")
    today_date = datetime.now().strftime("%B %d, %Y")

    system_instruction = '''
    You are an expert Defensive Cybersecurity Analyst.
    CRITICAL RULES:
    - Defensive-Only: NEVER generate exploit code or Proof of Concepts (PoCs).
    - Format the report using the Diamond Model of Intrusion Analysis.
    - Map vulnerabilities to specific CWE IDs AND MITRE ATT&CK Tactics/Techniques.
    - Start the Executive Summary with a BLUF (Bottom Line Up Front).
    - Provide clear remediation strategies, strictly categorized as [IMMEDIATE], [SHORT-TERM], and [ONGOING].
    '''

    prompt = f'''
    Based on the verified findings below for {threat} targeting {sector} (Environment: {context}), generate a comprehensive threat intelligence report.
    CURRENT DATE: {today_date}
    Verified Findings:
    {findings}
    '''

    report = call_gemini(prompt, system_instruction=system_instruction)
    state["final_report"] = report
    state["report"] = report
    state["messages"].append({"role": "reporter", "content": "Report generated successfully."})
    return state
