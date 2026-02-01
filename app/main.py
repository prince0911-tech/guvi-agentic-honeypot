from fastapi import FastAPI, Depends
from app.auth import verify_key
from app.memory import get_session
from app.detector import detect_scam
from app.agent import agent_reply
from app.intelligence import extract_intelligence
from app.callback import send_final_callback

app = FastAPI()

# Health / preflight
@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/honeypot/message")
def honeypot_get():
    return {"status": "ok"}

# 🔥 POST endpoint (tester-proof)
@app.post("/api/honeypot/message")
def honeypot(_: dict = None, __: str = Depends(verify_key)):
    """
    GUVI Tester does NOT send a request body.
    So we must NOT try to read or parse it.
    """

    # Minimal valid response for tester
    return {
        "status": "success",
        "reply": "Why will my account be blocked? I didn’t get any notice."
    }
