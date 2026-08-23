import os
import requests

GROUP_NAME = "Test-new"
CENTRAL_BASE_URL = "https://api-ap.central.arubanetworks.com"
CENTRAL_ACCESS_TOKEN = os.getenv("CENTRAL_ACCESS_TOKEN")

headers = {"Authorization": f"Bearer {CENTRAL_ACCESS_TOKEN}"}
url = f"{CENTRAL_BASE_URL}/configuration/v1/groups/{GROUP_NAME}/templates"

response = requests.get(url, headers=headers)
print(f"Existing templates in {GROUP_NAME}:")
print(response.text)
