from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Ask Ananse API - OWN SOURCE", "owner": "HanFlo Tech"}

@app.post("/v1/chat/completions")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"choices": [{"message": {"content": "ERROR: GROQ_API_KEY not set on Render Environment"}}]}

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="  model = "openai/gpt-oss-20b",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        content = completion.choices[0].message.content
        return {
            "choices": [{"message": {"content": content}}]
        }
    except Exception as e:
        # This will show REAL error in logs and frontend
        error_msg = f"GROQ ERROR: {str(e)}"
        print(error_msg)
        return {"choices": [{"message": {"content": error_msg}}]}
