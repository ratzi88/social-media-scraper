from flask import Flask, request, jsonify
from googlesearch import search  # type: ignore

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search_query():
    # Parse the JSON data from the request
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400

    search_query = data.get('name').strip()

    if not search_query:
        return jsonify({"error": "Search query cannot be empty"}), 400

    # Define the sites to search
    sites = ["site:facebook.com", "site:instagram.com", "site:x.com", "site:linkedin.com"]
    filtered_links = []

    try:
        # Perform search and filter results
        for site in sites:
            site_search_query = f"{site} {search_query}"
            results = list(search(site_search_query, tld="co.in", num=1, stop=1, pause=2))
            if results:
                filtered_links.append({"platform": site.split(':')[1], "link": results[0]})

        # Return the filtered links as a JSON response
        if filtered_links:
            return jsonify({"results": filtered_links}), 200
        else:
            return jsonify({"message": "No results found on specified platforms"}), 404

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
