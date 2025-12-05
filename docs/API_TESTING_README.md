```markdown
# API Testing Guide for AI Chatbot Sugarcane Webhook

## Endpoint
```
POST /webhook
```

## Required Headers
| Header              | Value                | Description                       |
|---------------------|----------------------|-----------------------------------|
| Content-Type        | application/json     | Required for JSON payloads        |

## Request Body (JSON)
Send a JSON object with one of the following formats:

### 1. Simple Format
```json
{
  "chat": "What are the best practices for sugarcane pest control?",
  "language": "english"
}
```

### 2. Periskope Format
```json
{
  "data": {
    "body": "What are the best practices for sugarcane pest control?"
  },
  "language": "english"
}
```

### 3. WhatsApp Format
```json
{
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messages": [
              {
                "text": {"body": "What are the best practices for sugarcane pest control?"}
              }
            ]
          }
        }
      ]
    }
  ],
  "language": "english"
}
```

## Example Python Test
```python
import requests

url = "http://localhost:5000/webhook"
headers = {"Content-Type": "application/json"}
payload = {
    "chat": "What are the best practices for sugarcane pest control?",
    "language": "english"
}
response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

## Response Format
The API will respond with JSON:
```json
{
  "response": "RAG answer...",
  "body": "RAG answer...",
  "text": "RAG answer...",
  "message": "RAG answer...",
  "status": "success"
}
```

## Notes
- Always set `Content-Type: application/json` for POST requests.
- The `language` parameter is optional (defaults to English).
- The API supports multiple payload formats for compatibility with different webhook sources.

```
