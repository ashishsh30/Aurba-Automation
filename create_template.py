import os
import requests

# Set target group to a clean/new template group
GROUP_NAME = "Test-Gateway-V2"            
TEMPLATE_NAME = "Gateway_Template_V2"    
DEVICE_TYPE = "MobilityController"        
FILE_PATH = "gateway_template.cfg"        

CENTRAL_BASE_URL = "https://api-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

if not CENTRAL_ACCESS_TOKEN or not os.path.exists(FILE_PATH):
    print("[ERROR] Missing token or local config file!")
    exit(1)

url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates"

params = {
    "name": TEMPLATE_NAME,
    "device_type": DEVICE_TYPE,
    "version": "ALL",
    "model": "ALL"
}

headers = {"Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}"}

with open(FILE_PATH, "rb") as f:
    files = {"template": (FILE_PATH, f, "text/plain")}
    print(f"[+] Provisioning '{TEMPLATE_NAME}' into group '{GROUP_NAME}'...")
    response = requests.post(url, headers=headers, params=params, files=files)

if response.status_code in [200, 201]:
    print(f"[SUCCESS] Template '{TEMPLATE_NAME}' successfully added to '{GROUP_NAME}'!")
    print(response.text)
else:
    print(f"[ERROR] {response.status_code}: {response.text}")
    exit(1)
