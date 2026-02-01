SCAM_KEYWORDS = [
    "urgent", "verify", "blocked", "suspended",
    "upi", "otp", "account", "click"
]

def detect_scam(text: str):
    text = text.lower()
    found = [k for k in SCAM_KEYWORDS if k in text]
    return {
        "scamDetected": len(found) > 0,
        "keywords": found
    }
