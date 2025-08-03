import csv

def save_results_to_csv(results, filename="results.csv"):
    if not results:
        return

    keys = ["title", "link", "snippet", "source", "category", "date"]

    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for result in results:
            writer.writerow({
                "title": result.get("title", ""),
                "link": result.get("link", ""),
                "snippet": result.get("snippet", ""),
                "source": result.get("source", ""),
                "category": result.get("category", ""),
                "date": result.get("date", ""),
            })
