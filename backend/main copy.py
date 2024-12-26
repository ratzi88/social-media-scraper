from flask import Flask, request, jsonify
from googlesearch import search  # type: ignore
from flask_cors import CORS  # To allow cross-origin requests from React frontend
from pymongo import MongoClient # type: ignore
from bson import json_util # type: ignore
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mongo db Configuration
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
client = MongoClient(mongo_uri)
db = client.social_media
collection = db.results

@app.route('/search', methods=['POST'])
def search_query():
    # Parse the JSON data from the request
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400

    search_query = data.get('name').strip().lower()

    if not search_query:
        return jsonify({"error": "Search query cannot be empty"}), 400
    
    existing_record = collection.find_one({"query": search_query})

    if existing_record:
        return jsonify(existing_record["results"]), 200

    # Define the sites to search
    sites = ["site:facebook.com", "site:instagram.com", "site:x.com", "site:linkedin.com"]
    filtered_links = []

    try:
        # Perform search and filter results
        for site in sites:
            site_search_query = f"{site} {search_query}"
            results = list(search(site_search_query, tld="co.in", num=1, stop=1, pause=2))
            if results:
                # Extract site name and link
                platform = site.split(':')[1].replace(".com", "")  # Ensure platform names are unique
                filtered_links.append((platform, results[0]))


        # Transform filtered_links into a dictionary with default values
        results_dict = {platform: link for platform, link in filtered_links}
        for platform in ["facebook", "instagram", "x", "linkedin"]:
            if platform not in results_dict:
                results_dict[platform] = None


        document = {"query": search_query, "results": results_dict}
        print(f"Inserting document into MongoDB: {document}")
        collection.insert_one(document)

        return jsonify(results_dict), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)