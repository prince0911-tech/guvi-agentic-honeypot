from fastapi import FastAPI, Depends, Body
from app.auth import verify_key
from app.memory import get_session
from app.detector import detect_scam
from app.agent import agent_reply
from app.intelligence import extract_intelligence
from app.callback import send_final_callback

app = FastAPI()

@app.post("/api/honeypot/message")
def honeypot(payload: dict = Body(default={}), _: str = Depends(verify_key)):
    # TOLERANT PAYLOAD HANDLING (tester-proof)
    session_id = payload.get("sessionId", "tester-session")

    message = payload.get("message", {
        "sender": "scammer",
        "text": "",
        "timestamp": None
    })

    text = message.get("text", "")

    session = get_session(session_id)
    session["messages"].append(message)

    extract_intelligence(text, session)

    scam_result = detect_scam(text)
    session["keywords"] += scam_result["keywords"]

    if scam_result["scamDetected"]:
        reply = agent_reply(text, session)
    else:
        reply = "Okay"

    # Mandatory callback trigger
    if not session["completed"] and (
        session["upiIds"] or session["links"] or session["phoneNumbers"]
    ):
        send_final_callback(session_id, session)
        session["completed"] = True

    return {
        "status": "success",
        "reply": reply
    }
