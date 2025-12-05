# AI Services Module Documentation

## Overview

The `ai_services.py` module is a centralized hub for all AI-related operations in the sugarcane advisory chatbot. This refactoring separates concerns by moving all Gemini client interactions and AI logic out of the main Flask application into a dedicated, well-organized module.

## Why This Refactoring?

### Before
- **app.py**: 446 lines (originally 800+ with all functions)
- All AI logic mixed with Flask routes
- Difficult to test AI functions independently
- Hard to reuse AI logic across different endpoints

### After
- **app.py**: ~100 lines (routes + error handlers only)
- **ai_services.py**: 513 lines (all AI logic, organized and documented)
- Clean separation of concerns
- Easy to test, maintain, and extend
- Reusable AI functions across the codebase

## Module Structure

### 1. **Configuration & Initialization**

```python
set_client_and_app(client, app, upload_folder)
```

**Purpose**: Initialize the module with Flask app and Gemini client references.

**Usage** (in app.py):
```python
if api_key:
    client = genai.Client(api_key=api_key)
    ai_services.set_client_and_app(client, app, app.config['UPLOAD_FOLDER'])
```

**Why**: Module-level CLIENT and FLASK_APP are initialized once at startup, avoiding circular imports and ensuring all functions share the same client instance.

---

## Functions by Category

### A. RAG & File Management

#### `ensure_file_search_store()`
**Purpose**: Ensure a Gemini file-search store exists, with persistence across restarts.

**How it works**:
1. Checks if a store name is persisted to `.file_search_store.json`
2. If found, reuses the existing store (avoids creating new stores on every restart)
3. If not found, creates a new store and persists its name

**Returns**: Store object with `.name` attribute

**Called by**: `/ask`, `/scan-image`, `/classify-plant`, `/webhook` routes

**Example**:
```python
store = ai_services.ensure_file_search_store()
# Use store.name in file_search configurations
```

---

#### `upload_file_to_store(path: str) -> bool`
**Purpose**: Upload a file to the knowledge base with hash-based deduplication.

**How it works**:
1. Computes SHA256 hash of file content
2. Checks upload cache (`upload_cache.json`) to see if file was already uploaded
3. Skips upload if already in store (avoids duplicate uploads)
4. Uploads new file and updates cache
5. Handles operation polling (waits for upload to complete)

**Returns**: `True` if successful or already uploaded, `False` otherwise

**Called by**: `/upload` route, `initialize_knowledge_base()`

**Example**:
```python
success = ai_services.upload_file_to_store('uploads/farming_guide.pdf')
if success:
    logger.info("File available in RAG store")
```

---

#### `initialize_knowledge_base()`
**Purpose**: Automatically upload all knowledge base files on first server request.

**How it works**:
1. Walks through `knowledge_base/` directory tree
2. Finds all `.pdf`, `.txt`, `.json`, `.doc`, `.docx` files
3. Uploads each file using `upload_file_to_store()` with deduplication
4. Logs upload progress

**Timing**: Called in `@app.before_request` on first HTTP request (not on startup to avoid blocking app initialization)

**Example**:
```python
ai_services.initialize_knowledge_base()
# Now all knowledge_base files are available to RAG queries
```

---

#### `load_reference_images(category: str, max_images: int = 2) -> List[Dict]`
**Purpose**: Load reference plant images for classification and infographic generation.

**How it works**:
1. Searches `knowledge_base/plant_images/{category}/` for image files
2. Limits to `max_images` (default 2)
3. Reads binary image data into memory
4. Returns list of dicts with `data` (bytes) and `filename` keys

**Returns**: List of image dictionaries: `[{'data': bytes, 'filename': str}, ...]`

**Called by**: `/classify-plant` endpoint

**Example**:
```python
refs = ai_services.load_reference_images('sugarcane', max_images=3)
for ref in refs:
    print(f"Reference image: {ref['filename']} ({len(ref['data'])} bytes)")
```

---

### B. Infographic Decision Logic

#### `_parse_json_from_text(raw: str) -> Optional[Dict]`
**Purpose**: Extract and parse JSON from model responses with multiple fallback strategies.

**How it works**:
1. Tries to extract fenced JSON: `` ```json {...}``` ``
2. If not found, tries bare JSON: `{...}`
3. If all else fails, tries to parse entire raw text as JSON
4. Returns parsed dict or `None` on complete failure

**Returns**: Parsed JSON dict or `None`

