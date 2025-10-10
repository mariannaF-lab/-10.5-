import os, random
from typing import Optional
from fastapi import FastAPI, Query
from generator import generate_post

app = FastAPI()

DEFAULT_TOPICS = [t.strip() for t in os.getenv("TOPICS", "").split("|") if t.strip()]

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/generate")
def generate(topic: Optional[str] = Query(default=None), max_tokens: int = 1600):
    chosen = topic or (random.choice(DEFAULT_TOPICS) if DEFAULT_TOPICS else "рыба в озере Ханка")
    data = generate_post(chosen, max_tokens=max_tokens)
    data["topic"] = chosen
    return data


from fastapi import FastAPI, Query, HTTPException
# ...
@app.get("/generate")
def generate(topic: str | None = Query(default=None), max_tokens: int = 1600):
    try:
        # ...
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
