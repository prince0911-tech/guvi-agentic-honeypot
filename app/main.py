from fastapi import FastAPI, Depends, Request
from app.auth import verify_key
from app.memory import get_session
from app.detector import detect_scam
from app.agent import agent_reply
from app.intelligence import extract_intelligence
from app.callback import send_final_callback

app = FastAPI()

# Health / preflight (keep)
@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/honeypot/message")
def honeypot_get():
    return {"status": "ok"}

# ✅ REAL AGENTIC POST (MEMORY ENABLED)
@app.post("/api/honeypot/message")
async def honeypot(request: Request, _: str = Depends(verify_key)):
    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    session_id = payload.get("sessionId", "memory-test")

    message = payload.get("message", {
        "sender": "scammer",
        "text": ""
    })

    text = message.get("text", "")

    session = get_session(session_id)
    session["messages"].append(message)

    extract_intelligence(text, session)

    scam_result = detect_scam(text)
    session["keywords"] += scam_result.get("keywords", [])

    if scam_result.get("scamDetected"):
        reply = agent_reply(text, session)
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
