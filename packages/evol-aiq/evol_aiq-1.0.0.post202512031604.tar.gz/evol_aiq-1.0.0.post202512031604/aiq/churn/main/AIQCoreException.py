class AIQCoreException(Exception):
    def __init__(self, message: str, step: str = "Unknown", original_exception: Exception = None):
        super().__init__(message)
        self.message = message
        self.step = step
        self.original_exception = original_exception

    def __str__(self):
        if self.step != "Unknown":
            return f"[{self.step} Failure] {self.message}"
        return self.message
