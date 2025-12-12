from abc import abstractmethod, ABC
import logging

class ModelDataGenerator(ABC):
    logger = logging.getLogger(__name__)
    def __init__(self):
        pass

    @abstractmethod
    def generate_model_readable_data(self, data: dict) -> dict | None:
        pass
