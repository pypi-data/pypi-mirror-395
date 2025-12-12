import logging
from typing import List, Any, Dict


class PredictionResult:
    logger = logging.getLogger(__name__)
    response_code: int = None
    response_message: str = None
    results: List[Dict[str, Any]] = None

    def __init__(self, response_code: str, response_message: str, results: List[Dict[str, Any]]):
        self.response_code = response_code
        self.response_message = response_message
        self.results = results

    def to_dict(self, api_version: str) -> dict:
        return {"results" : self.results, "response_code" : self.response_code, "response_message" : self.response_message, "api_version" : api_version}