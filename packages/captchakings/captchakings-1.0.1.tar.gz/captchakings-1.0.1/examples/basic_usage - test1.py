#!/usr/bin/env python3
"""
CaptchaKings - Basic Usage Example

Simple example showing how to solve a CAPTCHA using CaptchaKings library.
"""

from captchakings import CaptchaKings

def main():
    # Initialize client with your API key
    client = CaptchaKings('ck_038fde3200130c372229eb47688de707')
    
    # Solve CAPTCHA
    print("🔄 Solving CAPTCHA...")
    result = client.solve('captcha.jpg')
    
    # Display results
    print("\n✅ SUCCESS!")
    print("━" * 50)
    print(f"Prediction:        {result['prediction']}")
    print(f"Confidence:        {result['confidence']}")
    print(f"Process Time:      {result['process_time']}s")
    print("━" * 50)
    print(f"Credits Deducted:  {result['credits_deducted']}")
    print(f"Credits Remaining: {result['credits_remaining']}")
    print(f"Plan:              {result['plan']}")
    
    # Close session (optional, but good practice)
    client.close()

if __name__ == '__main__':
    main()
