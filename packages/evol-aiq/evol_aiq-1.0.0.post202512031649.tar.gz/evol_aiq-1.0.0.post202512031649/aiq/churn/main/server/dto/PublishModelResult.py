import logging
class PublishModelResult:
    logger = logging.getLogger(__name__)
    response_code: int = None
    response_message: str = None
    model_name: str = None
    model_version: str = None
    model_published: bool = None
    service_name: str = None

    def __init__(self):
        self.response_code = 0
        self.response_message = "success"
        pass

    def __init__(self, response_code: int, response_message: str, service_name: str, model_name: str, model_version: str, model_published: bool):
        self.response_code = response_code
        self.response_message = response_message
        self.model_name = model_name
        self.model_version = model_version
        self.model_published = model_published
        self.service_name = service_name

    def to_dict(self, api_version: str) -> dict:
        return { "response_code": self.response_code, "response_message": self.response_message, "service_name" : self.service_name, "model_name" : self.model_name, "model_version" : self.model_version, "model_published" : self.model_published, "api_version" : api_version}