import pandas as pd
from datetime import datetime
import os

def save_results_to_csv(data, query):
    if not data:
        return None
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{query.replace(' ', '_')}_results_{timestamp}.csv"
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    return filepath
