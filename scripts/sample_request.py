#!/usr/bin/env python3
"""
Sample API Request Script
=========================

A simple example script demonstrating how to make API requests to the
Agricultural Advisory Chatbot's RAG endpoint.

Usage:
    python sample_request.py

Requirements:
    - requests library (pip install requests)
    - Local server running at http://localhost:5000

Example:
    $ python scripts/sample_request.py
    
    Response:
    {
        "response": "Best practices for sugarcane pest control include...",
        "response_format": "text",
        ...
    }
"""
import requests


def main():
    """Send a sample query to the /ask endpoint and print the response."""
    url = "http://localhost:5000/ask"
    
    payload = {
        "question": "What are the best practices for sugarcane pest control?",
        "language": "english"
    }
    
    print(f"Sending request to: {url}")
    print(f"Payload: {payload}")
    print("-" * 50)
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        print("Response received successfully!")
        print("-" * 50)
        
        # Pretty print the response
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure the Flask app is running at http://localhost:5000")
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
