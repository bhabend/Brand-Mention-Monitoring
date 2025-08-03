import streamlit as st
from fetch_news import fetch_results_from_serpapi
from save_to_csv import save_results_to_csv

st.set_page_config(page_title="Brand Mention Monitoring", layout="wide")

st.title("🔍 Brand Mention Monitoring App")
keyword = st.text_input("Enter a brand or keyword:", placeholder="e.g., Tesla")

if st.button("Fetch Mentions"):
    if keyword:
        with st.spinner("Fetching data..."):
            results = fetch_results_from_serpapi(keyword)

        if results:
            st.success(f"Found {len(results)} mentions.")
            for r in results:
                st.markdown(f"### [{r['title']}]({r['link']})")
                st.markdown(f"**Source:** {r['source']} &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; **Category:** {r['category']}")
                st.markdown(f"{r['snippet']}")
                st.markdown("---")

            if st.download_button("📥 Download CSV", data=open("brand_mentions.csv", "rb"), file_name="brand_mentions.csv", mime="text/csv"):
                save_results_to_csv(results)
        else:
            st.warning("No results found. Check your query or SerpAPI quota.")
    else:
        st.error("Please enter a keyword.")
