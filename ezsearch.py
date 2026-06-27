
import sys
import os
import requests
import argparse


parser = argparse.ArgumentParser(
                    prog='ezsearch',
                    description='A way to send multiple search terms to BioPortal')

parser.add_argument('input_file', type=os.path.expanduser)
parser.add_argument('api_key', type=str)
parser.add_argument('-x', '--exact', action='store_true')
args = parser.parse_args()

# Check if the API key argument was provided
if len(sys.argv) < 3:
    print("Error: Missing API key and or list of query terms (#1, #2 respectively).")
    print("Usage: python script.py <YOUR_BIOPORTAL_API_KEY> <YOUR INPUT FILE WITH ONE SEARCH TERM PER LINE>")
    sys.exit(1)

# Retrieve API key from the first command-line argument
API_KEY = args.api_key

# Base configuration
BASE_URL = "https://data.bioontology.org/search"

# Parameters for the search
headers = {"Authorization": f"apikey token={API_KEY}"}

params_base = {
    #"q": "TGF-beta",  # Search term
    #"pagesize": 10,     # Limit results per page
    "require_exact_match": str(args.exact).lower()
}

query_file_name = args.input_file
query_file = open(query_file_name, "r", encoding="utf-8")
terms = query_file.read().splitlines()

for term in terms:
    params = { "q": term }
    params.update(params_base)

    # Execute GET request
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        for item in data.get("collection", []):
            #print(f"PrefLabel: {item.get('prefLabel')}")
            #print(f"Ontology:  {item.get('links', {}).get('ontology')}")
            #print(f"ID:        {item.get('@id')}\n")
            print(term, "\t", item.get('prefLabel'), "\t", item.get('@id'), "\t", item.get('ontology'), "\t", item.get('links').get('ontology'))
    else:
        print(f"Error: {response.status_code} - {response.text}")

query_file.close()
