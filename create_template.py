import os
import requests

# === CONFIGURATION ===
GROUP_NAME = "Test-new"                   # Target group name in Aruba Central
TEMPLATE_NAME = "Gateway_Template_V2"     # Template name
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

headers = {
    "Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}"
}

# 1. DELETE the existing template using the template_name in the URL path
delete_url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates/{TEMPLATE_NAME}"

print(f"[+] Attempting to delete existing template '{TEMPLATE_NAME}' from group '{GROUP_NAME}'...")
del_resp = requests.delete(delete_url, headers=headers)

if del_resp.status_code in [200, 204]:
    print(f"[+] Template '{TEMPLATE_NAME}' successfully deleted.")
elif del_resp.status_code == 404:
    print(f"[+] Template '{TEMPLATE_NAME}' not found. Proceeding with creation.")
else:
    print(f"[!] Delete response ({del_resp.status_code}): {del_resp.text}")

# 2. POST the fresh template to the group
create_url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates"
create_params = {
    "name": TEMPLATE_NAME,
    "device_type": DEVICE_TYPE,
    "version": "ALL",
    "model": "ALL"
}

with open(FILE_PATH, "rb") as f:
    files = {
        "template": (FILE_PATH, f, "text/plain")
    }

    print(f"[+] Uploading fresh template '{TEMPLATE_NAME}'...")
    response = requests.post(create_url, headers=headers, params=create_params, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Template '{TEMPLATE_NAME}' created/updated successfully in group '{GROUP_NAME}'!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Request failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
