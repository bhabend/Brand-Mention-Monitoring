import os
from dotenv import load_dotenv
from serpapi import serpapi_search  # Not GoogleSearch for v0.1.5

load_dotenv()

def fetch_google_news(keyword, limit=10):
    params = {
        "engine": "google",
        "q": keyword,
        "tbm": "nws",
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num": limit,
    }

    results = serpapi_search(params)
    news_results = results.get("news_results", [])
    articles = [
        {
            "title": article.get("title"),
            "link": article.get("link"),
            "snippet": article.get("snippet"),
            "source": article.get("source"),
            "date": article.get("date"),
        }
        for article in news_results
    ]
    return articles
