import streamlit as st
from utils.fetch_news import fetch_google_results
from utils.sentiment import analyze_sentiment
from utils.save_to_csv import save_results_to_csv

st.set_page_config(page_title="Brand Mention Monitor", layout="wide")

st.title("🔍 Brand Mention Monitoring Tool")

query = st.text_input("Enter brand or keyword to search", "")

if st.button("Fetch Mentions") and query.strip():
    st.info(f"Fetching Google results for: `{query}`...")
    results = fetch_google_results(query)
    
    if not results:
        st.warning("No results found.")
    else:
        for r in results:
            r["sentiment"] = analyze_sentiment(r["title"] + " " + r["snippet"])

        st.success(f"Found {len(results)} results.")
        st.dataframe(results)

        csv_file = save_results_to_csv(results, query)
        if csv_file:
            with open(csv_file, "rb") as f:
                st.download_button("Download CSV", f, file_name=csv_file.split("/")[-1])
