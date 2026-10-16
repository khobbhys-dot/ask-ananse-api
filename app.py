from fastapi import FastAPI
from pydantic import BaseModel
import os, requests

app = FastAPI()
class Req(BaseModel):
    messages: list
    model: str = "ananse"

@app.get("/")
def home():
    return {"status": "Ask Ananse API - OWN SOURCE", "owner": "HanFlo Tech"}

@app.post("/v1/chat/completions")
def chat(req: Req):
    key = os.getenv("GROQ_API_KEY")
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": "openai/gpt-oss-120b",
            "messages": [{"role":"system","content":"You are Ask Ananse, Ghanaian AI by HanFlo Tech."}, *req.messages[-10:]]
        },
        timeout=30
    )
    return r.json()
