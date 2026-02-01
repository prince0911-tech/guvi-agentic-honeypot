from fastapi import FastAPI, Depends
from app.auth import verify_key
from app.memory import get_session
from app.detector import detect_scam
from app.agent import agent_reply
from app.intelligence import extract_intelligence
from app.callback import send_final_callback

app = FastAPI()

@app.post("/api/honeypot/message")
def honeypot(payload: dict, _: str = Depends(verify_key)):
    session_id = payload["sessionId"]
    message = payload["message"]

    session = get_session(session_id)
    session["messages"].append(message)

    extract_intelligence(message["text"], session)

    scam_result = detect_scam(message["text"])
    session["keywords"] += scam_result["keywords"]

    if scam_result["scamDetected"]:
        reply = agent_reply(message["text"], session)
    else:
        reply = "Okay"

    if not session["completed"] and (
        session["upiIds"] or session["links"] or session["phoneNumbers"]
    ):
        send_final_callback(session_id, session)
        session["completed"] = True

    return {
        "status": "success",
        "reply": reply
    }