**Called by**: `decide_make_infographic()`, route handlers

**Example**:
```python
raw_response = '```json\n{"make": true}\n```'
parsed = ai_services._parse_json_from_text(raw_response)
# Returns: {'make': True}
```

---

#### `decide_make_infographic(content: str, original_question: str = '') -> Dict`
**Purpose**: Intelligently decide whether to generate an infographic using two strategies.

**Decision Logic**:

1. **SHOWCASE TRIGGERS** (Hardcoded - always generate):
   - "sugarcane growth stages"
   - "fertilizer schedule"
   - "irrigation methods"
   - "disease identification"
   - "sugarcane varieties"
   - "generate image"
   
2. **AI DECISION** (For other queries):
   - Calls Gemini with a JSON schema request
   - Asks model if infographic would help farmers understand

**Returns**:
```python
{
    'make': bool,          # Whether to generate
    'reason': str,         # Explanation of decision
    'style': str          # Suggested style: 'simple', 'chart', 'timeline'
}
```

**Called by**: `/scan-image`, `/classify-plant` routes

**Example**:
```python
decision = ai_services.decide_make_infographic(
    content="Detailed fertilizer info...",
    original_question="Tell me about fertilizer schedule"
)

if decision['make']:
    print(f"Generate {decision['style']} infographic")
    print(f"Reason: {decision['reason']}")
```

---

### C. Image Generation

#### `generate_svg_infographic(content: str, style: str = 'simple') -> Optional[str]`
**Purpose**: Generate a compact SVG infographic from content (lightweight alternative to image generation).

**How it works**:
1. Calls Gemini 3 Pro to produce SVG code
2. Extracts SVG from fenced code blocks or raw response
3. Returns raw SVG string (can be embedded directly in HTML)

**Returns**: SVG string or `None` on failure

**Characteristics**:
- Lightweight (under 800px width)
- No external file save (returns SVG string)
- Suitable for web embedding

**Example**:
```python
svg = ai_services.generate_svg_infographic(content, style='timeline')
if svg:
    return render_template('display_svg.html', svg_content=svg)
```

---

#### `generate_infographic_image(content: str, topic: str) -> Optional[str]`
**Purpose**: Generate high-quality infographic images using Gemini 3 Pro Image with Google Search grounding.

**How it works**:
1. Calls `gemini-3-pro-image-preview` model
2. Uses Google Search tool for real-time agricultural data
3. Generates 4K resolution images in 16:9 aspect ratio
4. Saves PNG files to `uploads/generated_infographics/`
5. Returns relative file path for URL serving

**Returns**: Relative file path (e.g., `generated_infographics/infographic_20250123_143022.png`) or `None` on failure

**Model Configuration**:
- **Model**: `gemini-3-pro-image-preview`
- **Resolution**: 4K
- **Aspect Ratio**: 16:9
- **Tools**: Google Search for grounding
- **Design**: Professional agricultural theme with green/yellow colors

**Called by**: `/ask` endpoint (dual-LLM fallback), `/scan-image`, `/classify-plant`

**Example**:
```python
image_path = ai_services.generate_infographic_image(
    content="Detailed disease info",
    topic="Sugarcane Disease Management"
)

if image_path:
    url = f"/uploads/{image_path}"
    return {'infographic_url': url, 'infographic_reason': 'AI-generated visual guide'}
else:
    logger.error("Image generation failed, falling back to text")
```

---

## Integration with Flask Routes

### Route: `/ask` (Main RAG Chat)
```python
# Pseudocode showing flow
store = ai_services.ensure_file_search_store()  # Get RAG store
response = client.models.generate_content(      # Call LLM 1
    model='gemini-3-pro-preview',
    tools=[file_search_store]
)

# Check if user asked for images and AI refused
if is_image_request and is_ai_refusing:
    image_path = ai_services.generate_infographic_image(...)  # Call LLM 2
    return {'response': text, 'infographic_url': image_path}
else:
    return {'response': text}
```

### Route: `/scan-image` (Image Analysis)
```python
# Analyze uploaded image
store = ai_services.ensure_file_search_store()
response = client.models.generate_content(...)

# Decide if infographic would help
decision = ai_services.decide_make_infographic(analysis_result)
if decision['make']:
    image_path = ai_services.generate_infographic_image(analysis_result)
```

