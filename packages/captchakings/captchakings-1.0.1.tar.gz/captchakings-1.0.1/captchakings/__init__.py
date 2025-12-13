"""
CaptchaKings Python Library

Simple and powerful Python client for CaptchaKings API.

Example:
    >>> from captchakings import CaptchaKings
    >>> client = CaptchaKings('ck_your_api_key')
    >>> result = client.solve('captcha.jpg')
    >>> print(result['prediction'])
"""

__version__ = '1.0.0'
__author__ = 'CaptchaKings'
__license__ = 'MIT'

from .client import CaptchaKings
from .exceptions import (
    CaptchaKingsException,
    APIError,
    AuthenticationError,
    InsufficientCreditsError,
    InvalidImageError,
    TimeoutError,
    NetworkError
)

__all__ = [
    'CaptchaKings',
    'CaptchaKingsException',
    'APIError',
    'AuthenticationError',
    'InsufficientCreditsError',
    'InvalidImageError',
    'TimeoutError',
    'NetworkError'
]
