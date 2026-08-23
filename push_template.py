import requests

TOEKN ="L6lpWL4eHGGCYi4iObVXmvI60IR28VRM"

headers = {
  "Authorization": f"Beared {L6lpWL4eHGGCYi4iObVXmvI60IR28VRM}"

url = "https://apigw-ap.central.arubanetworks.com/configuration/v2/groups"

r = requests.get(url, headers=headers)

print(r.status_code)
print(r.text)
