import streamlit as st
from utils.fetch_news import fetch_google_results
from utils.sentiment import analyze_sentiment
from utils.save_to_csv import save_results_to_csv

st.set_page_config(page_title="Brand Mention Monitor", layout="wide")

st.title("🔍 Brand Mention Monitoring Tool")

query = st.text_input("Enter brand or keyword to search", "")

limit = st.slider("How many mentions to fetch?", min_value=10, max_value=50, value=30, step=10)

if st.button("Fetch Mentions") and query.strip():
    st.info(f"Fetching up to {limit} Google results for: `{query}`...")
    results = fetch_google_results(query, total_results=limit)

    if not results:
        st.warning("⚠️ No results found. Check your query or SerpAPI quota.")
        st.stop()

    # Add sentiment analysis
    for r in results:
        combined_text = f"{r['title']} {r['snippet']}"
        r["sentiment"] = analyze_sentiment(combined_text)

    st.success(f"✅ Found {len(results)} results.")
    st.dataframe(results)

    # Save and allow download
    csv_file = save_results_to_csv(results, query)
    if csv_file:
        with open(csv_file, "rb") as f:
            st.download_button("📥 Download CSV", f, file_name=csv_file.split("/")[-1])
