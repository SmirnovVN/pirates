from app.schemas.scan import Scan


class Response:
    def __init__(self, success: bool, scan: Scan):
        self.success = success
        self.scan = scan
