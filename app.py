import streamlit as st
from utils.fetch_news import fetch_google_news
from utils.sentiment import analyze_sentiment
from utils.save_to_csv import save_results_to_csv

st.set_page_config(page_title="Brand Mention Monitor", layout="wide")

st.title("🛡️ Brand Mention Monitor")
st.markdown("Monitor your brand or keywords across news sources with sentiment classification.")

with st.form("mention_form"):
    query = st.text_input("🔍 Enter a keyword to monitor")
    submitted = st.form_submit_button("Track Mentions")

if submitted and query:
    st.info("Fetching results...")

    try:
        results = fetch_google_news(query)

        if not results:
            st.warning("No results found.")
        else:
            # Add sentiment
            for result in results:
                result["sentiment"] = analyze_sentiment(result["title"] + " " + result["snippet"])

            # Show data
            st.success(f"Found {len(results)} results.")
            st.dataframe(results)

            # Offer CSV download
            csv = save_results_to_csv(results)
            st.download_button("📥 Download Results as CSV", csv, file_name="brand_mentions.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
