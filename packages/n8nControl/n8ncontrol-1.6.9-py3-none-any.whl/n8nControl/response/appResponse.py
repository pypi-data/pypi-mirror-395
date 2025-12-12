class AppResponse:
    def __init__(self, status: str, message: str, data=None):
        self.status = status
        self.message = message
        self.data = data