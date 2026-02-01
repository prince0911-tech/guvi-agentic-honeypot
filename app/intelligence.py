import re

def extract_intelligence(text: str, session: dict):
    if not text:
        return

    session["upiIds"] += re.findall(r"[a-zA-Z0-9.\-_]+@[a-zA-Z]+", text)
    session["phoneNumbers"] += re.findall(r"\+91\d{10}", text)
    session["links"] += re.findall(r"https?://\S+", text)
