from fastapi import APIRouter
from app.inference.loader import get_model

router = APIRouter()

@router.get("/ready", tags=["Lifecycle"])
def check_readiness():
    """
    Readiness check endpoint.
    Answers: Is the AI service capable of handling requests?
    """
    try:
        model = get_model()
        if model.is_ready:
            return {"status": "ready"}
    except Exception:
        pass
    return {"status": "not_ready"}

