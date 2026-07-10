from fastapi import FastAPI
from app.api.routes import router
from app.api.portfolio import router as portfolio_router

from app.core.model_loader import model_loader
from app.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

app =  FastAPI(
    title = "CredPulse API",
    description= "AI-powered MSME Credit Risk Assessment and Financial Health Scoring API",
    version="1.0.0"
)
    
@app.on_event("startup")
async def startup():
    logger.info("Starting CredPulse API...")

    model_loader.load()

    logger.info("Models loaded successfully.")

app.include_router(router)
app.include_router(portfolio_router)

@app.get('/')
def home():
    logger.info("Home endpoint called")
    return {
        "message": "Welcome to CredPulse API",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
