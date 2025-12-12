class SDKError(Exception):
    """Base exception for all SDK errors."""
    pass


class ValidationError(SDKError):
    """Raised when input validation fails."""
    pass


class APIError(SDKError):
    """Raised when API request fails."""
    
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{message} (Status: {status_code})" if status_code else message)


class CryptoError(SDKError):
    """Raised when encryption/decryption fails."""
    pass


class WebSocketError(SDKError):
    """Raised when WebSocket connection fails."""
    pass
