# app_hello.py
from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def health():
    return {"ok": True, "app": "hello"}
