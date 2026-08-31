import os
import json
import requests

# === CONFIGURATION ===
FILE_NAME = "vars.json"
# =====================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, FILE_NAME)

CENTRAL_BASE_URL = "https://api-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

if not CENTRAL_ACCESS_TOKEN:
    print("[ERROR] CENTRAL_ACCESS_TOKEN environment variable is missing!")
    exit(1)

if not os.path.exists(FILE_PATH):
    print(f"[ERROR] Variable file '{FILE_PATH}' not found!")
    exit(1)

# Load target variables from local JSON file
with open(FILE_PATH, "r") as f:
    try:
        local_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse local '{FILE_NAME}': {e}")
        exit(1)

headers = {
    "Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}"
}

# 1. Get current variables from Aruba Central to identify existing values
get_url = f"{CENTRAL_BASE_URL}/configuration/v1/devices/template_variables"
print("[+] Fetching existing variables from Aruba Central...")
get_resp = requests.get(get_url, headers=headers)

remote_data = {}
if get_resp.status_code == 200:
    try:
        remote_data = get_resp.json().get("variables", {})
    except Exception:
        remote_data = {}
else:
    print(f"[!] Warning: Could not fetch existing variables (HTTP {get_resp.status_code}). Proceeding with full payload upload.")

# 2. Compare local variables against remote variables for each device serial
delta_payload = {}
skipped_count = 0
updated_count = 0

for serial, local_vars in local_data.items():
    remote_vars = remote_data.get(serial, {})
    device_delta = {}

    for key, val in local_vars.items():
        # Mandatory system identifiers are always retained
        if key in ["_sys_serial", "_sys_lan_mac"]:
            device_delta[key] = val
            continue

        # Check if key value has changed compared to Central
        if remote_vars.get(key) == val:
            skipped_count += 1
        else:
            device_delta[key] = val
            updated_count += 1

    # Only include device in upload if actual variable changes exist
    non_sys_keys = [k for k in device_delta if k not in ["_sys_serial", "_sys_lan_mac"]]
    if non_sys_keys:
        delta_payload[serial] = device_delta

# 3. Handle upload logic
if not delta_payload and skipped_count > 0:
    print(f"[SUCCESS] No variable changes detected ({skipped_count} variables unchanged). Skipping API upload!")
    exit(0)

print(f"[+] Found {updated_count} updated variable(s). Skipped {skipped_count} unchanged variable(s).")
print("[+] Uploading delta variables payload to Aruba Central...")

# Write delta payload into temporary JSON format for multipart form upload
delta_json_bytes = json.dumps(delta_payload, indent=2).encode("utf-8")
files = {
    "variables": (FILE_NAME, delta_json_bytes, "application/json")
}

post_url = f"{CENTRAL_BASE_URL}/configuration/v1/devices/template_variables"
response = requests.post(post_url, headers=headers, files=files)

if response.status_code in [200, 201]:
    print("[SUCCESS] Delta variables uploaded successfully!")
    print(f"API Response: {response.text}")
else:
    print(f"[ERROR] Upload failed with status code {response.status_code}")
    print(f"API Response: {response.text}")
    exit(1)
