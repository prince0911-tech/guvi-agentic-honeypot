def agent_reply(text: str, session: dict):
    text = text.lower()

    if "blocked" in text or "suspended" in text:
        return "Why will my account be blocked? I didn’t get any notice."

    if "upi" in text:
        return "Why do you need my UPI ID for verification?"

    if "otp" in text:
        return "I am not comfortable sharing OTP. Is there another way?"

    if "link" in text or "click" in text:
        return "Can you send the official bank link? I want to check."

    if session["upiIds"] or session["links"]:
        return "I need some time to verify this. I will get back."

    return "Can you explain this again? I am confused."
