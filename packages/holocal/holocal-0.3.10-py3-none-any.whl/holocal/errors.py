class HolocalException(Exception):
    pass


class HTTPStatusError(HolocalException):
    def __init__(self, status: int, target: str = "") -> None:
        super().__init__(f"http status is not success: {status}")
        self.target = target
