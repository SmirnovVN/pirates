from typing import List


class Error:
    def __init__(self, message: str):
        self.message = message


class DefaultResponse:
    def __init__(self, tick: int, success: bool, errors: List[Error]):
        self.tick = tick
        self.success = success
        self.errors = errors
