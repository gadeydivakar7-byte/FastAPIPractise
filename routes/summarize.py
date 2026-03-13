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
                {
                    "role": "system",
                    "content": (
                        "You are a precise text summarization assistant. "
                        "Your goal is to compress text while preserving maximum factual information. "
                        "Always prioritize retaining key entities (people, organizations, places), "
                        "dates, numbers, metrics, decisions, and outcomes. "
                        "Remove redundancy, filler words, and less important descriptions, "
                        "but never omit critical facts."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Summarize the text below in **no more than {payload.max_length} characters**.\n\n"
                        "Rules:\n"
                        "1. Preserve important facts, names, numbers, and outcomes.\n"
                        "2. Prefer concise phrasing and information-dense wording.\n"
                        "3. Do not invent or infer information not present in the text.\n"
                        "4. If necessary, shorten wording but keep all critical details.\n"
                        "5. Ensure the final output does not exceed the character limit.\n\n"
                        "Text:\n"
                        f"{payload.text}"
                    ),
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
