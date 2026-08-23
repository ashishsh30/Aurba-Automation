import os
import requests

GROUP_NAME = "Test-new"
# Must match the name of the template currently in the group
TEMPLATE_NAME = "Gateway_Template_V2"
FILE_PATH = "gateway_template.cfg"

CENTRAL_BASE_URL = "https://api-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

if not CENTRAL_ACCESS_TOKEN or not os.path.exists(FILE_PATH):
    print("[ERROR] Missing token or file.")
    exit(1)

# PUT endpoint to update an existing template in place
url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates/{TEMPLATE_NAME}"

headers = {"Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}"}

with open(FILE_PATH, "rb") as f:
    files = {"template": (FILE_PATH, f, "text/plain")}
    print(f"[+] Updating existing template '{TEMPLATE_NAME}' in group '{GROUP_NAME}'...")
    response = requests.put(url, headers=headers, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Template '{TEMPLATE_NAME}' successfully updated!")
else:
    print(f"[ERROR] Status Code {response.status_code}: {response.text}")
    exit(1)
