#!/bin/bash
# This script sets the Python path and runs the infographic generator.

# --- Set the path to your site-packages ---
SITE_PACKAGES="/home/karan/.local/lib/python3.13/site-packages"

# --- Export the PYTHONPATH ---
export PYTHONPATH="$PYTHONPATH:$SITE_PACKAGES"

echo "🐍 PYTHONPATH set to: $PYTHONPATH"
echo "🚀 Running the infographic generator..."

# --- Run the script ---
python3 infographic_generator/generate_infographic.py
