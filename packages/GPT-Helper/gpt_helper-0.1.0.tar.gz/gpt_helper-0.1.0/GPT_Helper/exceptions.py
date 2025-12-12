class GPTError(Exception):
    """Base exception for GPT_Helper."""

class APIKeyMissing(GPTError):
    """Raised when API key is not found."""

class APIError(GPTError):
    """Raised when the ChatGPT API returns an error."""
