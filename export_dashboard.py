import requests
import json


def export_saved_objects(kibana_host, output_file):
    url = f"http://{kibana_host}:5601/api/saved_objects/_export"
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Basic ZWxhc3RpYzoxMjM0NTY=',
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

export_saved_objects(kibana_host, output_file)
