import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from utils.fetch_data import fetch_mentions
from utils.sentiment import analyze_sentiment

load_dotenv()

st.set_page_config(page_title="Brand Mention Monitor", layout="wide")
st.title("🔎 Brand Mention Monitoring Dashboard")

keyword = st.text_input("Enter Brand Name or Keyword(s):", placeholder="e.g. OpenAI, Bitcoin, Nike")

if st.button("Fetch Mentions") and keyword:
    with st.spinner("Fetching data from platforms..."):
        raw_data = fetch_mentions(keyword)
        df = pd.DataFrame(raw_data)

        if df.empty:
            st.warning("No mentions found.")
        else:
            df["sentiment"] = df["text"].apply(analyze_sentiment)

            st.subheader("📊 Sentiment Overview")
            sentiment_count = df["sentiment"].value_counts()
            st.bar_chart(sentiment_count)

            st.subheader("🗂️ Mentions")
            st.dataframe(df[["platform", "title", "text", "url", "timestamp", "sentiment"]])

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", data=csv, file_name="mentions.csv", mime="text/csv")
else:
    st.info("Enter a keyword and click 'Fetch Mentions' to begin.")
