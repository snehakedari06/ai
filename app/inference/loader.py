import logging
from app.config.settings import settings
from app.inference.base import BaseModel
from app.inference.dummy import DummyModel

logger = logging.getLogger("aevor-ai")

# Global model instance
_model_instance = None

def get_model() -> BaseModel:
    """
    Returns the initialized active model instance.
    Raises RuntimeError if the model is not yet initialized.
    """
    global _model_instance
    if _model_instance is None:
        raise RuntimeError("Model is not initialized. Call initialize_model() first.")
    return _model_instance

def set_model(model: BaseModel) -> None:
    """
    Manually set the global model instance (primarily used for unit testing).
    """
    global _model_instance
    _model_instance = model

def initialize_model() -> None:
    """
    Initializes and loads the model based on configuration settings.
    """
    global _model_instance
    model_name = settings.MODEL_NAME
    logger.info(f"Loading configured model: {model_name}")

    if model_name == "dummy-model":
        model = DummyModel()
        model.load()
        _model_instance = model
    else:
        logger.error(f"Unknown model configuration: {model_name}")
        raise ValueError(f"Unknown model configuration: {model_name}")
