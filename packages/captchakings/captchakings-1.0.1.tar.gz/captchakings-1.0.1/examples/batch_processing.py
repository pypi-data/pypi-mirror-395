#!/usr/bin/env python3
"""
CaptchaKings - Batch Processing Example

Process multiple CAPTCHA images from a folder efficiently.
"""

from captchakings import CaptchaKings
from captchakings.exceptions import CaptchaKingsException
import os
import time
from pathlib import Path

def process_folder(api_key, folder_path, output_file='results.txt'):
    """
    Process all CAPTCHA images in a folder
    
    Args:
        api_key: Your CaptchaKings API key
        folder_path: Path to folder containing CAPTCHA images
        output_file: File to save results (optional)
    """
    
    # Get all image files
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    image_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(supported_formats)
    ]
    
    if not image_files:
        print(f"❌ No image files found in {folder_path}")
        return
    
    print(f"📁 Found {len(image_files)} images to process")
    print("=" * 70)
    
    # Initialize client
    with CaptchaKings(api_key) as client:
        results = []
        start_time = time.time()
        
        for idx, filename in enumerate(image_files, 1):
            filepath = os.path.join(folder_path, filename)
            
            try:
                # Solve with retry
                result = client.solve_with_retry(
                    filepath,
                    max_retries=3,
                    retry_delay=1
                )
                
                # Store result
                results.append({
                    'filename': filename,
                    'prediction': result['prediction'],
                    'confidence': result['confidence'],
                    'status': 'success'
                })
                
                # Display progress
                print(f"[{idx}/{len(image_files)}] ✅ {filename}: {result['prediction']} "
                      f"(confidence: {result['confidence']:.2f})")
                
            except CaptchaKingsException as e:
                # Store error
                results.append({
                    'filename': filename,
                    'prediction': None,
                    'error': str(e),
                    'status': 'failed'
                })
                
                print(f"[{idx}/{len(image_files)}] ❌ {filename}: {e}")
        
        # Calculate statistics
        elapsed_time = time.time() - start_time
        success_count = sum(1 for r in results if r['status'] == 'success')
        failed_count = len(results) - success_count
        avg_time = elapsed_time / len(results)
        
        # Display summary
        print("=" * 70)
        print(f"\n📊 SUMMARY")
        print("━" * 70)
        print(f"Total Processed:   {len(results)}")
        print(f"✅ Successful:     {success_count}")
        print(f"❌ Failed:         {failed_count}")
        print(f"Success Rate:      {(success_count/len(results)*100):.1f}%")
        print(f"Total Time:        {elapsed_time:.2f}s")
        print(f"Average Time:      {avg_time:.2f}s per image")
        print("━" * 70)
        
        # Save results to file
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("CAPTCHAKINGS BATCH PROCESSING RESULTS\n")
                f.write("=" * 70 + "\n\n")
                
                for result in results:
                    if result['status'] == 'success':
                        f.write(f"{result['filename']}: {result['prediction']} "
                               f"(confidence: {result['confidence']:.2f})\n")
                    else:
                        f.write(f"{result['filename']}: FAILED - {result['error']}\n")
                
                f.write("\n" + "=" * 70 + "\n")
                f.write(f"Total: {len(results)} | Success: {success_count} | "
                       f"Failed: {failed_count}\n")
            
            print(f"\n💾 Results saved to: {output_file}")

def main():
    # Configuration
    API_KEY = 'ck_your_api_key_here'
    CAPTCHA_FOLDER = 'captchas'  # Folder containing CAPTCHA images
    OUTPUT_FILE = 'captcha_results.txt'
    
    # Check if folder exists
    if not os.path.exists(CAPTCHA_FOLDER):
        print(f"❌ Folder not found: {CAPTCHA_FOLDER}")
        print(f"Please create the folder and add CAPTCHA images")
        return
    
    # Process folder
    print("\n🚀 Starting Batch Processing...")
    print()
    
    process_folder(API_KEY, CAPTCHA_FOLDER, OUTPUT_FILE)
    
    print("\n✨ Batch processing completed!")

if __name__ == '__main__':
    main()
