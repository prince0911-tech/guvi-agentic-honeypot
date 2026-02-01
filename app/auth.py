from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def verify_key(x_api_key: str = Header(...)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
