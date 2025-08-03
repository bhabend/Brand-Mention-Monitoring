import csv

def save_results_to_csv(results, filename="brand_mentions.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Snippet", "Source", "Category"])

        for result in results:
            writer.writerow([
                result.get("title", ""),
                result.get("link", ""),
                result.get("snippet", ""),
                result.get("source", ""),
                result.get("category", "")
            ])
