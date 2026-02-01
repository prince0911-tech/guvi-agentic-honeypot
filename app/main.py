from fastapi import FastAPI, Depends, Request
from app.auth import verify_key
from app.memory import get_session
from app.detector import detect_scam
from app.agent import agent_reply
from app.intelligence import extract_intelligence
from app.callback import send_final_callback

app = FastAPI()

# --------------------------------------------------
# HEALTH / PREFLIGHT ROUTES (REQUIRED FOR TESTER)
# --------------------------------------------------

@app.get("/")
def root():
    # Tester / platform pre-check
    return {"status": "ok"}

@app.get("/api/honeypot/message")
def honeypot_get():
    # Tester sometimes sends GET before POST
    return {"status": "ok"}

# --------------------------------------------------
# MAIN HONEYPOT ENDPOINT (POST)
# --------------------------------------------------

@app.post("/api/honeypot/message")
async def honeypot(request: Request, _: str = Depends(verify_key)):
    # Safely read request body (NO validation errors)
    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    # Extract sessionId safely
    session_id = payload.get("sessionId", "tester-session")

    # Extract message safely
    message = payload.get("message", {
        "sender": "scammer",
        "text": "",
        "timestamp": None
    })

    text = message.get("text", "")

    # Session memory
    session = get_session(session_id)
    session["messages"].append(message)

    # Intelligence extraction
    extract_intelligence(text, session)

    # Scam detection
    scam_result = detect_scam(text)
    session["keywords"] += scam_result.get("keywords", [])

    # Agent reply
    if scam_result.get("scamDetected"):
        reply = agent_reply(text, session)
    else:
        reply = "Okay"

    # Mandatory final callback
    if not session["completed"] and (
        session["upiIds"] or session["links"] or session["phoneNumbers"]
    ):
        send_final_callback(session_id, session)
        session["completed"] = True

    # Required response format
    return {
        "status": "success",
        "reply": reply
    }
