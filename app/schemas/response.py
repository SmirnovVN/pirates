from app.schemas.scan import Scan


class Response:
    def __init__(self, success: bool, scan: dict):
        self.success = success
        self.scan = Scan(**scan)
