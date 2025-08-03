import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_google_results(query, num_results=10):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY"),
        "engine": "google",
        "num": num_results,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get("organic_results", [])
        return [
            {
                "source": "Google",
                "title": r.get("title"),
                "link": r.get("link"),
                "snippet": r.get("snippet", ""),
            }
            for r in results
        ]
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch from SerpAPI: {e}")
        return []
