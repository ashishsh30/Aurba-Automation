import os
import yaml
import requests

# Retrieve credentials from GitHub Action secrets
CENTRAL_BASE_URL = os.environ["ARUBA_CENTRAL_URL"] # e.g., https://app1-apigw.central.arubanetworks.com
ACCESS_TOKEN = os.environ["ARUBA_CENTRAL_TOKEN"]

def upload_variables_to_apc():
    with open("inventory.yml", "r") as file:
        data = yaml.safe_load(file)

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    for group in data.get("groups", []):
        group_name = group["group_name"]
        
        # Aruba Central expects payload structured as: { "SERIAL_NUM": { "var1": "val1" } }
        variables_payload = {}
        for dev in group.get("devices", []):
            serial = dev["_sys_serial"]
            variables_payload[serial] = dev

        # API Call to push variables to the APC Group
        url = f"{CENTRAL_BASE_URL}/configuration/v1/devices/variables?group={group_name}"
        response = requests.post(url, json={"variables": variables_payload}, headers=headers)

        if response.status_code == 200:
            print(f"Successfully pushed variables for group: {group_name}")
        else:
            print(f"Failed to push to {group_name}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    upload_variables_to_apc()
