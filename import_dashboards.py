import requests
import base64
import json
from config import USERNAME, PASSWORD

def import_saved_objects(kibana_host, input_file, username, password):
    url = f"http://{kibana_host}:5601/api/saved_objects/_import"

    # Basic Auth
    auth_string = f"{username}:{password}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
    headers = {'Authorization': f'Basic {auth_base64}', 'Content-Type': 'application/json'}

    with open(input_file, 'rb') as f:
        data = f.read()

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("Saved objects imported successfully")
    else:
        print(f"Error importing saved objects: {response.text}")

# Example usage:
kibana_host = "localhost"
input_file = "dashboards/saved_objects.ndjson"
username = USERNAME
password = PASSWORD

import_saved_objects(kibana_host, input_file, username, password)