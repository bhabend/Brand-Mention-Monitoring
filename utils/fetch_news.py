import os
from serpapi.google_search_results import GoogleSearch

def fetch_google_news(keyword, serp_api_key, max_results=10):
    """Fetch Google News search results using SerpAPI."""
    params = {
        "engine": "google",
        "q": f"{keyword} site:news.google.com",
        "api_key": serp_api_key,
        "num": max_results,
        "tbm": "nws",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    news_results = results.get("news_results", [])
    cleaned_results = []

    for item in news_results:
        cleaned_results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "source": item.get("source"),
            "snippet": item.get("snippet"),
            "published": item.get("date") or item.get("published_date"),
        })

    return cleaned_results
