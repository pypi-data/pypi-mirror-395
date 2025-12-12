"""Custom exceptions for API Key Manager"""


class NoValidAPIKeyError(Exception):
    """Raised when all API keys have been exhausted"""
    pass
