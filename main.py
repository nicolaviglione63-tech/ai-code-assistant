from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import json
from fastapi.responses import FileResponse
import os

app = FastAPI()

# 🔑 Inserisci la tua API key qui
client = OpenAI(
    api_key="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"
)


@app.get("/")
def serve_frontend():
    path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(path)


# 📦 Modello richiesta
class CodeRequest(BaseModel):
    code: str


# 🚀 Endpoint
@app.post("/review")
async def review_code(request: CodeRequest):

    prompt = (
        """
You are a strict senior code reviewer.

Analyze the code and return ONLY valid JSON.

Be precise and short.

Return this structure:
{
  "bugs": [],
  "performance": [],
  "security": [],
  "improvements": [],
  ""line_issues": [
    {
      "line": 0,
      "issue": ""
    }
  ],
  "score": 0,
  "summary": ""
}

Rules:
- Max 1 sentence per item
- No duplicates
- score from 0 to 10

Code:
"""
        + request.code
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content

        # 🔍 Prova a leggere JSON
        try:
            parsed = json.loads(content)
        except Exception:
            parsed = {
                "bugs": [],
                "performance": [],
                "security": [],
                "improvements": [],
                "line_issues": [],
                "score": 0,
                "summary": content,
            }

        return parsed

    except Exception as e:
        return {"error": str(e)}
