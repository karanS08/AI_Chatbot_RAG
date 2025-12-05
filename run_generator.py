import sys
import os

# --- Add the correct site-packages to the Python path ---
# This ensures that the installed libraries like google-generativeai are found.
site_packages_path = '/home/karan/.local/lib/python3.13/site-packages'
if site_packages_path not in sys.path:
    print(f"🔧 Adding '{site_packages_path}' to Python path.")
    sys.path.append(site_packages_path)

# --- Set the working directory ---
# This helps the script find the 'infographic_generator' module correctly.
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"📂 Changed working directory to: '{script_dir}'")

# --- Now, import and run the main script ---
try:
    print("🚀 Attempting to import and run the main script...")
    from infographic_generator import generate_infographic
    generate_infographic.main()
except ModuleNotFoundError as e:
    print(f"🔴 Critical Error: Module not found even after path modification.")
    print(f"   Error details: {e}")
    print(f"   Current Python path: {sys.path}")
except ImportError as e:
    print(f"🔴 Critical Error: Could not import the script.")
    print(f"   Error details: {e}")
except Exception as e:
    print(f"🔴 An unexpected error occurred: {e}")

