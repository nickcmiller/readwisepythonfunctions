import json
import os
from dotenv import load_dotenv
import datetime
import requests


load_dotenv()
readwise_token = os.getenv('READWISE_TOKEN')


def fetch_highlights(token=readwise_token, updated_after_days=None):
    full_data = []
    next_page_cursor = None
    while True:
        params = {}
        if next_page_cursor:
            params['pageCursor'] = next_page_cursor
        if updated_after_days:
            updated_after = datetime.datetime.now() - datetime.timedelta(days=updated_after_days)
            params['updatedAfter'] = updated_after
        print("Making export api request with params " + str(params) + "...")
        response = requests.get(
            url="https://readwise.io/api/v2/export/",
            params=params,
            headers={"Authorization": f"Token {token}"}, verify=False
        )
        response_json = response.json()
        full_data.extend(response.json()['results'])
        next_page_cursor = response.json().get('nextPageCursor')
        if not next_page_cursor:
            break
    return full_data

if __name__ == "__main__":
    highlights = fetch_highlights(readwise_token, 1)
    print(json.dumps(highlights[0], indent=4))
    for h in highlights:
        print(h["title"])