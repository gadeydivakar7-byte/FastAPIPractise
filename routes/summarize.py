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
                        "You are an expert text compression and summarization assistant. "
                        "Your task is to produce extremely information-dense summaries while "
                        "preserving all critical facts from the source text.\n\n"
                        "Prioritize keeping:\n"
                        "- Named entities (people, organizations, locations)\n"
                        "- Dates, times, numbers, and statistics\n"
                        "- Key actions, decisions, and outcomes\n"
                        "- Important relationships between entities\n\n"
                        "Compression strategy:\n"
                        "- Remove filler words, redundancy, and stylistic language\n"
                        "- Replace long phrases with shorter equivalents\n"
                        "- Use compact phrasing and punctuation when helpful\n"
                        "- Avoid repeating the same idea\n"
                        "- Never invent information not present in the text\n"
                        "Output requirements:\n"
                        "- Return ONLY the summary text\n"
                        "- No explanations or prefixes\n"
                        "- The summary MUST respect the character limit"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Summarize the following text in <= {payload.max_length} characters.\n\n"
                        "Rules:\n"
                        "1. Preserve maximum factual information.\n"
                        "2. Keep names, numbers, dates, and outcomes whenever possible.\n"
                        "3. Use compact wording to maximize information density.\n"
                        "4. Do not exceed the character limit.\n"
                        "5. If the limit is very small, prioritize the most critical facts.\n\n"
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
