import streamlit as st
import pandas as pd
from utils.fetch_news import fetch_results_from_serpapi
from utils.save_to_csv import save_results_to_csv

st.set_page_config(page_title="Brand Mention Monitoring", layout="wide")

st.title("🔍 Brand Mention Monitoring App")
st.markdown("Enter a **brand name** or keyword to track recent mentions from news, blogs, videos, and community posts.")

keyword = st.text_input("Enter brand or keyword:", placeholder="e.g., Tesla")

if st.button("Fetch Mentions"):
    if not keyword.strip():
        st.warning("Please enter a keyword.")
    else:
        with st.spinner("Fetching mentions..."):
            results = fetch_results_from_serpapi(keyword)
            if results:
                df = pd.DataFrame(results)
                save_results_to_csv(df)
                st.success(f"Found {len(results)} mentions.")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"{keyword}_mentions.csv",
                    mime="text/csv",
                )
            else:
                st.error("No results found. Check your query or SerpAPI quota.")
