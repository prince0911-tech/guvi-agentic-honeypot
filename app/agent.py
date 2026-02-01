def agent_reply(text: str, session: dict):
    session["turn"] += 1
    text = text.lower()

    # Stage 1: Initial confusion
    if session["stage"] == "initial":
        session["stage"] = "clarification"
        return "Why will my account be blocked? I didn’t get any notice."

    # Stage 2: Ask for proof
    if session["stage"] == "clarification":
        if "upi" in text:
            session["stage"] = "resistance"
            return "Why do you need my UPI ID for verification?"
        return "Can you explain what exactly went wrong with my account?"

    # Stage 3: Soft resistance
    if session["stage"] == "resistance":
        if "link" in text or "click" in text:
            session["stage"] = "verification"
            return "Can you send the official bank website link?"
        return "I’m not comfortable sharing details without proof."

    # Stage 4: Delay tactic
    if session["stage"] == "verification":
        return "I need some time to check this with my bank."

    # Fallback
    return "Please give me some time."
