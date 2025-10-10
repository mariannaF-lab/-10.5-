from fastapi import FastAPI, Query, HTTPException
# ...
@app.get("/generate")
def generate(topic: str | None = Query(default=None), max_tokens: int = 1600):
    try:
        # ...
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
