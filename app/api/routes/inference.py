import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.inference.loader import get_model
from app.inference.base import BaseModel as AbstractBaseModel

logger = logging.getLogger("aevor-ai")
router = APIRouter()

class InferenceRequest(BaseModel):
    input: str = Field(..., min_length=1, description="Source content or query for the model.")
    options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Model parameter overrides.")

class InferenceResponse(BaseModel):
    result: str
    metadata: Dict[str, Any]

@router.post("/inference", response_model=InferenceResponse, tags=["Inference"])
async def run_inference(
    request: InferenceRequest,
    model: AbstractBaseModel = Depends(get_model)
):
    """
    Executes model inference on the provided input text.
    """
    if not model.is_ready:
        logger.error("Inference requested but model is not ready.")
        return JSONResponse(
            status_code=503,
            content={
                "error": {
                    "code": "MODEL_UNAVAILABLE",
                    "message": "AI model is currently unavailable"
                }
            }
        )

    try:
        options = request.options or {}
        prediction = model.predict(request.input, options)
        return prediction
    except Exception as e:
        logger.error(f"Error during model inference: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INFERENCE_FAILED",
                    "message": f"Inference execution failed: {str(e)}"
                }
            }
        )
