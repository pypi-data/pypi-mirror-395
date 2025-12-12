class ClientException(Exception):
    status_code: int
    message: str

    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"[{self.status_code}] {self.message}"
