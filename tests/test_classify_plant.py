#!/usr/bin/env python3
"""
Test script for the /classify-plant endpoint.
Classifies if an image contains sugarcane or weed using Gemini Vision API.

Usage:
    python test_classify_plant.py --image path/to/image.jpg
    python test_classify_plant.py --image path/to/image.jpg --language hindi
    python test_classify_plant.py --image path/to/image.jpg --host localhost --port 5000
"""

import argparse
import requests
import os
import sys
from pathlib import Path

def test_classify_plant(host='localhost', port=5000, image_path=None, language='english'):
    """Test the /classify-plant endpoint"""
    
    # Validate image file exists
    if not image_path or not os.path.exists(image_path):
        print(f"❌ Error: Image file not found: {image_path}")
        return False
    
    # Prepare the request
    url = f"http://{host}:{port}/classify-plant"
    
    print(f"🌿 Testing Plant Classification")
    print(f"📍 URL: {url}")
    print(f"🖼️  Image: {image_path}")
    print(f"🌐 Language: {language}")
    print("-" * 60)
    
    try:
        # Open and send the image file
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            data = {'language': language}
            
            print("📤 Sending request...")
            response = requests.post(url, files=files, data=data, timeout=60)
        
        print(f"✅ Response Status: {response.status_code}")
        print("-" * 60)
        
        if response.status_code == 200:
            result = response.json()
            
            # Display results with formatting
            classification = result.get('classification', 'unknown').upper()
            confidence = result.get('confidence', 0) * 100
            
            # Choose emoji based on classification
            if classification == 'SUGARCANE':
                emoji = '✅🌾'
            elif classification == 'WEED':
                emoji = '⚠️🌿'
            else:
                emoji = '❓'
            
            print(f"{emoji} CLASSIFICATION RESULT")
            print("=" * 60)
            print(f"Type:           {classification}")
            print(f"Confidence:     {confidence:.1f}%")
            
            if result.get('plant_type'):
                print(f"Plant Type:     {result['plant_type']}")
            
            print(f"\nDetails:")
            print(f"  {result.get('details', 'N/A')}")
            
            if result.get('characteristics'):
                print(f"\nCharacteristics:")
                print(f"  {result['characteristics']}")
            
            if result.get('recommendation'):
                print(f"\n💡 Recommendation:")
                print(f"  {result['recommendation']}")
            
            print("=" * 60)
            return True
            
        else:
            error_data = response.json()
            print(f"❌ Error: {error_data.get('error', 'Unknown error')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Could not connect to {url}")
        print(f"   Make sure the Flask server is running on {host}:{port}")
        return False
    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout Error: Request took too long (>60s)")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Test the plant classification endpoint',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_classify_plant.py --image sugarcane.jpg
  python test_classify_plant.py --image weed.jpg --language hindi
  python test_classify_plant.py --image test.jpg --host 192.168.1.100 --port 8080
        """
    )
    
    parser.add_argument('--host', 
                       default=os.getenv('SERVER_HOST', 'localhost'),
                       help='Server host (default: localhost or SERVER_HOST env var)')
    
    parser.add_argument('--port', 
                       type=int,
                       default=int(os.getenv('PORT', os.getenv('SERVER_PORT', 5000))),
                       help='Server port (default: 5000 or PORT/SERVER_PORT env var)')
    
    parser.add_argument('--image', 
                       default=os.getenv('TEST_IMAGE'),
                       help='Path to image file (required)')
    
    parser.add_argument('--language',
                       default='english',
                       choices=['english', 'hindi', 'marathi', 'tamil', 'telugu', 'kannada', 'punjabi'],
                       help='Language for response (default: english)')
    
    args = parser.parse_args()
    
    if not args.image:
        parser.print_help()
        print("\n❌ Error: --image argument is required")
        sys.exit(1)
    
    success = test_classify_plant(
        host=args.host,
        port=args.port,
        image_path=args.image,
        language=args.language
    )
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
