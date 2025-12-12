import logging

class StartTrainResult:
    logger = logging.getLogger(__name__)
    response_code: int = None
    response_message: str = None

    def __init__(self):
        self.response_code = 0
        self.response_message = "success"
        pass

    def __init__(self, response_code: int, response_message: str):
        self.response_code = response_code
        self.response_message = response_message

    def to_dict(self, api_version: str) -> dict:
        return {"response_code" : self.response_code, "response_message" : self.response_message, "api_version" : api_version}