# utils/fetch_news.py

import requests
from serpapi import GoogleSearch

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

    articles = []
    for result in results.get("news_results", []):
        articles.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet"),
            "source": result.get("source"),
            "date": result.get("date"),
        })

    return articles
