import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config.settings import settings
from app.api.routes import health, readiness, inference, repository
from app.inference.loader import initialize_model

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("aevor-ai")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info(f"Starting Aevor AI Service in {settings.APP_ENV} mode...")
    logger.info(f"Configuration settings loaded successfully. Model Name: {settings.MODEL_NAME}")
    try:
        initialize_model()
    except Exception as e:
        logger.error(f"Failed to initialize model: {str(e)}", exc_info=True)
    yield
    # Shutdown logic
    logger.info("Shutting down Aevor AI Service...")

# Initialize FastAPI App
app = FastAPI(
    title="Aevor AI Microservice",
    description="Dedicated microservice for executing AI/ML tasks.",
    version="1.0.0",
    lifespan=lifespan
)

# Custom Exception Handler to return structured errors as requested in specifications
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred on the server."
            }
        }
    )

# Register routes
app.include_router(health.router)
app.include_router(readiness.router)
app.include_router(inference.router, prefix="/api/v1")
app.include_router(repository.router, prefix="/api/v1")


