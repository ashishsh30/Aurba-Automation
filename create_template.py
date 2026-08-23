import os
import requests

# === CONFIGURATION ===
GROUP_NAME = "Test-new"                   # Target group name in Aruba Central
TEMPLATE_NAME = "Gateway_Template_V2"     # Name of the template in Central
DEVICE_TYPE = "MobilityController"        # Device type
FILE_PATH = "gateway_template.cfg"        # Local config template file path
# =====================

CENTRAL_BASE_URL = "https://api-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

if not CENTRAL_ACCESS_TOKEN:
    print("[ERROR] CENTRAL_ACCESS_TOKEN environment variable is missing!")
    exit(1)

if not os.path.exists(FILE_PATH):
    print(f"[ERROR] Template file '{FILE_PATH}' not found in repo!")
    exit(1)

# Endpoint: Base group templates URL
url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates"

params = {
    "name": TEMPLATE_NAME,
    "device_type": DEVICE_TYPE,
    "version": "ALL",
    "model": "ALL"
}

headers = {
    "Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}"
}

with open(FILE_PATH, "rb") as f:
    files = {
        "template": (FILE_PATH, f, "text/plain")
    }

    # 1. Use PUT on base URL to update existing template
    print(f"[+] Attempting PUT update for '{TEMPLATE_NAME}' in group '{GROUP_NAME}'...")
    response = requests.put(url, headers=headers, params=params, files=files)

    # 2. Fallback to POST if template does not exist
    if response.status_code == 404:
        print(f"[+] Template not found. Creating via POST...")
        f.seek(0)
        response = requests.post(url, headers=headers, params=params, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Template '{TEMPLATE_NAME}' updated successfully in group '{GROUP_NAME}'!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Request failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
