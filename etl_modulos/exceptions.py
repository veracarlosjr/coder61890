class APIError(Exception):
    """Exception raised for errors in the API request."""
    def __init__(self, message, status_code=None):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class DatabaseError(Exception):
    """Exception raised for errors in the database."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
