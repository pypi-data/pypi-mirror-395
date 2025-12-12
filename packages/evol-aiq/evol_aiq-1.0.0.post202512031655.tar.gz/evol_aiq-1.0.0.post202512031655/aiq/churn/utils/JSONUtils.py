from datetime import datetime
from typing import Dict, Any, List

class JSONUtils:
    @staticmethod
    def decode_str(data: Dict[str, Any], key: str, default: str = "") -> str:
        value = data.get(key, default)
        if not isinstance(value, str):
            raise TypeError(f"{key} must be a string, got {type(value).__name__}")
        return value

    @staticmethod
    def decode_bool(data: Dict[str, Any], key: str, default: bool = False) -> bool:
        value = data.get(key, default)
        if isinstance(value, str):
            value = value.lower() == "true"
        if not isinstance(value, bool):
            raise TypeError(f"{key} must be a boolean, got {type(value).__name__}")
        return value

    @staticmethod
    def decode_int(data: Dict[str, Any], key: str, default: int = 0) -> int:
        value = data.get(key, default)
        if isinstance(value, str):
            if value.isdigit():
                value = int(value)
            else:
                raise ValueError(f"{key} must be an integer string, got '{value}'")
        if not isinstance(value, int):
            raise TypeError(f"{key} must be an integer, got {type(value).__name__}")
        return value

    @staticmethod
    def decode_float(data: Dict[str, Any], key: str, default: float = 0.0) -> float:
        value = data.get(key, default)
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                raise ValueError(f"{key} must be a float string, got '{value}'")
        if not isinstance(value, (int, float)):
            raise TypeError(f"{key} must be a float, got {type(value).__name__}")
        return float(value)

    @staticmethod
    def decode_dict(data: Dict[str, Any], key: str, default: Dict[str, Any] = None) -> Dict[str, Any]:
        if default is None:
            default = {}
        value = data.get(key, default)
        if not isinstance(value, dict):
            raise TypeError(f"{key} must be a dict, got {type(value).__name__}")
        return value

    @staticmethod
    def decode_date(data: Dict[str, Any], key: str, default: datetime = None, fmt: str = "%Y-%m-%d") -> datetime:
        if default is None:
            default = datetime.now()
        value = data.get(key)
        if value is None:
            return default
        if isinstance(value, str):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                raise ValueError(f"{key} must match format {fmt}, got '{value}'")
        raise TypeError(f"{key} must be a date string, got {type(value).__name__}")

    @staticmethod
    def decode_array(data: Dict[str, Any], key: str, default: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if default is None:
            default = []
        value = data.get(key, default)
        if not isinstance(value, list):
            raise TypeError(f"{key} must be a list, got {type(value).__name__}")
        for i, item in enumerate(value):
            if not isinstance(item, dict):
                raise TypeError(f"Item at index {i} in {key} must be a dict, got {type(item).__name__}")
        return value

    @staticmethod
    def decode_json(data: Dict[str, Any], key: str, default=None) -> Dict[str, Any]:
        """
        Decodes a nested JSON object by key and validates it's a dictionary.
        """
        if default is None:
            default = {}
        value = data.get(key, default)
        if not isinstance(value, dict):
            raise TypeError(f"{key} must be a JSON object (dict), got {type(value).__name__}")
        return value

