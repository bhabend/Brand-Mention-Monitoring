import streamlit as st
import pandas as pd
from utils.fetch_news import fetch_results_from_serpapi
from utils.save_to_csv import save_results_to_csv

st.set_page_config(page_title="Brand Mention Monitoring", layout="wide")

st.title("🔍 Brand Mention Monitoring Tool")

keyword = st.text_input("Enter brand or keyword to monitor:", value="Tesla")

if st.button("Fetch Mentions"):
    if keyword:
        with st.spinner("Fetching data..."):
            results = fetch_results_from_serpapi(keyword)
            if results:
                df = pd.DataFrame(results)
                st.success(f"Found {len(df)} mentions for '{keyword}'")
                st.dataframe(df)

                # Save CSV
                save_results_to_csv(results)
                with open("results.csv", "rb") as f:
                    st.download_button("Download CSV", f, file_name="results.csv")
            else:
                st.warning("No results found. Check your query or SerpAPI quota.")
    else:
        st.error("Please enter a keyword.")
