from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Lifecycle"])
def check_health():
    """
    Lightweight health check endpoint.
    Answers: Is the service process alive?
    """
    return {"status": "ok"}
