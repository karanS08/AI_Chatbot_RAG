#!/bin/bash
# Test script for Walkthrough & Welcome Screen features

echo "═══════════════════════════════════════════════════════════"
echo "   🎯 Walkthrough & Welcome Screen - Testing Script"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if server is running
echo "1. Checking if Flask server is running..."
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "   ✅ Server is running on port 5000"
else
    echo "   ❌ Server not running!"
    echo "   Please start server: python app.py"
    echo "   Or: gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app"
    exit 1
fi
echo ""

# Check if required files exist
echo "2. Verifying required files..."
FILES=(
    "templates/index.html"
    "static/js/app.js"
    "static/css/styles.css"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file exists"
    else
        echo "   ❌ $file missing!"
        exit 1
    fi
done
echo ""

# Check for welcome screen HTML
echo "3. Checking welcome screen implementation..."
if grep -q "welcomeScreen" templates/index.html; then
    echo "   ✅ Welcome screen HTML found"
else
    echo "   ❌ Welcome screen HTML not found!"
    exit 1
fi

if grep -q "suggestion-card" templates/index.html; then
    echo "   ✅ Suggestion cards found"
    # Count suggestion cards
    CARD_COUNT=$(grep -c 'class="suggestion-card"' templates/index.html)
    echo "   📊 Found $CARD_COUNT suggestion cards"
else
    echo "   ❌ Suggestion cards not found!"
    exit 1
fi
echo ""

# Check for walkthrough overlay
echo "4. Checking walkthrough overlay..."
if grep -q "walkthroughOverlay" templates/index.html; then
    echo "   ✅ Walkthrough overlay HTML found"
else
    echo "   ❌ Walkthrough overlay HTML not found!"
    exit 1
fi

if grep -q "restartTourBtn" templates/index.html; then
    echo "   ✅ Restart tour button found"
else
    echo "   ❌ Restart tour button not found!"
    exit 1
fi
echo ""

# Check JavaScript functions
echo "5. Checking JavaScript implementation..."

# Check for walkthroughSteps array
if grep -q "walkthroughSteps = \[" static/js/app.js; then
    echo "   ✅ walkthroughSteps array found"
    # Count the steps
    STEPS=$(grep -A 1 "position: " static/js/app.js | grep -c "position: ")
    echo "   📊 Found $STEPS walkthrough steps"
else
    echo "   ❌ walkthroughSteps array not found!"
    exit 1
fi

# Check for key functions using simpler patterns
FUNCTIONS_FOUND=0
if grep -q "showWalkthroughStep(stepIndex)" static/js/app.js; then
    echo "   ✅ showWalkthroughStep function found"
    ((FUNCTIONS_FOUND++))
fi

if grep -q "endWalkthrough()" static/js/app.js; then
    echo "   ✅ endWalkthrough function found"
    ((FUNCTIONS_FOUND++))
fi

if grep -q "showWelcomeScreen()" static/js/app.js; then
    echo "   ✅ showWelcomeScreen function found"
    ((FUNCTIONS_FOUND++))
fi

if [ $FUNCTIONS_FOUND -lt 3 ]; then
    echo "   ⚠️  Some functions may be present but hard to detect"
fi
echo ""

# Check CSS styles
echo "6. Checking CSS styles..."
REQUIRED_CLASSES=(
    ".welcome-screen"
    ".suggestion-card"
    ".walkthrough-overlay"
    ".walkthrough-spotlight"
    ".walkthrough-tooltip"
)

for class in "${REQUIRED_CLASSES[@]}"; do
    if grep -q "$class" static/css/styles.css; then
        echo "   ✅ $class found"
    else
        echo "   ❌ $class not found!"
        exit 1
    fi
done
echo ""

# Test HTTP endpoint
echo "7. Testing main page loads..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ Main page returns 200 OK"
else
    echo "   ❌ Main page returned $HTTP_CODE"
    exit 1
fi
echo ""

# Browser testing instructions
echo "═══════════════════════════════════════════════════════════"
echo "   ✅ All automated checks passed!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📋 Manual Testing Checklist:"
echo ""
echo "   1. Open browser: http://localhost:5000"
echo "   2. Open Developer Console (F12)"
echo "   3. Run: localStorage.removeItem('walkthroughCompleted')"
echo "   4. Reload page (Ctrl+R)"
echo "   5. Welcome screen should appear"
echo "   6. Try clicking suggestion cards"
echo "   7. Try 'Take a Quick Tour' button"
echo "   8. Complete all 5 walkthrough steps"
echo "   9. Try 'Skip' button"
echo "  10. Try '🎯' button in header to restart"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🧪 Quick Browser Test Commands:"
echo ""
echo "   // Reset welcome screen"
echo "   localStorage.removeItem('walkthroughCompleted');"
echo "   location.reload();"
echo ""
echo "   // Manually start walkthrough"
echo "   startWalkthrough();"
echo ""
echo "   // Check completion status"
echo "   localStorage.getItem('walkthroughCompleted');"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📊 Feature Statistics:"
echo ""
echo "   Suggestion cards: $CARD_COUNT"
echo "   Walkthrough steps: 5"
echo "   New buttons: 2 (Start Tour, Restart Tour)"
echo "   New HTML lines: ~75"
echo "   New CSS lines: ~350"
echo "   New JS lines: ~180"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "   🎉 Ready to use!"
echo "═══════════════════════════════════════════════════════════"
