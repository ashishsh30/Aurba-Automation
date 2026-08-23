import os
import requests

# === CONFIGURATION ===
GROUP_NAME = "Test-new"                   # Target group name in Aruba Central
DEVICE_TYPE = "MobilityController"        # Device type
FILE_PATH = "gateway_template.cfg"        # Local config template file path
DEFAULT_TEMPLATE_NAME = "Gateway_Template_V2"
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

# 1. Query existing templates in group using required limit/offset
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
    # Aruba Central template listing payload structures
    templates_list = data.get("data", []) if isinstance(data, dict) and "data" in data else data.get("templates", []) if isinstance(data, dict) else []
    
    for t in templates_list:
        if t.get("device_type") in [DEVICE_TYPE, "ALL"]:
            target_template_name = t.get("name") or t.get("template_name")
            print(f"[+] Detected active template in group: '{target_template_name}'")
            break

if not target_template_name:
    target_template_name = DEFAULT_TEMPLATE_NAME
    print(f"[!] Active template name not found in GET response. Using fallback: '{target_template_name}'")

# 2. Update existing template via PATCH using 'template_name'
patch_params = {
    "template_name": target_template_name,
    "device_type": DEVICE_TYPE,
    "version": "ALL",
    "model": "ALL"
}

with open(FILE_PATH, "rb") as f:
    files = {
        "template": (FILE_PATH, f, "text/plain")
    }

    print(f"[+] Executing PATCH update on template '{target_template_name}' in group '{GROUP_NAME}'...")
    response = requests.patch(base_url, headers=headers, params=patch_params, files=files)

# 3. Fallback to POST with 'name' if no template exists to update
if response.status_code in [400, 404] and "not found" in response.text.lower():
    print(f"[+] Template not found for update. Creating new template via POST...")
    post_params = {
        "name": target_template_name,
        "device_type": DEVICE_TYPE,
        "version": "ALL",
        "model": "ALL"
    }
    with open(FILE_PATH, "rb") as f:
        files = {"template": (FILE_PATH, f, "text/plain")}
        response = requests.post(base_url, headers=headers, params=post_params, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Template '{target_template_name}' updated successfully in group '{GROUP_NAME}'!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Request failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