### Route: `/classify-plant` (Plant Classification)
```python
# Load reference images
refs = ai_services.load_reference_images('sugarcane')

# Classify user image with references
response = client.models.generate_content(image_parts)

# Generate infographic if needed
decision = ai_services.decide_make_infographic(classification)
```

### Route: `/upload` (File Upload)
```python
# Upload user files to knowledge base
for file in files:
    ai_services.upload_file_to_store(file_path)
    # File now available to RAG queries
```

---

## Key Design Patterns

### 1. **Module Initialization Pattern**
```python
# app.py calls this once at startup
ai_services.set_client_and_app(client, app, upload_folder)

# Then all functions use module-level CLIENT, FLASK_APP, UPLOAD_FOLDER
# No need to pass these around as parameters
```

### 2. **Persistence Pattern**
- File search store name persisted to `.file_search_store.json`
- Upload cache maintained in `uploads/upload_cache.json`
- Prevents recreating resources on each server restart

### 3. **Graceful Degradation Pattern**
```python
def some_ai_function():
    if CLIENT is None:
        logger.warning("AI unavailable")
        return None
    # Proceed with AI call
```

### 4. **Dual-LLM Fallback Pattern**
```python
# LLM 1: Gemini 3 Pro (text + reasoning)
text_response = client.models.generate_content(model='gemini-3-pro-preview')

# If user requested images but LLM 1 refused:
if image_request and refusal_detected:
    # LLM 2: Gemini 3 Pro Image (image generation)
    image_path = generate_infographic_image()
```

---

## Error Handling & Logging

All functions include comprehensive logging:

```python
logger.info("🕵️ Starting infographic decision logic...")
logger.warning("⚠️ AI client not available")
logger.error("❌ Image generation failed")
```

**Debug Tips**:
- Check `/tmp/app_debug.log` for detailed logs
- Look for `🕵️`, `✅`, `❌` emoji markers for quick scanning
- Logs show model calls, decision logic, image generation details

---

## Testing & Validation

### Test RAG (Knowledge Base)
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Tell me about sugarcane diseases","language":"english"}'
```

### Test Image Generation Fallback
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Generate an infographic for sugarcane growth stages","language":"english"}'
```

### Test Plant Classification
```bash
curl -X POST http://localhost:5000/classify-plant \
  -F "image=@path/to/image.jpg"
```

---

## Future Enhancements

1. **Caching**: Add Redis caching for infographic decisions
2. **Async**: Make image generation async (non-blocking)
3. **Batch Processing**: Process multiple files in `initialize_knowledge_base()`
4. **A/B Testing**: Track which image styles work best for farmers
5. **Monitoring**: Add metrics for AI decision accuracy and image generation success rates

---

## Concrete examples to reference when editing
- To add language-specific instructions: edit `AGRICULTURAL_INSTRUCTIONS` in `app.py` AND add the language option in `templates/index.html` and `translations` (JS).
- To see how uploads are processed: follow `/upload` in `app.py` — files are saved to `uploads/` and then `upload_file_to_store()` is called.
- To add a new endpoint that calls Gemini with files/images: mimic the pattern in `/scan-image` and `/classify-plant` (use `types.Part(inline_data=types.Blob(...))`).

---

## Integration with Flask Routes

### Route: `/ask` (Main RAG Chat)
```python
# Pseudocode showing flow
store = ai_services.ensure_file_search_store()  # Get RAG store
response = client.models.generate_content(      # Call LLM 1
    model='gemini-3-pro-preview',
    tools=[file_search_store]
)

# Check if user asked for images and AI refused
if is_image_request and is_ai_refusing:
    image_path = ai_services.generate_infographic_image(...)  # Call LLM 2
    return {'response': text, 'infographic_url': image_path}
else:
    return {'response': text}
```

---

## Error Handling & Logging

All functions include comprehensive logging:

```python
logger.info("🕵️ Starting infographic decision logic...")
logger.warning("⚠️ AI client not available")
logger.error("❌ Image generation failed")
```

**Debug Tips**:
- Check `/tmp/app_debug.log` for detailed logs
- Look for `🕵️`, `✅`, `❌` emoji markers for quick scanning
- Logs show model calls, decision logic, image generation details

---

## Testing & Validation

### Test RAG (Knowledge Base)
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Tell me about sugarcane diseases","language":"english"}'
```

---

## Future Enhancements

1. **Caching**: Add Redis caching for infographic decisions
2. **Async**: Make image generation async (non-blocking)
3. **Batch Processing**: Process multiple files in `initialize_knowledge_base()`
