# fetch_news.py

import requests
from urllib.parse import urlparse
from utils.sentiment import analyze_sentiment

def fetch_google_results(query, serpapi_key):
    search_url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": serpapi_key,
        "num": 100,
        "hl": "en",
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    results = []
    organic_results = data.get("organic_results", [])

    for result in organic_results:
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")

        # Dynamically extract source from link
        parsed_url = urlparse(link)
        domain = parsed_url.netloc.replace("www.", "")

        results.append({
            "source": domain,
            "title": title,
            "link": link,
            "snippet": snippet,
            "sentiment": analyze_sentiment(f"{title} {snippet}"),
        })

    return results
