import os
from urllib.parse import urlparse
from serpapi import GoogleSearch

def fetch_results_from_serpapi(query, max_results=100):
    api_key = os.getenv("SERPAPI_API_KEY") or os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SerpAPI key not found in environment variables.")

    all_results = []
    for start in range(0, max_results, 10):
        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "num": 10,
            "start": start,
            "hl": "en",
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        if "organic_results" not in results:
            break

        for result in results["organic_results"]:
            link = result.get("link", "")
            parsed_url = urlparse(link)
            domain = parsed_url.netloc.replace("www.", "") if parsed_url.netloc else "Unknown"

            # Categorize source by domain
            if "reddit.com" in domain:
                source = "Reddit"
            elif "youtube.com" in domain or "youtu.be" in domain:
                source = "YouTube"
            elif "twitter.com" in domain or "x.com" in domain:
                source = "Twitter"
            elif any(news_site in domain for news_site in ["cnn", "bbc", "nytimes", "indiatimes", "ndtv", "thehindu", "reuters"]):
                source = "News"
            elif any(blog in domain for blog in ["medium", "substack", "blogspot", "wordpress"]):
                source = "Blog"
            elif any(forum in domain for forum in ["quora", "stackexchange", "stack", "github", "producthunt"]):
                source = "Community"
            else:
                source = domain.title()

            result["source"] = source
            result["domain"] = domain
            all_results.append(result)

        # Optional: add a short delay to respect rate limits if needed
        # time.sleep(1)

    return all_results
