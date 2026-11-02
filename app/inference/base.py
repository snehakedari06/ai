from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Abstract base class representing an AI/ML Model Interface.
    Allows swapping model implementations without changing API routing code.
    """

    @abstractmethod
    def load(self) -> None:
        """
        Loads the model weights and initializes the model.
        Should be called during service startup.
        """
        pass

    @abstractmethod
    def predict(self, text: str, options: dict) -> dict:
        """
        Executes model inference on the provided input text.
        """
        pass

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        """
        Returns True if the model is loaded and ready for inference, False otherwise.
        """
        pass
