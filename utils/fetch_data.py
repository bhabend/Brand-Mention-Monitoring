import os
import requests
from datetime import datetime

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def fetch_mentions(keyword):
    results = []

    platforms = [
        {"engine": "google_news"},
        {"engine": "youtube"},
        {"engine": "reddit"}
    ]

    for platform in platforms:
        params = {
            "engine": platform["engine"],
            "q": keyword,
            "api_key": SERPAPI_KEY,
            "num": 10
        }
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code == 200:
            data = response.json()
            if platform["engine"] == "google_news":
                for item in data.get("news_results", []):
                    results.append({
                        "platform": "Google News",
                        "title": item.get("title"),
                        "text": item.get("snippet"),
                        "url": item.get("link"),
                        "timestamp": item.get("date", datetime.now().isoformat())
                    })
            elif platform["engine"] == "youtube":
                for item in data.get("video_results", []):
                    results.append({
                        "platform": "YouTube",
                        "title": item.get("title"),
                        "text": item.get("description"),
                        "url": item.get("link"),
                        "timestamp": datetime.now().isoformat()
                    })
            elif platform["engine"] == "reddit":
                for item in data.get("organic_results", []):
                    results.append({
                        "platform": "Reddit",
                        "title": item.get("title"),
                        "text": item.get("snippet"),
                        "url": item.get("link"),
                        "timestamp": datetime.now().isoformat()
                    })
        else:
            print(f"Error fetching from {platform['engine']}: {response.status_code}")
    return results
