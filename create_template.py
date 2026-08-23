import os
import requests

# === CONFIGURATION ===
GROUP_NAME = "Test-new"                   # Target group name
NEW_TEMPLATE_NAME = "Gateway_Template_V3" # Distinct template name
DEVICE_TYPE = "MobilityController"        # Device type

# Supported Aruba Central model strings for Gateways:
# Options: "70XX", "72XX", "90XX", "92XX", "MC-VA"
MODEL = "70XX"                            
VERSION = "ALL"                           # Leave as "ALL" for all firmware versions
FILE_PATH = "gateway_template.cfg"
# =====================

CENTRAL_BASE_URL = "https://api-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

if not CENTRAL_ACCESS_TOKEN:
    print("[ERROR] CENTRAL_ACCESS_TOKEN environment variable is missing!")
    exit(1)

if not os.path.exists(FILE_PATH):
    print(f"[ERROR] Template file '{FILE_PATH}' not found in repo!")
    exit(1)

url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates"

params = {
    "name": NEW_TEMPLATE_NAME,
    "device_type": DEVICE_TYPE,
    "version": VERSION,
    "model": MODEL
}

headers = {
    "Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}"
}

with open(FILE_PATH, "rb") as f:
    files = {
        "template": (FILE_PATH, f, "text/plain")
    }

    print(f"[+] Creating template '{NEW_TEMPLATE_NAME}' for model family '{MODEL}' in group '{GROUP_NAME}'...")
    response = requests.post(url, headers=headers, params=params, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Template '{NEW_TEMPLATE_NAME}' successfully added to group '{GROUP_NAME}'!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Request failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
