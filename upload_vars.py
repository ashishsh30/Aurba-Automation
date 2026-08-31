import os
import requests

# === CONFIGURATION ===
GROUP_NAME = "Test-new"                 # Target group name in Aruba Central
FILE_NAME = "var.json"                  # Local JSON file name
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

# Endpoint for Aruba Central Group Variables API
base_url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/variables"

headers = {
    "Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}"
}

# Load file into memory for instant PATCH -> POST failover
with open(FILE_PATH, "rb") as f:
    file_bytes = f.read()

files = {
    "variables": (os.path.basename(FILE_PATH), file_bytes, "application/json")
}

# 1. Attempt PATCH to update existing group variables
print(f"[+] Attempting to update group variables from '{FILE_NAME}' for group '{GROUP_NAME}' via PATCH...")
response = requests.patch(base_url, headers=headers, files=files)

# 2. Fallback to POST if variables set doesn't exist yet or endpoint returns 400/404
if response.status_code in [400, 404] and ("not found" in response.text.lower() or "does not exist" in response.text.lower()):
    print(f"[+] Variables for group '{GROUP_NAME}' not found. Falling back to POST creation...")
    response = requests.post(base_url, headers=headers, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Variables from '{FILE_NAME}' uploaded successfully to group '{GROUP_NAME}'!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Request failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
