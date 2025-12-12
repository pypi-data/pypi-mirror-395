import logging
class LoadModelResult:
    logger = logging.getLogger(__name__)
    response_code: int = None
    response_message: str = None
    service_name: str = None
    model_name: str = None
    model_version: str = None
    model_loaded: bool = None

    def __init__(self, response_code: int, response_message: str, service_name: str, model_name: str, model_version: str, model_loaded: bool):
        self.response_code = response_code
        self.response_message = response_message
        self.service_name = service_name
        self.model_name = model_name
        self.model_version = model_version
        self.model_loaded = model_loaded

    def to_dict(self, api_version: str) -> dict:
        return {
            "api_version": api_version,
            "response_code": self.response_code,
            "response_message": self.response_message,
            "service_name": self.service_name,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "model_loaded": self.model_loaded
        }