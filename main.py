from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from routes.analyze_sentiment import router as analyze_sentiment_router
from routes.health import router as health_router
from routes.summarize import router as summarize_router

app = FastAPI()

app.include_router(health_router)
app.include_router(summarize_router)
app.include_router(analyze_sentiment_router)
