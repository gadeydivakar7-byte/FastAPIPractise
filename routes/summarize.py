import os

from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
OPENAI_MODEL = "gpt-4o-mini"


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1)
    max_length: int = Field(..., ge=1)


class SummarizeResponse(BaseModel):
    summary: str


@router.post("/summarize", response_model=SummarizeResponse)
def summarize(payload: SummarizeRequest) -> SummarizeResponse:
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        raise HTTPException(
            status_code=500,
            detail="Set OPENAI_API_KEY before calling this endpoint.",
        )

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
        messages=[
                {"role": "system", "content": "You understand the text and summarize text clearly and concisely."},
                {
                    "role": "user",
                    "content": f"Summarize this text in at most {payload.max_length} characters:\n\n{payload.text}",
                },
            ],
            temperature=0.2,
        )
        summary = (completion.choices[0].message.content or "").strip()
        if not summary:
            raise HTTPException(status_code=502, detail="Empty response from OpenAI.")
        return SummarizeResponse(summary=summary[: payload.max_length])
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc}") from exc
