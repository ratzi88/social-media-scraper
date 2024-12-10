try:
    from googlesearch import search # type: ignore
except ImportError:
    print("No module named 'google' found")
    exit()

# Prompt user for search query
search_query = input("What do you want to search? ").strip()

if not search_query:
    print("Search query cannot be empty.")
    exit()
    
site_search_query=""
filtered_links = []
sites=["site:facebook.com","site:instagram.com","site:x.com","site:linkedin.com"]
# Perform search and filter results
try:
    print("Searching, please wait...")
    for site in sites:
        site_search_query= site + " " + search_query
        print(f"\n{site[5:]} Links:")
        j=list(search(site_search_query, tld="co.in", num=1, stop=1, pause=5))
        if (j):
            j=''.join(j)
            print(j)
            filtered_links.append(j)
        else:
            print("Links to site was not found")

# Display results
    if filtered_links:
        print("\nFiltered Links:")
        for idx, link in enumerate(filtered_links, start=1):
            print(f"{idx}. {link}")
    else:
        print("No results found on specified platforms.")
except Exception as e:
    print(f"An error occurred: {e}")
