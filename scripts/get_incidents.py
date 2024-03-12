"""Get incidents."""
import requests
import json
import sys
import os

api_key = os.getenv('PAGERDUTY_API_KEY')

if api_key is None:
    sys.exit(1)

url = 'https://api.pagerduty.com/incidents?limit=100&date_range=all'
headers = {
    'Accept': 'application/vnd.pagerduty+json;version=2',
    'Authorization': f'Token token={api_key}'
}
all_incidents = []

while url:
    response = requests.get(url, headers=headers, timeout=30)
    print(len(all_incidents))
    data = response.json()
    if data.get('more', False):
        limit = data['limit']
        offset = data['offset']
        url = f'https://api.pagerduty.com/incidents?limit={limit}&offset={offset}'

    if 'incidents' in data:
        all_incidents.extend(data['incidents'])
    else:
        url = None

    with open('incidents.json', 'w') as f:
        json.dump(all_incidents, f)
 