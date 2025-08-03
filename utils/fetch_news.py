import os
from serpapi import GoogleSearch
from urllib.parse import urlparse

CATEGORY_MAP = {
    "reddit.com": "Community",
    "quora.com": "Community",
    "stackexchange.com": "Community",
    "stackoverflow.com": "Community",
    "youtube.com": "Video",
    "medium.com": "Blog",
    "wordpress.com": "Blog",
    "blogspot.com": "Blog",
    "forbes.com": "News",
    "cnn.com": "News",
    "nytimes.com": "News",
    "bbc.com": "News",
    "theguardian.com": "News",
    "techcrunch.com": "News"
}

def get_category(url):
    domain = urlparse(url).netloc.replace("www.", "")
    for known_domain in CATEGORY_MAP:
        if known_domain in domain:
            return CATEGORY_MAP[known_domain]
    return "Other"

def fetch_results_from_serpapi(query, num_results=20):
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    organic_results = results.get("organic_results", [])
    filtered_results = []

    for result in organic_results:
        link = result.get("link")
        title = result.get("title")
        snippet = result.get("snippet", "")
        if link and title:
            filtered_results.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "source": urlparse(link).netloc.replace("www.", ""),
                "category": get_category(link)
            })

    return filtered_results
