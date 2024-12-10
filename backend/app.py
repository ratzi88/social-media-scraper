import requests as re
import os

# change working dir to python running dir
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# trying to open api key and serch engine id
try:
    with open('API_KEY', 'r') as f:
        API_KEY = f.read().strip()
    with open('SEARCH_ENGINE_ID', 'r') as f:
        SEARCH_ENGINE_ID = f.read().strip()
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Ensure 'API_KEY' and 'SEARCH_ENGINE_ID' files exist in the script directory.")
    exit()


if not API_KEY or not SEARCH_ENGINE_ID:
    print("Error: API_KEY or SEARCH_ENGINE_ID is empty.")
    exit()

# ask the user what to search    
search_query=input('What do you want to search? ').strip()

# define the API endpoint and parameters
url= 'https://www.googleapis.com/customsearch/v1'
params = {
    'q': search_query,
    'key': API_KEY,
    'cx': SEARCH_ENGINE_ID
}

filtered_links=[]

# API request
response = re.get(url, params=params)
results= response.json()
if 'items' in results:
    print("\nSearch Results:")
    for item in results['items']:
        if ('linkedin.com' in item['link'] or 
        'x.com' in item['link'] or 
        'instagram.com' in item['link'] or 
        'facebook.com' in item['link']):
            filtered_links.append(item['link'])
else:
    print('No result found')

print(filtered_links)