"""
CaptchaKings API Client
"""

import requests
import os
import time
from typing import Dict, Optional, Union
from .exceptions import (
    APIError,
    AuthenticationError,
    InsufficientCreditsError,
    InvalidImageError,
    TimeoutError as CKTimeoutError,
    NetworkError
)

class CaptchaKings:
    """
    CaptchaKings API Client
    
    Simple and powerful Python client for CaptchaKings API.
    
    Example:
        >>> from captchakings import CaptchaKings
        >>> client = CaptchaKings('ck_your_api_key')
        >>> result = client.solve('captcha.jpg')
        >>> print(result['prediction'])
    """
    
    def __init__(self, api_key: str, base_url: str = 'https://captchakings.com/api/process.php'):
        """
        Initialize CaptchaKings client
        
        Args:
            api_key: Your CaptchaKings API key
            base_url: API endpoint URL (default: official API)
        """
        if not api_key:
            raise ValueError("API key is required")
        
        self.api_key = api_key
        self.base_url = base_url
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {api_key}'
        })
    
    def solve(self, image_path: str, timeout: int = 30) -> Dict:
        """
        Solve CAPTCHA from image file
        
        Args:
            image_path: Path to CAPTCHA image file
            timeout: Request timeout in seconds (default: 30)
            
        Returns:
            dict: Response with prediction and credits info
            
        Raises:
            InvalidImageError: If image file not found or invalid
            AuthenticationError: If API key is invalid
            InsufficientCreditsError: If not enough credits
            APIError: For other API errors
            
        Example:
            >>> result = client.solve('captcha.jpg')
            >>> print(f"Solved: {result['prediction']}")
            >>> print(f"Credits: {result['credits_remaining']}")
        """
        if not os.path.exists(image_path):
            raise InvalidImageError(f"Image file not found: {image_path}")
        
        try:
            with open(image_path, 'rb') as f:
                files = {
                    'captcha': ('captcha.jpg', f, 'image/jpeg')
                }
                
                response = self._session.post(
                    self.base_url,
                    files=files,
                    timeout=timeout
                )
            
            data = response.json()
            
            if response.status_code == 200 and data.get('success'):
                return {
                    'prediction': data['data']['prediction'],
                    'confidence': data['data']['confidence'],
                    'process_time': data['data']['process_time'],
                    'credits_deducted': data['credits']['credits_deducted'],
                    'credits_remaining': data['credits']['credits_remaining'],
                    'plan': data['credits']['plan']
                }
            else:
                self._handle_error(response.status_code, data)
                
        except requests.exceptions.Timeout:
            raise CKTimeoutError(f"Request timeout after {timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request error: {str(e)}")
        except (ValueError, KeyError) as e:
            raise APIError(f"Invalid response format: {str(e)}")
        except IOError as e:
            raise InvalidImageError(f"Error reading image file: {str(e)}")
    
    def solve_with_retry(self, image_path: str, max_retries: int = 3, 
                        retry_delay: int = 2, timeout: int = 30) -> Dict:
        """
        Solve CAPTCHA with automatic retry on failure
        
        Args:
            image_path: Path to CAPTCHA image file
            max_retries: Maximum number of retry attempts (default: 3)
            retry_delay: Delay between retries in seconds (default: 2)
            timeout: Request timeout in seconds (default: 30)
            
        Returns:
            dict: Response with prediction and credits info
            
        Raises:
            Same as solve() method
            
        Example:
            >>> result = client.solve_with_retry('captcha.jpg', max_retries=5)
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                return self.solve(image_path, timeout)
            except (AuthenticationError, InsufficientCreditsError, InvalidImageError):
                raise
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        
        raise last_error
    
    def get_balance(self) -> Dict:
        """
        Get account balance and plan information
        
        Returns:
            dict: Balance information
            
        Note:
            This method sends a test request to get balance info
        """
        test_image_path = os.path.join(os.path.dirname(__file__), 'test.jpg')
        
        try:
            result = self.solve(test_image_path)
            return {
                'credits_remaining': result['credits_remaining'],
                'plan': result['plan']
            }
        except Exception:
            raise APIError("Could not retrieve balance information")
    
    def _handle_error(self, status_code: int, data: Dict):
        """Handle API error responses"""
        error_msg = data.get('error', 'Unknown error')
        
        if status_code == 401 or 'Invalid API key' in error_msg:
            raise AuthenticationError(error_msg)
        elif status_code == 402 or 'Insufficient credits' in error_msg or 'Free trial expired' in error_msg:
            raise InsufficientCreditsError(error_msg)
        elif status_code == 400 or 'Invalid image' in error_msg:
            raise InvalidImageError(error_msg)
        else:
            raise APIError(f"API error: {error_msg}")
    
    def close(self):
        """Close the session"""
        self._session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
