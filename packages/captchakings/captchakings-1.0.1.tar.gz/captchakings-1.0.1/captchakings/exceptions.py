"""
CaptchaKings API Exceptions
"""

class CaptchaKingsException(Exception):
    """Base exception for CaptchaKings API"""
    pass

class APIError(CaptchaKingsException):
    """API request error"""
    pass

class AuthenticationError(CaptchaKingsException):
    """Invalid API key or authentication failed"""
    pass

class InsufficientCreditsError(CaptchaKingsException):
    """Not enough credits to process request"""
    pass

class InvalidImageError(CaptchaKingsException):
    """Invalid or corrupted image file"""
    pass

class TimeoutError(CaptchaKingsException):
    """Request timeout"""
    pass

class NetworkError(CaptchaKingsException):
    """Network connection error"""
    pass
