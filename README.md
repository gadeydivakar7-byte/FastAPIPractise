# FirstAIApp

A minimal FastAPI service with OpenAI-powered text processing.

## Features

- `GET /health` - health check with current UTC timestamp
- `POST /summarize` - summarize text with a character limit
- `POST /analyze-sentiment` - returns sentiment, confidence, and explanation

## Project Structure

```text
FirstAIApp/
  main.py
  .env
  routes/
    health.py
    summarize.py
    analyze_sentiment.py
```

## Prerequisites

- Python 3.10+ (you are currently using a virtual environment, recommended)
- OpenAI API key

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn openai python-dotenv
```

3. Configure environment variables in `.env`:

```env
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
```

Replace the placeholder with your real API key.

## Run the App

```bash
uvicorn main:app --reload
```

App URL: `http://127.0.0.1:8000`

Interactive docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### 1) Health Check

- Method: `GET`
- Path: `/health`
- Response:

```json
{
  "status": "ok",
  "timestamp": "2026-03-11T12:34:56.789012+00:00"
}
```

### 2) Summarize Text

- Method: `POST`
- Path: `/summarize`
- Request body:

```json
{
  "text": "Your long input text goes here...",
  "max_length": 300
}
```

- Response body:

```json
{
  "summary": "Concise summary text..."
}
```

### 3) Analyze Sentiment

- Method: `POST`
- Path: `/analyze-sentiment`
- Request body:

```json
{
  "text": "I love how simple and fast this setup is."
}
```

- Response body:

```json
{
  "sentiment": "positive",
  "confidence": 0.94,
  "explanation": "The text uses strongly positive words and tone."
}
```

## cURL Examples

Health:

```bash
curl http://127.0.0.1:8000/health
```

Summarize:

```bash
curl -X POST "http://127.0.0.1:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text":"FastAPI is a modern Python web framework for building APIs quickly.","max_length":120}'
```

Analyze sentiment:

```bash
curl -X POST "http://127.0.0.1:8000/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text":"This app is very useful and easy to use."}'
```

## Notes

- If `OPENAI_API_KEY` is missing or still set to placeholder, NLP endpoints return an error.
- `GET /` is not defined in this project, so opening the root URL returns `404 Not Found` (expected).
