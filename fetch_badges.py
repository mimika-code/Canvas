import requests
import json
import os
import time

DUNE_API_KEY = os.environ.get('DUNE_API_KEY')
QUERY_ID = 4092808
RESULTS_PER_PAGE = 50

def fetch_data(query_id, offset=0):
    url = f"https://api.dune.com/api/v1/query/{query_id}/results?limit={RESULTS_PER_PAGE}&offset={offset}"
    headers = {"x-dune-api-key": DUNE_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def update_badge_data():
    badge_info = {}
    offset = 0

    while True:
        data = fetch_data(QUERY_ID, offset)
        if data and 'result' in data and data['result']['rows']:
            for row in data['result']['rows']:
                badge_name = row['badge_name'] 
                total_minted = row['total_minted']
                badge_info[badge_name] = total_minted
            offset += RESULTS_PER_PAGE
        else:
            break

    with open("badge_data.json", "w") as f:
        json.dump(badge_info, f, separators=(',', ':'))  

    print("badge_data.json updated successfully with content:", badge_info)

if __name__ == "__main__":
    update_badge_data()
