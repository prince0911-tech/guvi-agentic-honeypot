sessions = {}

def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "upiIds": [],
            "phoneNumbers": [],
            "links": [],
            "keywords": [],
            "turn": 0,                 # 👈 NEW
            "stage": "initial",        # 👈 NEW
            "completed": False
        }
    return sessions[session_id]
