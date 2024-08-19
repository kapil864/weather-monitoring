import requests
import json
import base64
from config import USERNAME, PASSWORD


def export_saved_objects(kibana_host, output_file, username, password):

    auth_string = f"{username}:{password}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')

    url = f"http://{kibana_host}:5601/api/saved_objects/_export"
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Basic {auth_base64}',
               'kbn-xsrf': 'true'}
    data = {'type': 'dashboard'}  # Filter for dashboards only
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Saved objects exported to {output_file}")
    else:
        print(f"Error exporting saved objects: {response.text}")


# Example usage:
kibana_host = "localhost"
output_file = "dashboards/saved_objects.ndjson"

export_saved_objects(kibana_host, output_file, USERNAME, PASSWORD)
