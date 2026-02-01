import requests
import os

def send_final_callback(session_id, session):
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
        "agentNotes": "Scammer used urgency and payment request tactics"
    }

    requests.post(
        os.getenv("GUVI_CALLBACK"),
        json=payload,
        timeout=5
    )
