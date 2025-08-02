import pandas as pd
from datetime import datetime
import os

def save_results_to_csv(data: list[dict], keyword: str) -> str:
    """
    Save list of mention data to a CSV file and return the filepath.
    Each dict in `data` should contain fields like source, title, url, snippet, published_time, sentiment.
    """
    df = pd.DataFrame(data)

    # Ensure output folder exists
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{keyword}_mentions_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)

    df.to_csv(filepath, index=False)
    return filepath
