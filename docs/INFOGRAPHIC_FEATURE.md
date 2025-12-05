````markdown
# PNG Infographic Generation Feature

## Overview
The chatbot now uses Gemini's **Imagen 3.0** model to generate PNG infographics when relevant. This feature enhances user experience by providing visual representations of complex agricultural information.

## How It Works

### 1. **Decision Logic**
- When the API receives a response (from `/ask`, `/scan-image`, or `/classify-plant`), it first asks Gemini to decide if an infographic would be helpful
- The decision considers factors like:
  - Content complexity
  - Presence of step-by-step instructions
  - Data that would benefit from visualization
  - User context (sugarcane farmer audience)

### 2. **Image Generation**
- If Gemini decides an infographic would help, the system calls the **Imagen 3.0 API**
- The prompt describes the desired infographic style:
  - Clear, professional design
  - Large readable text
  - Simple icons
  - Farmer-friendly layout
  - Easy-to-understand colors

### 3. **Storage & Serving**
- Generated PNG images are saved in: `uploads/infographics/`
- Each image has a unique timestamp-based filename
- Images are served via the `/uploads/<path>` route
- Frontend displays images with download and "Open in new tab" options

## API Response Format

### `/ask` Endpoint
```json
{
  "response": "Main text response...",
  "infographic_url": "/uploads/infographics/infographic_1733220123456.png",
  "infographic_reason": "Step-by-step guide works better visually"
}
```

### `/scan-image` Endpoint
```json
{
  "summary": "Crop analysis...",
  "diagnosis": ["Red rot detected"],
  "recommendations": ["Treatment steps..."],
  "infographic_url": "/uploads/infographics/infographic_1733220789012.png",
  "infographic_reason": "Visual disease identification guide"
}
```

### `/classify-plant` Endpoint
```json
{
  "classification": "sugarcane",
  "confidence": 0.95,
  "plant_type": "Sugarcane variety CO 86032",
  "infographic_url": "/uploads/infographics/infographic_1733221234567.png",
  "infographic_reason": "Plant characteristics comparison chart"
}
```

## Frontend Implementation

### JavaScript Functions

#### `renderInfographicImage(imageUrl, reason)`
Renders a PNG infographic block with:
- Image display
- Caption showing why the infographic was created
- Download button
- "Open in new tab" button

#### Event Delegation
```javascript
// Handles "Open in new tab" button clicks
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('infographic-open-image')) {
        const url = e.target.getAttribute('data-url');
        window.open(url, '_blank');
    }
});
```

### CSS Styling
```css
.infographic {
  border: 1px solid rgba(0,0,0,0.06);
  padding: 10px;
  border-radius: 8px;
  background: #fff;
}

.infographic-inner img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

.infographic-download,
.infographic-open-image {
  background: #e6f7f2;
  color: #036;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}
```

## Backend Implementation

### Key Functions

#### `decide_make_infographic(content: str) -> Dict`
```python
# Asks Gemini to decide if infographic would help
# Returns: {'make': bool, 'reason': str, 'style': str}
```

#### `generate_infographic_image(content: str, style: str) -> Optional[str]`
```python
# Generates PNG infographic using Imagen 3.0
# Returns: Relative path like "infographics/infographic_123.png"
```

### Imagen API Call
```python
response = client.models.generate_images(
    model='imagen-3.0-generate-001',
    prompt=prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        include_rai_reason=False,
        output_mime_type='image/png'
    )
)
```

## Configuration

### Environment Variables
- **GOOGLE_API_KEY**: Required for Gemini and Imagen API access
- Must have access to both `gemini-3-pro-preview` and `imagen-3.0-generate-001`

### File Paths
- Infographics directory: `uploads/infographics/`
- Auto-created if doesn't exist
- Files named: `infographic_<timestamp>.png`

## Testing

### Manual Testing
1. Start the server: `gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app`
2. Ask a complex question: "What are the steps for planting sugarcane?"
3. Check response for `infographic_url` field
4. Verify image is accessible at the URL

### Automated Testing
```bash
python test_infographic_generation.py
```

## Troubleshooting

### Infographics Not Generating
**Possible causes:**
1. **Missing API key**: Check `GOOGLE_API_KEY` is set
2. **API access**: Ensure API key has Imagen 3.0 access
3. **Conservative decision**: Gemini may decide infographic isn't needed
4. **Generation failure**: Check server logs for error messages

### Images Not Displaying
**Possible causes:**
1. **File permissions**: Ensure `uploads/infographics/` is writable
2. **Path issues**: Verify `/uploads/<path>` route is working
3. **CORS issues**: Check CORS configuration for image serving

### Large File Sizes
- PNG images can be large (500KB - 2MB typical)
- Consider implementing:
  - Image compression
  - Caching strategy
  - Periodic cleanup of old infographics

## Fallback Behavior

The system gracefully handles failures:
- If decision API fails → No infographic, just text response
- If image generation fails → No infographic, just text response
- If file save fails → Error logged, no infographic shown
- Frontend continues to work even if infographic fails to load

## Future Enhancements

### Potential Improvements
1. **Caching**: Store generated infographics for common queries
2. **Multiple sizes**: Generate thumbnail + full-size versions
3. **Localization**: Generate infographics in user's language
4. **Analytics**: Track which infographics are most helpful
5. **User feedback**: Allow users to rate infographic usefulness
6. **Template system**: Pre-defined templates for common topics
7. **Compression**: Optimize PNG size with lossless compression

## Performance Considerations

### Generation Time
- Imagen API typically takes 5-15 seconds
- Server has 120s timeout to accommodate this
- UI shows loading indicator during generation

### Storage
- Each infographic: ~500KB - 2MB
- Recommend periodic cleanup of old files
- Consider cloud storage for production (S3, GCS, etc.)

### API Costs
- Imagen API calls have associated costs
- Conservative decision logic minimizes unnecessary generations
- Monitor API usage and set quotas as needed

## Security

### Image Validation
- Only saves to `uploads/infographics/` directory
- Timestamp-based filenames prevent path traversal
- No user-provided filenames accepted

### Content Safety
- Imagen 3.0 has built-in safety filters
- `include_rai_reason=False` reduces response size
- Consider adding content moderation layer

## Backwards Compatibility

### SVG Support Retained
- Original SVG generation (`generate_svg_infographic`) still available
- Frontend checks for both `infographic_svg` and `infographic_url`
- Can switch between PNG/SVG based on use case

### Migration Path
- No breaking changes to existing API contracts
- New fields are optional
- Clients without infographic support work normally

````
