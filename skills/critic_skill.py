from .utils import call_gemini

def critic_node(state):
    print("\n[Critic] Analyzing findings (Two-Source Rule)...")
    findings = state.get("findings", "")
    sector = state.get("sector", "")
    threat = state.get("threat", "")

    if findings.startswith("Error"):
        state["messages"].append({"role": "critic", "content": "Bypassed due to Scout error."})
        state["is_verified"] = False
        state["retry_count"] = state.get("retry_count", 0) + 1
        return state

    prompt = f'''
    Review the following OSINT findings for {threat} in the {sector} sector.
    Apply the 'Two-Source Rule': Determine if the key threat indicators are corroborated by at least TWO independent and distinct source domains.
    You must output your final decision exactly as either:
    FINAL_VERDICT: VERIFIED
    or
    FINAL_VERDICT: UNVERIFIED
    Findings:
    {findings}
    '''
    analysis = call_gemini(prompt)
    state["messages"].append({"role": "critic", "content": analysis})

    if "FINAL_VERDICT: VERIFIED" in analysis.upper():
        state["is_verified"] = True
        print("[Critic] Status: VERIFIED")
    else:
        state["is_verified"] = False
        state["retry_count"] = state.get("retry_count", 0) + 1
        print("[Critic] Status: UNVERIFIED. Needs more data.")

    return state
