import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_google_results(query, num_results=10):
    url = "https://serpapi.com/search.json"
    api_key = os.getenv("SERPAPI_KEY")
    
    print("DEBUG: Query =", query)
    print("DEBUG: API Key present? =", bool(api_key))

    if not api_key:
        print("[ERROR] SERPAPI_KEY not found")
        return []

    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": num_results,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        print("DEBUG: Response status =", response.status_code)
        data = response.json()
        print("DEBUG: Full response =", data)

        results = data.get("organic_results", [])
        print(f"DEBUG: Found {len(results)} results.")
        
        return [
            {
                "source": "Google",
                "title": r.get("title"),
                "link": r.get("link"),
                "snippet": r.get("snippet", ""),
            }
            for r in results
        ]
    except Exception as e:
        print(f"[ERROR] SerpAPI request failed: {e}")
        return []
