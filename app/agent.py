def agent_reply(message_text, session):
    text = message_text.lower()

    if "blocked" in text or "suspended" in text:
        return "Why will my account be blocked? I didn’t get any notice."

    if "upi" in text:
        return "Why do you need my UPI ID for verification?"

    if "otp" in text:
        return "I’m not comfortable sharing OTP. Is there another way?"

    if "link" in text or "click" in text:
        return "Can you send the official link from the bank website?"

    if session["upiIds"] or session["links"]:
        return "I need some time to check this. I will get back."

    return "Can you explain this again? I’m confused."
