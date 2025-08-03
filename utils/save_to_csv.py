import csv
import os

def save_results_to_csv(results, query):
    safe_query = query.replace(" ", "_").lower()
    filename = f"/mnt/data/{safe_query}_brand_mentions.csv"

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["source", "title", "link", "snippet", "sentiment"])
            writer.writeheader()
            writer.writerows(results)
        return filename
    except Exception as e:
        print(f"[ERROR] Failed to save CSV: {e}")
        return None
