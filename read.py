import json
import os
from dotenv import load_dotenv
import datetime
import requests


load_dotenv()
readwise_token = os.getenv('READWISE_TOKEN')

#### Helpers

gap = '\n-------------------\n'+'-------------------\n'

def formatted_print(input_json):
    print(gap)
    print(json.dumps(input_json, indent=4))
    print(gap)

def write_to_file(file_name, data):
    # Use the json.dump method to write the JSON object to a file
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file)


####
def fetch_highlights(updated_after_days=None, token=readwise_token):
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

def extract_highlights(highlights):
    aggregated_highlights = []
    for book in highlights:
        print(book['title'])
        for h in book['highlights']:
            h['title'] = book['title']
            h['author'] = book['author']
            h['book_unique_url'] = book['unique_url']
            h['book_readwise_url'] = book['readwise_url']
            aggregated_highlights.append(h)
    return aggregated_highlights

if __name__ == "__main__":
    highlights = fetch_highlights(1)
    formatted_print(extract_highlights(highlights))