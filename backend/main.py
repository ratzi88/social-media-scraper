try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")
    exit()

# Prompt user for search query
search_query = input("What do you want to search? ").strip()

if not search_query:
    print("Search query cannot be empty.")
    exit()

filtered_links = []

# Perform search and filter results
try:
    print("Searching, please wait...")
    for j in search(search_query, tld="co.in", num=30, stop=30, pause=3):
        if 'linkedin.com' in j or 'x.com' in j or 'instagram.com' in j or 'facebook.com' in j:
            filtered_links.append(j)

# Display results
    if filtered_links:
        print("\nFiltered Links:")
        for idx, link in enumerate(filtered_links, start=1):
            print(f"{idx}. {link}")
    else:
        print("No results found on specified platforms.")
except Exception as e:
    print(f"An error occurred: {e}")
