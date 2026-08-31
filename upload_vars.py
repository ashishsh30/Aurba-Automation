import os
import sys
import requests

# Retrieve environment variables
access_token = os.environ.get("CENTRAL_ACCESS_TOKEN")
target_group = os.environ.get("ARUBA_GROUP_NAME", "Test-new")
host = "https://app2-ap.central.arubanetworks.com"

if not access_token:
    print("Error: CENTRAL_ACCESS_TOKEN is missing!")
    sys.exit(1)

# Aruba Central API endpoint for uploading CSV/JSON template variables
url = f"{host}/configuration/v1/devices/template_variables"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Open and send the vars.json file
try:
    with open("vars.json", "rb") as f:
        # If your endpoint expects group param in query string:
        params = {"group": target_group}
        response = requests.post(url, headers=headers, params=params, data=f)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")

        if response.status_code not in [200, 201]:
            print("Failed to upload variables to Aruba Central.")
            sys.exit(1)

except Exception as e:
    print(f"Execution Error: {e}")
    sys.exit(1)
