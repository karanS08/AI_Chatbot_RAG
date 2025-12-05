#!/usr/bin/env python3
"""
Test script for infographic generation feature.
Tests the /ask endpoint to verify PNG infographic generation with multiple farming questions.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

# Test questions specifically designed to trigger infographic generation
# These phrases are HARDCODED to always generate infographics for showcase purposes
TEST_QUESTIONS = [
    {
        "question": "Tell me about sugarcane growth stages from planting to harvest. What are the different phases?",
        "description": "Sugarcane growth stages timeline",
        "trigger": "sugarcane growth stages"
    },
    {
        "question": "I need to understand the fertilizer schedule for my sugarcane farm. When should I apply which nutrients?",
        "description": "Fertilizer application schedule",
        "trigger": "fertilizer schedule"
    },
    {
        "question": "Can you explain different irrigation methods for sugarcane? I want to know which is best for my farm.",
        "description": "Irrigation methods comparison",
        "trigger": "irrigation methods"
    },
    {
        "question": "Help me with disease identification in sugarcane. What are the common diseases and how to spot them?",
        "description": "Sugarcane disease identification guide",
        "trigger": "disease identification"
    },
    {
        "question": "Which sugarcane varieties should I choose for my region? I need to compare different options.",
        "description": "Sugarcane varieties comparison chart",
        "trigger": "sugarcane varieties"
    }
]

def test_single_question(question_data, test_number):
    """Test a single question and check for infographic generation"""
    print(f"\n{'='*70}")
    print(f"TEST {test_number}: {question_data['description']}")
    print(f"{'='*70}")
    print(f"Question: {question_data['question'][:80]}...")
    
    payload = {
        "question": question_data["question"],
        "language": "english"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=180)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received ({len(data.get('response', ''))} chars)")
            
            if 'infographic_url' in data:
                print(f"\n🎨 INFOGRAPHIC GENERATED!")
                print(f"   URL: {data['infographic_url']}")
                print(f"   Reason: {data.get('infographic_reason', 'N/A')}")
                
                # Verify the infographic is accessible
                infographic_url = f"{BASE_URL}{data['infographic_url']}"
                img_response = requests.head(infographic_url, timeout=10)
                if img_response.status_code == 200:
                    print(f"   ✅ Infographic accessible at: {infographic_url}")
                    return True
                else:
                    print(f"   ⚠️ Infographic not accessible (status: {img_response.status_code})")
                    return False
            else:
                print(f"\n❌ No infographic generated")
                print(f"   Note: Gemini decided infographic wasn't needed")
                return False
        else:
            print(f"❌ Error: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("⚠️ Request timed out (this can happen with image generation)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_questions():
    """Test all farming questions"""
    print("\n" + "="*70)
    print("TESTING MULTIPLE FARMING QUESTIONS FOR INFOGRAPHICS")
    print("="*70)
    
    results = []
    
    for i, question_data in enumerate(TEST_QUESTIONS, 1):
        success = test_single_question(question_data, i)
        results.append({
            'test': i,
            'description': question_data['description'],
            'infographic_generated': success
        })
        
        # Small delay between requests
        if i < len(TEST_QUESTIONS):
            print("\nWaiting 3 seconds before next test...")
            time.sleep(3)
    
    return results

def test_health():
    """Test health endpoint"""
    print("\nTesting /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Health check passed: {response.json()}")
        return True
    else:
        print(f"❌ Health check failed: {response.text}")
        return False

def print_summary(results):
    """Print summary of all test results"""
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    total = len(results)
    successful = sum(1 for r in results if r['infographic_generated'])
    
    print(f"\nTotal tests: {total}")
    print(f"Infographics generated: {successful}")
    print(f"Success rate: {(successful/total*100):.1f}%\n")
    
    for r in results:
        status = "✅ Generated" if r['infographic_generated'] else "❌ Not generated"
        print(f"Test {r['test']}: {status} - {r['description']}")
    
    print("\n" + "="*70)
    if successful > 0:
        print(f"🎉 SUCCESS! {successful} infographic(s) were generated!")
        print("Check the URLs above to view the generated images.")
    else:
        print("⚠️ No infographics were generated.")
        print("Possible reasons:")
        print("  - Gemini decided visualization wasn't needed")
        print("  - Imagen API access not enabled")
        print("  - API rate limits reached")
        print("  - Network/timeout issues")
    print("="*70)

if __name__ == "__main__":
    print("="*70)
    print("SUGARCANE FARMING INFOGRAPHIC GENERATION TEST")
    print("="*70)
    print("\n🎯 SHOWCASE MODE: These 5 questions are HARDCODED to always generate")
    print("infographics for demonstration purposes!")
    print("\nTrigger phrases that guarantee infographic generation:")
    for i, q in enumerate(TEST_QUESTIONS, 1):
        print(f"  {i}. '{q['trigger']}' → {q['description']}")
    print("\n💡 You can use these exact phrases in the chat UI to see infographics!")
    print("⏱️  Note: Each test may take 10-20 seconds due to image generation")
    
    try:
        # First check server health
        if not test_health():
            print("\n❌ Server health check failed. Exiting.")
            exit(1)
        
        # Run all farming question tests
        results = test_all_questions()
        
        # Print summary
        print_summary(results)
        
        print("\n💡 Tips:")
        print("  - Generated images are saved in: uploads/infographics/")
        print("  - You can view them in browser at: http://localhost:5000/uploads/infographics/")
        print("  - Images are in PNG format and can be downloaded")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server")
        print("Make sure gunicorn is running on port 5000:")
        print("  gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app")
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
