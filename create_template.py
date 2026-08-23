import os
import requests

# === EDIT THESE VALUES ===
GROUP_NAME = "Test-new"      # Case-sensitive Group Name in APC
NEW_TEMPLATE_NAME = "Gateway_Template_V2" # Name for your NEW template
DEVICE_TYPE = "MobilityController"        # Device type
FILE_PATH = "gateway_template.cfg"        # Template filename in GitHub
# =========================

# Correct API Gateway URL for app2-ap cluster
CENTRAL_BASE_URL = "https://apigw-app2-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

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

response = requests.post(url, headers=headers, json=payload)

if response.status_code in [200, 201]:
    print(f"SUCCESS: Created template '{NEW_TEMPLATE_NAME}' in group '{GROUP_NAME}'")
else:
    print(f"ERROR ({response.status_code}): {response.text}")
    exit(1)
