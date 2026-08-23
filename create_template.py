import os
import requests

# === CONFIGURATION ===
GROUP_NAME = "Test-new"                   # Target group name in Aruba Central
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

base_url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates"

# 1. GET existing template with required pagination parameters
get_params = {
    "limit": 20,
    "offset": 0,
    "device_type": DEVICE_TYPE
}

print(f"[+] Querying existing templates in group '{GROUP_NAME}'...")
get_resp = requests.get(base_url, headers=headers, params=get_params)

target_template_name = None

if get_resp.status_code == 200:
    data = get_resp.json()
    templates_list = data.get("templates", []) if isinstance(data, dict) else data
    
    for t in templates_list:
        if t.get("device_type") == DEVICE_TYPE or t.get("device_type") == "ALL":
            target_template_name = t.get("name") or t.get("template_name")
            print(f"[+] Identified existing template: '{target_template_name}'")
            break

if not target_template_name:
    target_template_name = "Gateway_Template_V2"
    print(f"[!] No existing template detected via GET. Falling back to default name '{target_template_name}'")

# 2. PATCH update using the actual template name retrieved from Central
patch_params = {
    "name": target_template_name,
    "device_type": DEVICE_TYPE,
    "version": "ALL",
    "model": "ALL"
}

with open(FILE_PATH, "rb") as f:
    files = {
        "template": (FILE_PATH, f, "text/plain")
    }

    print(f"[+] Updating template '{target_template_name}' in group '{GROUP_NAME}' via PATCH...")
    response = requests.patch(base_url, headers=headers, params=patch_params, files=files)

# Fallback to POST if no template exists to update
if response.status_code in [400, 404] and "not found" in response.text.lower():
    print(f"[+] Template not found via PATCH. Creating new template via POST...")
    with open(FILE_PATH, "rb") as f:
        files = {"template": (FILE_PATH, f, "text/plain")}
        response = requests.post(base_url, headers=headers, params=patch_params, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Template '{target_template_name}' successfully updated in group '{GROUP_NAME}'!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Request failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
