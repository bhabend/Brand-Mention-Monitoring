import os
from serpapi import GoogleSearch
from urllib.parse import urlparse

def fetch_results_from_serpapi(query, num_pages=3):
    api_key = os.getenv("SERPAPI_API_KEY") or os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SerpAPI key not set in environment")

    all_results = []

    for page in range(num_pages):
        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "start": page * 10,
            "num": 10,
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        if "error" in results:
            print("SerpAPI Error:", results["error"])
            break

        organic_results = results.get("organic_results", [])
        for item in organic_results:
            title = item.get("title", "")
            link = item.get("link", "")
            snippet = item.get("snippet", "")
            date = item.get("date", "")
            source_url = urlparse(link).netloc

            # Categorize based on domain
            if "reddit.com" in source_url:
                category = "Community"
            elif "youtube.com" in source_url:
                category = "Video"
            elif any(site in source_url for site in ["forbes", "bloomberg", "cnn", "bbc", "reuters"]):
                category = "News"
            elif any(site in source_url for site in ["medium", "substack", "blog", "wordpress"]):
                category = "Blog"
            else:
                category = "Other"

            all_results.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "source": source_url,
                "category": category,
                "date": date,
            })

    return all_results
