import json
import os
from tavily import TavilyClient
from .utils import call_gemini

tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def scout_node(state):
    print("\n[Scout] Gathering OSINT data...")
    sector = state.get("sector", "")
    threat = state.get("threat", "")
    context = state.get("context", "")

    query = f"Recent threat intelligence, {threat} active campaigns and vulnerabilities targeting {sector} using {context}"

    try:
        search_result = tavily_client.search(query=query, search_depth="advanced", max_results=5)
        results_str = json.dumps(search_result.get('results', []), indent=2)

        prompt = f'''
        You are an expert OSINT Gatherer. Analyze the following search results for threats targeting {sector} specifically regarding {threat}.
        Focus your extraction on the following technical environment: {context}.
        Please extract and structure the data into the following categories:
        1. **Active Campaigns & Threat Actors:** Names of groups or campaigns currently active.
        2. **Technical TTPs & Vulnerabilities:** Specific CVEs, attack vectors, and technical methods used.
        3. **Indicators of Compromise (IOCs):** Defang any malicious URLs, domains, or IPs.
        4. **Potential Impacts:** Operational, data, and financial risks.
        CRITICAL RULES:
        - REDACT any legitimate PII.
        - CITATION REQUIREMENT: Append source URL using format [Source: URL].
        - DO NOT include findings without source URLs.
        Search Results:
        {results_str}
        '''
        findings = call_gemini(prompt)
        state["findings"] = findings
        state["messages"].append({"role": "scout", "content": "Gathered and structured raw findings with citations."})
    except Exception as e:
        state["findings"] = f"Error during Scout phase: {str(e)}"
        state["messages"].append({"role": "scout", "content": "Failed to gather data."})
    return state
