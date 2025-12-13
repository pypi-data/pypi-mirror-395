# CaptchaKings Python Library

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Official Python client library for [CaptchaKings API](https://captchakings.com) - Fast, accurate, and affordable CAPTCHA solving service.

## ✨ Features

- 🚀 **Simple & Clean API** - Just 2 lines of code to solve CAPTCHAs
- 🔄 **Automatic Retry** - Built-in retry logic for failed requests
- 🛡️ **Type Hints** - Full type annotations for better IDE support
- ⚡ **Fast & Reliable** - Optimized for performance
- 🎯 **Error Handling** - Custom exceptions for different error types
- 📦 **Zero Configuration** - Works out of the box

## 📦 Installation

### From Source (Local Development)

```bash
cd captchakings-python
pip install -e .
```

### Requirements

- Python 3.6 or higher
- `requests` library (automatically installed)

## 🚀 Quick Start

```python
from captchakings import CaptchaKings

# Initialize client
client = CaptchaKings('ck_your_api_key_here')

# Solve CAPTCHA
result = client.solve('captcha.jpg')

print(f"Solved: {result['prediction']}")
print(f"Confidence: {result['confidence']}")
print(f"Credits Remaining: {result['credits_remaining']}")
```

That's it! Just 3 lines of code. 🎉

## 📖 Usage Examples

### Basic Usage

```python
from captchakings import CaptchaKings

client = CaptchaKings('ck_your_api_key')
result = client.solve('path/to/captcha.jpg')

if result:
    print(f"✅ CAPTCHA Solved: {result['prediction']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Credits Remaining: {result['credits_remaining']}")
```

### With Automatic Retry

```python
from captchakings import CaptchaKings

client = CaptchaKings('ck_your_api_key')

# Automatically retry up to 5 times with 2 second delay
result = client.solve_with_retry(
    'captcha.jpg',
    max_retries=5,
    retry_delay=2
)

print(f"Solved: {result['prediction']}")
```

### Error Handling

```python
from captchakings import CaptchaKings
from captchakings.exceptions import (
    AuthenticationError,
    InsufficientCreditsError,
    InvalidImageError,
    APIError
)

client = CaptchaKings('ck_your_api_key')

try:
    result = client.solve('captcha.jpg')
    print(f"Solved: {result['prediction']}")
    
except AuthenticationError:
    print("❌ Invalid API key")
except InsufficientCreditsError:
    print("❌ Not enough credits")
except InvalidImageError:
    print("❌ Invalid image file")
except APIError as e:
    print(f"❌ API Error: {e}")
```

### Using Context Manager

```python
from captchakings import CaptchaKings

# Automatically closes session after use
with CaptchaKings('ck_your_api_key') as client:
    result = client.solve('captcha.jpg')
    print(f"Solved: {result['prediction']}")
```

### Processing Multiple CAPTCHAs

```python
from captchakings import CaptchaKings
import os

client = CaptchaKings('ck_your_api_key')

captcha_folder = 'captchas/'
for filename in os.listdir(captcha_folder):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        filepath = os.path.join(captcha_folder, filename)
        
        try:
            result = client.solve(filepath)
            print(f"{filename}: {result['prediction']}")
        except Exception as e:
            print(f"{filename}: Error - {e}")
```

## 🎯 API Reference

### CaptchaKings Class

#### `__init__(api_key, base_url='https://captchakings.com/api/process.php')`

Initialize the client.

**Parameters:**
- `api_key` (str): Your CaptchaKings API key
- `base_url` (str, optional): API endpoint URL

#### `solve(image_path, timeout=30)`

Solve a CAPTCHA from an image file.

**Parameters:**
- `image_path` (str): Path to CAPTCHA image file
- `timeout` (int, optional): Request timeout in seconds (default: 30)

**Returns:**
- `dict`: Response containing:
  - `prediction` (str): Solved CAPTCHA text
  - `confidence` (float): Prediction confidence score
  - `process_time` (float): Processing time in seconds
  - `credits_deducted` (int): Credits used for this request
  - `credits_remaining` (int): Remaining credits in account
  - `plan` (str): Your current plan name

**Raises:**
- `InvalidImageError`: Image file not found or invalid
- `AuthenticationError`: Invalid API key
- `InsufficientCreditsError`: Not enough credits
- `TimeoutError`: Request timeout
- `NetworkError`: Connection error
- `APIError`: Other API errors

#### `solve_with_retry(image_path, max_retries=3, retry_delay=2, timeout=30)`

Solve CAPTCHA with automatic retry on transient failures.

**Parameters:**
- `image_path` (str): Path to CAPTCHA image file
- `max_retries` (int, optional): Maximum retry attempts (default: 3)
- `retry_delay` (int, optional): Delay between retries in seconds (default: 2)
- `timeout` (int, optional): Request timeout in seconds (default: 30)

**Returns:**
- Same as `solve()` method

## 🎨 Response Format

```python
{
    'prediction': 'ABC123',           # Solved CAPTCHA text
    'confidence': 0.98,               # Confidence score (0-1)
    'process_time': 0.234,            # Processing time in seconds
    'credits_deducted': 1,            # Credits used
    'credits_remaining': 9999,        # Remaining credits
    'plan': 'Professional'            # Your plan name
}
```

## ⚠️ Exception Types

- `CaptchaKingsException` - Base exception class
- `APIError` - General API errors
- `AuthenticationError` - Invalid API key
- `InsufficientCreditsError` - Not enough credits
- `InvalidImageError` - Invalid or missing image file
- `TimeoutError` - Request timeout
- `NetworkError` - Network connection error

## 🔑 Getting API Key

1. Visit [CaptchaKings.com](https://captchakings.com)
2. Register for an account
3. Go to Dashboard
4. Copy your API key (starts with `ck_`)

## 💡 Tips

1. **Use context manager** - Ensures proper session cleanup
2. **Enable retry logic** - For better reliability
3. **Handle exceptions** - For robust error handling
4. **Batch processing** - Reuse the same client instance

## 📚 More Examples

Check the `examples/` folder for more usage examples:

- `basic_usage.py` - Simple CAPTCHA solving
- `advanced_usage.py` - Advanced features and error handling
- `batch_processing.py` - Process multiple CAPTCHAs

## 🤝 Support

- **Website**: [captchakings.com](https://captchakings.com)
- **Documentation**: [captchakings.com/docs](https://captchakings.com?section=documentation)
- **Email**: support@captchakings.com

## 📄 License

MIT License - see LICENSE file for details

## 🌟 Why CaptchaKings?

- ✅ **High Accuracy** - 99%+ success rate
- ✅ **Fast Processing** - < 1 second average response time
- ✅ **Affordable Pricing** - Starting from $1/1000 solves
- ✅ **24/7 Support** - Always here to help
- ✅ **No Setup Required** - Start in seconds

---

Made with ❤️ by [CaptchaKings](https://captchakings.com)
