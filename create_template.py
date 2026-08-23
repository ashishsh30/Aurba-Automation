import os
import requests

CENTRAL_URL = "https://api-ap.central.arubanetworks.com"
ACCESS_TOKEN = os.environ.get("CENTRAL_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise ValueError("CENTRAL_ACCESS_TOKEN environment variable is missing.")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

url = f"{CENTRAL_URL}/configuration/v1/templates"

# Add your payload and POST logic below
