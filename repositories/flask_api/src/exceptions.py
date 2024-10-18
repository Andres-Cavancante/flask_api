class ApiException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

    def get_return_msg(self):
        return {
                "code": self.code,
                "message": str(self)
            }