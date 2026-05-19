import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv

import google.generativeai as genai

from skills.scout_skill import scout_node
from skills.critic_skill import critic_node
from skills.reporter_skill import reporter_node
from skills.utils import call_gemini

basedir = Path(__file__).resolve().parent.parent
env_file = basedir / ".env"
if env_file.exists():
    load_dotenv(env_file)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def parse_query(query: str) -> dict:
    prompt = f'''
    Extract the following from this OSINT query and return ONLY a JSON object with no markdown, no backticks, no extra text:
    {{
        "sector": "the industry or sector being targeted (e.g. healthcare, finance, energy)",
        "threat": "the specific threat or malware or attack type mentioned",
        "context": "the technical environment or additional context"
    }}

    Query: {query}
    '''
    raw = call_gemini(prompt)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"sector": "general", "threat": query, "context": "general"}

def run_agent_workflow(report_id: int, query: str, db_session=None) -> str:
    parsed = parse_query(query)
    sector = parsed.get("sector", "general")
    threat = parsed.get("threat", query)
    context = parsed.get("context", "general")

    def update_phase(phase: str):
        if db_session and report_id:
            from backend.models import OSINTReport
            report = db_session.query(OSINTReport).filter(OSINTReport.id == report_id).first()
            if report:
                report.phase = phase
                db_session.commit()

    state = {
        "sector": sector,
        "threat": threat,
        "context": context,
        "messages": [],
        "findings": "",
        "is_verified": False,
        "retry_count": 0
    }

    max_retries = 2
    while not state["is_verified"] and state["retry_count"] <= max_retries:
        if state["retry_count"] > 0:
            time.sleep(2)
        update_phase("scouting")
        state = scout_node(state)
        update_phase("critiquing")
        state = critic_node(state)

    if state["is_verified"]:
        update_phase("reporting")
        state = reporter_node(state)
        update_phase("completed")
        return state.get("final_report") or state.get("report", "No report generated.")
    else:
        update_phase("failed")
        return "Failed to verify threat indicators across multiple sources after maximum retries."
