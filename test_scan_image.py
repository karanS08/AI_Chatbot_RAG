import os
import sys
import argparse
import requests

# Simple test for /scan-image endpoint with configurable port and image path
def main():
    parser = argparse.ArgumentParser(description="Test /scan-image endpoint")
    parser.add_argument("--host", default=os.getenv("SERVER_HOST", "localhost"), help="Server host (default: localhost)")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", os.getenv("SERVER_PORT", 5000))), help="Server port (default: env PORT/SERVER_PORT or 5000)")
    parser.add_argument("--image", default=os.getenv("TEST_IMAGE", "/home/karan/test_farm1a/germination/dataset/data_asmoli_model/train/images/11_14.png"), help="Path to test image")
    parser.add_argument("--language", default="english", help="Target language")
    parser.add_argument("--prompt", default="Is this showing red rot? Suggest immediate treatment.", help="Optional prompt to guide analysis")
    args = parser.parse_args()

    url = f"http://{args.host}:{args.port}/scan-image"
    image_path = args.image

    if not os.path.isfile(image_path):
        print(f"Image file '{image_path}' not found. Provide a valid path with --image or set TEST_IMAGE env var.")
        sys.exit(1)

    try:
        with open(image_path, 'rb') as f:
            # Infer MIME type from extension
            ext = os.path.splitext(image_path)[1].lower()
            mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
            files = {"file": (os.path.basename(image_path), f, mime)}
            data = {"language": args.language, "prompt": args.prompt}
            print(f"Sending image {image_path} to {url} ...")
            resp = requests.post(url, files=files, data=data, timeout=45)
            print("Status:", resp.status_code)
            try:
                print("Response JSON:")
                print(resp.json())
            except Exception:
                print("Raw Response:")
                print(resp.text)
    except requests.exceptions.ConnectionError as ce:
        print(f"Connection error to {url}. Is the server running? Start the app with PORT={args.port}.")
        sys.exit(2)
    except Exception as e:
        print("Error during request:", e)
        sys.exit(3)


if __name__ == "__main__":
    main()
