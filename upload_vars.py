import os
import requests

# === CONFIGURATION ===
FILE_NAME = "vars.json"  # Local JSON file name
# =====================

# Dynamic path resolution for GitHub Actions / runner environments
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, FILE_NAME)

CENTRAL_BASE_URL = "https://api-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

if not CENTRAL_ACCESS_TOKEN:
    print("[ERROR] CENTRAL_ACCESS_TOKEN environment variable is missing!")
    exit(1)

if not os.path.exists(FILE_PATH):
    print(f"[ERROR] Variable file '{FILE_PATH}' not found!")
    exit(1)

# Correct Aruba Central Template Variables Endpoint
url = f"{CENTRAL_BASE_URL}/configuration/v1/devices/template_variables"

headers = {
    "Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}"
}

with open(FILE_PATH, "rb") as f:
    file_bytes = f.read()

files = {
    "variables": (os.path.basename(FILE_PATH), file_bytes, "application/json")
}

print(f"[+] Uploading template variables from '{FILE_NAME}' to Aruba Central...")
response = requests.post(url, headers=headers, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Variables from '{FILE_NAME}' uploaded successfully!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Upload failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
