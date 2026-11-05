import os
import random
from typing import Optional

from fastapi import FastAPI, Query, HTTPException, Header
from generator import generate_post
from access_control import authorized, reserve_quota

app = FastAPI()

DEFAULT_TOPICS = [t.strip() for t in os.getenv("TOPICS", "").split("|") if t.strip()]

@app.get("/")
def root():
    return {
        "ok": True,
        "message": "TG Post Generator is running",
        "routes": ["/health", "/generate", "/docs"],
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/generate")
def generate(topic: Optional[str] = Query(default=None, max_length=500), max_tokens: int = Query(default=1600, ge=1, le=1600), authorization: Optional[str] = Header(default=None)):
    if not authorized(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        allowed = reserve_quota(os.getenv("QUOTA_DB_PATH", "quota.sqlite3"))
    except Exception:
        raise HTTPException(status_code=503, detail="Quota storage unavailable") from None
    if not allowed:
        raise HTTPException(status_code=429, detail="Generation quota exceeded")
    try:
        chosen = topic or (random.choice(DEFAULT_TOPICS) if DEFAULT_TOPICS else "рыба в озере Ханка")
        data = generate_post(chosen, max_tokens=max_tokens)
        data["topic"] = chosen
        return data
    except Exception as e:
        # отдаём понятную 500 вместо падения приложения
        raise HTTPException(status_code=502, detail="Generation failed") from None


