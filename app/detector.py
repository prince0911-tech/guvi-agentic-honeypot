SCAM_KEYWORDS = [
    "urgent", "verify", "blocked", "suspended",
    "upi", "otp", "account", "click"
]

def detect_scam(text):
    found = [k for k in SCAM_KEYWORDS if k in text.lower()]
    return {
        "scamDetected": len(found) > 0,
        "keywords": found
    }
