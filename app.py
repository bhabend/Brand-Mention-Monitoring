import os
import streamlit as st
import pandas as pd
from utils.fetch_news import fetch_google_news
from utils.sentiment import analyze_sentiment
from datetime import datetime

# Required for Render deployment
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_PORT'] = os.getenv('PORT', '10000')
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'

# Streamlit page setup
st.set_page_config(page_title="Brand Mention Monitor", layout="wide")
st.title("📣 Brand Mention Monitor")
st.markdown("Monitor your brand mentions with sentiment analysis from Google News.")

# Keyword input
keyword = st.text_input("Enter keyword or brand name", placeholder="e.g., OpenAI, Solana, Netflix")

# Button
if st.button("🔍 Fetch Mentions"):
    if not keyword.strip():
        st.warning("Please enter a keyword.")
    else:
        with st.spinner("Fetching mentions..."):
            data = fetch_google_news(keyword)
            if data.empty:
                st.warning("No mentions found.")
            else:
                data["sentiment"] = data["snippet"].apply(analyze_sentiment)

                # Display sentiment breakdown
                sentiment_counts = data["sentiment"].value_counts().reset_index()
                sentiment_counts.columns = ["Sentiment", "Count"]
                st.subheader("📊 Sentiment Breakdown")
                st.bar_chart(sentiment_counts.set_index("Sentiment"))

                # Show full data
                st.subheader("🗞️ Mentions")
                st.dataframe(data[["title", "link", "snippet", "source", "date", "sentiment"]])

                # CSV download
                st.subheader("⬇️ Download Mentions as CSV")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv = data.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{keyword}_mentions_{timestamp}.csv",
                    mime="text/csv",
                )
