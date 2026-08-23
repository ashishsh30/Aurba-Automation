import os
import requests

# === CONFIGURATION ===
GROUP_NAME = "Test-new"                   # Target group name in Aruba Central
TEMPLATE_NAME = "Gateway_Template_V2"     # Name of the existing template to update
DEVICE_TYPE = "MobilityController"        # Device type
FILE_PATH = "gateway_template.cfg"        # Local path to config template file
# =====================

CENTRAL_BASE_URL = "https://api-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

if not CENTRAL_ACCESS_TOKEN:
    print("[ERROR] CENTRAL_ACCESS_TOKEN environment variable is missing!")
    exit(1)

if not os.path.exists(FILE_PATH):
    print(f"[ERROR] Template file '{FILE_PATH}' not found in repo!")
    exit(1)

# Target the specific template path to perform an in-place update
url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates/{TEMPLATE_NAME}"

params = {
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

    print(f"[+] Updating existing template '{TEMPLATE_NAME}' in group '{GROUP_NAME}'...")
    response = requests.post(url, headers=headers, params=params, files=files)

# Fallback: If template is missing (404), POST to group base path to create it fresh
if response.status_code == 404:
    print(f"[+] Template '{TEMPLATE_NAME}' not found. Creating it as new...")
    create_url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates"
    create_params = {
        "name": TEMPLATE_NAME,
        "device_type": DEVICE_TYPE,
        "version": "ALL",
        "model": "ALL"
    }
    with open(FILE_PATH, "rb") as f:
        files = {"template": (FILE_PATH, f, "text/plain")}
        response = requests.post(create_url, headers=headers, params=create_params, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Template '{TEMPLATE_NAME}' pushed successfully to group '{GROUP_NAME}'!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Request failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
