import requests
import json

OLLAMA_API = "http://localhost:11434/api/generate"

def test_ollama():
    payload = {
        "model": "mistral",
        "prompt": "What is an invoice?",
        "stream": False,
        "temperature": 0.3
    }
    
    print(f"Sending payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=120)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ollama()