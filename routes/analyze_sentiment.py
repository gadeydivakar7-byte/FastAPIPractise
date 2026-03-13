import json
import os
from typing import Literal

from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
OPENAI_MODEL = "gpt-4o-mini"


class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1)


class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str


@router.post("/analyze-sentiment", response_model=SentimentResponse)
def analyze_sentiment(payload: SentimentRequest) -> SentimentResponse:
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        raise HTTPException(status_code=500, detail="Set OPENAI_API_KEY before calling this endpoint.")

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return valid JSON with keys sentiment, confidence, explanation. "
                        "sentiment must be one of positive, negative, neutral. "
                        "confidence must be a number between 0 and 1."
                    ),
                },
                {"role": "user", "content": payload.text},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        content = (completion.choices[0].message.content or "{}").strip()
        parsed = json.loads(content)

        sentiment = str(parsed.get("sentiment", "neutral")).lower()
        if sentiment not in {"positive", "negative", "neutral"}:
            sentiment = "neutral"

        confidence = float(parsed.get("confidence", 0.5))
        confidence = max(0.0, min(1.0, confidence))

        explanation = str(parsed.get("explanation", "Sentiment inferred from provided text."))

        return SentimentResponse(
            sentiment=sentiment, confidence=confidence, explanation=explanation
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc}") from exc
