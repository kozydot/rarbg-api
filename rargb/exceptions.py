class APIError(Exception):
    pass

class RateLimitError(APIError):
    pass

class InvalidTokenError(APIError):
    pass