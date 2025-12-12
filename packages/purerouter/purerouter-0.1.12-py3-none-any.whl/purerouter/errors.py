# purerouter-sdk/src/purerouter/errors.py
from typing import Optional

class APIError(Exception):
    def __init__(self, status_code: int, message: str, *, body: Optional[object] = None):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.body = body