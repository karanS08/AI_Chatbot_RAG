````markdown
# 🎨 Showcase Phrases for Guaranteed Infographic Generation

## Overview
These 5 phrases are **hardcoded** in the backend to **always** trigger infographic generation, perfect for demonstrations and showcases.

## The Magic Phrases

### 1. **"sugarcane growth stages"**
- **Description**: Timeline showing different growth phases
- **Example questions**:
  - "Tell me about sugarcane growth stages"
  - "What are the sugarcane growth stages from planting to harvest?"
  - "Explain sugarcane growth stages and timeline"

### 2. **"fertilizer schedule"**
- **Description**: Chart showing fertilizer application timing
- **Example questions**:
  - "Show me the fertilizer schedule for sugarcane"
  - "What is the recommended fertilizer schedule?"
  - "I need a fertilizer schedule for my farm"

### 3. **"irrigation methods"**
- **Description**: Comparison of different irrigation techniques
- **Example questions**:
  - "What are different irrigation methods?"
  - "Compare irrigation methods for sugarcane"
  - "Tell me about irrigation methods available"

### 4. **"disease identification"**
- **Description**: Visual guide for identifying crop diseases
- **Example questions**:
  - "Help me with disease identification"
  - "How do I do disease identification in sugarcane?"
  - "I need help with disease identification"

### 5. **"sugarcane varieties"**
- **Description**: Comparison chart of different varieties
- **Example questions**:
  - "What are the best sugarcane varieties?"
  - "Compare different sugarcane varieties"
  - "Tell me about sugarcane varieties for Punjab"

## How to Use

### In Chat UI
Simply type any question containing one of these phrases:
```
"Tell me about sugarcane growth stages"
```

### In API Tests
```bash
python test_infographic_generation.py
```

### Via cURL
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me about sugarcane growth stages", "language": "english"}'
```

## Response Format

When a showcase phrase is detected, you'll get:

```json
{
  "response": "Detailed text answer about the topic...",
  "infographic_url": "/uploads/infographics/infographic_1733220123456.png",
  "infographic_reason": "Showcase mode: Visual guide for sugarcane growth stages"
}
```

## Why Hardcoded?

Normally, Gemini decides whether an infographic would be helpful. However, for demonstrations and showcases, we want **guaranteed** infographic generation for specific topics. These 5 phrases bypass the decision logic and always trigger image generation.

## Technical Details

### Backend Implementation (`app.py`)
```python
SHOWCASE_TRIGGERS = [
    "sugarcane growth stages",
    "fertilizer schedule",
    "irrigation methods",
    "disease identification",
    "sugarcane varieties"
]
```

The `decide_make_infographic()` function checks if any trigger phrase appears in the content (case-insensitive) and returns:
- `make: True` (force generation)
- `reason: "Showcase mode: Visual guide for [topic]"`
- `style: "timeline"` or `"chart"` or `"simple"` (depending on topic)

### Image Generation
Uses **Imagen 3.0 API** to generate PNG infographics based on the content and style hint.

## Tips for Best Results

1. **Include the exact phrase**: Make sure your question contains one of the 5 trigger phrases
2. **Add context**: While the trigger guarantees generation, adding details improves the infographic quality
3. **Be patient**: Image generation takes 10-20 seconds
4. **Check logs**: Server logs will show: `🎨 SHOWCASE MODE: Trigger phrase detected`

## Example Showcase Flow

1. User asks: **"Tell me about sugarcane growth stages"**
2. Backend detects trigger: ✅ "sugarcane growth stages"
3. System forces: `make_infographic = True`
4. Imagen generates PNG infographic
5. User receives text + visual infographic

## Disabling Showcase Mode

If you want to disable hardcoded triggers and rely solely on Gemini's decision:

```python
# In app.py, comment out the showcase check:
# SHOWCASE_TRIGGERS = [...]
# for trigger in SHOWCASE_TRIGGERS:
#     if trigger in content_lower:
#         return {'make': True, ...}
```

## Related Files
- `app.py` - Contains the trigger logic in `decide_make_infographic()`
- `test_infographic_generation.py` - Test script using all 5 phrases
- `INFOGRAPHIC_FEATURE.md` - Complete feature documentation

````
