# AI Chatbot Sugarcane Webhook Endpoint

## Overview
This webhook endpoint allows external services to send chat messages to your AI Chatbot (powered by Gemini RAG) and receive intelligent, context-aware responses about sugarcane agriculture.

## Webhook Verification Token
**Verify Token:** `sugarcane_ai_webhook_2024`

You can customize this by setting the `WEBHOOK_VERIFY_TOKEN` environment variable in your `.env` file.

## Endpoints

### Verification (GET)
```
GET /webhook?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=CHALLENGE_STRING
```
Used by services like WhatsApp, Facebook to verify the webhook.

### Message Processing (POST)
```
POST /webhook
```

## Request Format
Send a JSON payload with the following fields:

| Field     | Type   | Required | Description                                 |
|-----------|--------|----------|---------------------------------------------|
| chat      | string | Yes      | The chat message or question to process     |
| language  | string | No       | Language for the response (default: english)|

### Example Request
```json
{
  "chat": "How do I control pests in sugarcane?",
  "language": "english"
}
```

## Response Format
Returns a JSON object with the RAG Gemini answer:

```json
{
  "response": "To control pests in sugarcane, regularly monitor crops, use biological controls, and follow recommended irrigation practices."
}
```

## Usage
- Deploy your Flask app to a public server (e.g., Render, Heroku, AWS, etc.)
- Register the public `/webhook` URL with any service that can send chat data (e.g., automation platforms, other bots, custom integrations)
- The webhook will process incoming chat and return an answer using Gemini RAG and your knowledge base

## Testing Locally
You can use [ngrok](https://ngrok.com/) to expose your local Flask server for webhook testing:

```
ngrok http 5000
```

Then use the generated public URL for webhook requests.

## Example with `requests` (Python)
```python
import requests

url = "http://localhost:5000/webhook"
payload = {
    "chat": "What are the best practices for sugarcane pest control?",
    "language": "english"
}
response = requests.post(url, json=payload)
print(response.json())
```

## Notes
- The webhook uses the same Gemini RAG logic as the main chatbot API
- Supports multi-language responses (English, Hindi, Marathi, Tamil, Telugu, Kannada)
- Returns helpful error messages for missing or invalid data
