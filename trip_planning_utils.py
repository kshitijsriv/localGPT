import json
import os
import re
import pandas as pd
from fuzzywuzzy import process
import requests
from dotenv import load_dotenv


load_dotenv(".env")
DIRECTIONS_BASE_URL = os.getenv("DIRECTIONS_BASE_URL")
print(DIRECTIONS_BASE_URL)
stops = pd.read_csv("./stops.txt")


def find_stop_coordinates(stop_name_to_find, score_threshold=80):
    # Perform fuzzy matching to get a list of matches and their scores
    matches = process.extract(stop_name_to_find, stops['stop_name'])

    # Filter to find the best match above the score threshold
    best_match = next((match for match, score, _ in matches if score >= score_threshold), None)

    if best_match:
        # Find the stop in the DataFrame
        matching_stop = stops[stops['stop_name'] == best_match].iloc[0]
        return matching_stop['stop_lat'], matching_stop['stop_lon']
    else:
        return None, None


def extract_src_dest(json_string):
    json_string_match = re.search(r'{.*?}', json_string, re.DOTALL)
    if json_string_match:
        json_string = json_string_match.group()
        # Parsing the JSON string
        data = json.loads(json_string)
        src = data.get("src")
        dest = data.get("dest")
    else:
        src, dest = None, None
    return src, dest


def get_directions(src, dest):
    url = f"{DIRECTIONS_BASE_URL}?src=%5B{src[0]},%20{src[1]}%5D&dest=%5B{dest[0]},%20{dest[1]}%5D&src_type=place&dest_type=place"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response


if __name__ == '__main__':
    print(find_stop_coordinates(stop_name_to_find="govindpuri"))
    print(find_stop_coordinates(stop_name_to_find="Rajiv chowk"))
