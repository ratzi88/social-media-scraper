from flask import Flask, request, jsonify
from flask_cors import CORS  # To allow cross-origin requests from React frontend
from pymongo import MongoClient  # For MongoDB integration
from bson import json_util
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# MongoDB Configuration
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
client = MongoClient(mongo_uri)
db = client.social_media
collection = db.results

def google_search(query, num_results=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = []
    for g in soup.find_all("div", class_="tF2Cxc"):
        title = g.find("h3").text
        link = g.find("a")["href"]
        search_results.append({"title": title, "link": link})
    
    return search_results

@app.route('/search', methods=['GET','POST'])
def search_query():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400

    search_query = data.get('name').strip().lower()

    if not search_query:
        return jsonify({"error": "Search query cannot be empty"}), 400
    
    existing_record = collection.find_one({"query": search_query})

    if existing_record:
        return jsonify(existing_record["results"]), 200

    sites = ["site:facebook.com", "site:instagram.com", "site:x.com", "site:linkedin.com"]
    filtered_links = {}

    try:
        for site in sites:
            site_search_query = f"{site} {search_query}"
            results = google_search(site_search_query, num_results=1)
            if results:
                platform = site.split(':')[1].replace(".com", "")  # Extract platform name
                filtered_links[platform] = results[0]["link"]

        # Add default None values for platforms with no results
        for platform in ["facebook", "instagram", "x", "linkedin"]:
            if platform not in filtered_links:
                filtered_links[platform] = None

        document = {"query": search_query, "results": filtered_links}
        collection.insert_one(document)

        return jsonify(filtered_links), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
