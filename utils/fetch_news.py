import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_google_results(query, total_results=50):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("[ERROR] SERPAPI_KEY not found")
        return []

    all_results = []
    start = 0

    while len(all_results) < total_results:
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "num": 10,       # Max allowed per page
            "start": start   # Pagination offset
        }

        try:
            response = requests.get("https://serpapi.com/search.json", params=params, timeout=10)
            response.raise_for_status()
            organic = response.json().get("organic_results", [])
            print(f"Fetched {len(organic)} results at start={start}")

            if not organic:
                break  # No more results

            for r in organic:
                all_results.append({
                    "source": "Google",
                    "title": r.get("title"),
                    "link": r.get("link"),
                    "snippet": r.get("snippet", ""),
                })

            start += 10

        except Exception as e:
            print(f"[ERROR] SerpAPI request failed: {e}")
            break

    return all_results[:total_results]
