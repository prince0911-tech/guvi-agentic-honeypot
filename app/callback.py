import requests
import os

def send_final_callback(session_id: str, session: dict):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(session["messages"]),
        "extractedIntelligence": {
            "bankAccounts": [],
            "upiIds": session["upiIds"],
            "phishingLinks": session["links"],
            "phoneNumbers": session["phoneNumbers"],
            "suspiciousKeywords": session["keywords"]
        },
        "agentNotes": "Scammer used urgency and payment redirection tactics"
    }

    try:
        requests.post(
            os.getenv("GUVI_CALLBACK"),
            json=payload,
            timeout=5
        )
    except Exception:
        pass   # Silent fail (required by spec)
