"""
Custom exceptions for the Blocky API client.
"""


class BlockyError(Exception):
    """Base exception for all Blocky API errors."""
    pass


class BlockyAPIError(BlockyError):
    """Raised when the API returns an error response."""
    
    def __init__(self, message: str, status_code: int = None, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class BlockyAuthenticationError(BlockyAPIError):
    """Raised when authentication fails or is required but not provided."""
    pass


class BlockyNetworkError(BlockyError):
    """Raised when a network error occurs during API communication."""
    pass


class BlockyValidationError(BlockyError):
    """Raised when input validation fails."""
    pass


class BlockyMarketNotFoundError(BlockyValidationError):
    """Raised when a requested market does not exist."""
    
    def __init__(self, market: str):
        super().__init__(f"Market '{market}' not found. Please ensure it exists.")
        self.market = market
