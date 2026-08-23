import os
import requests

# === CONFIGURATION ===
GROUP_NAME = "Test-new"                   # Target group name in Aruba Central
NEW_TEMPLATE_NAME = "Gateway_Template_V2" # Name for your NEW template
DEVICE_TYPE = "MobilityController"        # Device type for Gateways
FILE_PATH = "gateway_template.cfg"        # Local path to config template file
# =====================

# Confirmed API Gateway URL from your Swagger UI
CENTRAL_BASE_URL = "https://api-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

if not CENTRAL_ACCESS_TOKEN:
    print("[ERROR] CENTRAL_ACCESS_TOKEN environment variable is missing!")
    exit(1)

# Check if template file exists
if not os.path.exists(FILE_PATH):
    print(f"[ERROR] Template file '{FILE_PATH}' not found in repo!")
    exit(1)

# Read local template file content
with open(FILE_PATH, "r") as f:
    template_content = f.read()

url = f"{CENTRAL_BASE_URL}/configuration/v1/templates"

payload = {
    "group": GROUP_NAME,
    "template_name": NEW_TEMPLATE_NAME,
    "device_type": DEVICE_TYPE,
    "model": "ALL",
    "version": "ALL",
    "template_format": "TEXT",
    "template_content": template_content
}

headers = {
    "Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

print(f"[+] Sending POST request to: {url}")
response = requests.post(url, headers=headers, json=payload)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Template '{NEW_TEMPLATE_NAME}' successfully created in group '{GROUP_NAME}'!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Request failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
