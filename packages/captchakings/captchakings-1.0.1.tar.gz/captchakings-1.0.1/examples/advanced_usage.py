#!/usr/bin/env python3
"""
CaptchaKings - Advanced Usage Example

Shows advanced features including:
- Error handling
- Automatic retry
- Context manager
- Batch processing
"""

from captchakings import CaptchaKings
from captchakings.exceptions import (
    AuthenticationError,
    InsufficientCreditsError,
    InvalidImageError,
    TimeoutError,
    NetworkError,
    APIError
)
import os

def example_with_error_handling():
    """Example with comprehensive error handling"""
    print("📚 Example 1: Error Handling")
    print("=" * 50)
    
    client = CaptchaKings('ck_your_api_key_here')
    
    try:
        result = client.solve('captcha.jpg')
        print(f"✅ Solved: {result['prediction']}")
        print(f"Credits remaining: {result['credits_remaining']}")
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("Please check your API key")
        
    except InsufficientCreditsError as e:
        print(f"❌ Not enough credits: {e}")
        print("Please add credits to your account")
        
    except InvalidImageError as e:
        print(f"❌ Invalid image: {e}")
        print("Please check the image file path")
        
    except TimeoutError as e:
        print(f"❌ Request timeout: {e}")
        print("Please try again")
        
    except NetworkError as e:
        print(f"❌ Network error: {e}")
        print("Please check your internet connection")
        
    except APIError as e:
        print(f"❌ API error: {e}")
        
    finally:
        client.close()
    
    print()

def example_with_retry():
    """Example with automatic retry logic"""
    print("📚 Example 2: Automatic Retry")
    print("=" * 50)
    
    client = CaptchaKings('ck_your_api_key_here')
    
    try:
        # Will automatically retry up to 5 times if request fails
        result = client.solve_with_retry(
            'captcha.jpg',
            max_retries=5,
            retry_delay=2,
            timeout=30
        )
        
        print(f"✅ Solved: {result['prediction']}")
        print(f"Confidence: {result['confidence']}")
        
    except Exception as e:
        print(f"❌ Failed after retries: {e}")
    
    finally:
        client.close()
    
    print()

def example_context_manager():
    """Example using context manager (recommended)"""
    print("📚 Example 3: Context Manager")
    print("=" * 50)
    
    # Using 'with' statement - automatically closes session
    with CaptchaKings('ck_your_api_key_here') as client:
        try:
            result = client.solve('captcha.jpg')
            print(f"✅ Solved: {result['prediction']}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print()

def example_batch_processing():
    """Example processing multiple CAPTCHAs"""
    print("📚 Example 4: Batch Processing")
    print("=" * 50)
    
    captcha_folder = 'captchas/'
    
    # Check if folder exists
    if not os.path.exists(captcha_folder):
        print(f"❌ Folder not found: {captcha_folder}")
        print()
        return
    
    with CaptchaKings('ck_your_api_key_here') as client:
        solved_count = 0
        failed_count = 0
        
        for filename in os.listdir(captcha_folder):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                filepath = os.path.join(captcha_folder, filename)
                
                try:
                    result = client.solve_with_retry(filepath, max_retries=3)
                    print(f"✅ {filename}: {result['prediction']}")
                    solved_count += 1
                    
                except Exception as e:
                    print(f"❌ {filename}: {e}")
                    failed_count += 1
        
        print("━" * 50)
        print(f"Total Solved: {solved_count}")
        print(f"Total Failed: {failed_count}")
    
    print()

def example_custom_timeout():
    """Example with custom timeout"""
    print("📚 Example 5: Custom Timeout")
    print("=" * 50)
    
    with CaptchaKings('ck_your_api_key_here') as client:
        try:
            # Set custom timeout to 60 seconds
            result = client.solve('captcha.jpg', timeout=60)
            print(f"✅ Solved: {result['prediction']}")
        except TimeoutError:
            print("❌ Request took too long")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print()

if __name__ == '__main__':
    print("\n🚀 CaptchaKings Advanced Usage Examples\n")
    
    # Run all examples
    example_with_error_handling()
    example_with_retry()
    example_context_manager()
    example_batch_processing()
    example_custom_timeout()
    
    print("✨ All examples completed!")
