import streamlit as st
import serpapi
import os
import time

# --- APP SETUP ---
st.set_page_config(
    page_title="Brand Mention Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Brand Mention Monitor")
st.markdown("Enter a brand name to find its latest mentions in the news.")

# --- API KEY MANAGEMENT ---
# This code assumes the SerpAPI key is stored as a secret, which is the
# recommended way for deployment platforms like Render and Streamlit Cloud.
#
# For local development, create a .streamlit/secrets.toml file with:
# [serpapi]
# api_key="YOUR_SERPAPI_KEY"
try:
    API_KEY = st.secrets["serpapi"]["api_key"]
except (KeyError, FileNotFoundError):
    st.error("SerpAPI key not found. Please add it to your Streamlit secrets or Render environment variables.")
    st.info("For more information on secrets, see the links below.")
    st.markdown("1. Streamlit Secrets: https://docs.streamlit.io/deploy/streamlit-cloud/secrets-management")
    st.markdown("2. Render Environment Variables: https://render.com/docs/environment-variables")
    st.stop()


# --- SEARCH FUNCTIONALITY ---
@st.cache_data(show_spinner=False)
def search_brand_mentions(brand_name, serpapi_key):
    """
    Searches for news mentions of a given brand using SerpAPI.
    The search is cached to avoid repeated API calls for the same query.
    """
    if not brand_name:
        return None

    try:
        # Use the modern serpapi.Client class
        client = serpapi.Client(api_key=serpapi_key)
        params = {
            "engine": "google_news",
            "q": brand_name,
            "tbs": "qdr:w",  # Restrict results to the past week
            "num": 20,       # Number of results to fetch
        }
        
        st.info(f"Searching for news mentions of '{brand_name}'...")
        
        start_time = time.time()
        results = client.search(params=params)
        end_time = time.time()
        
        st.success(f"Search completed in {end_time - start_time:.2f} seconds.")
        return results

    except serpapi.SerpApiError as e:
        st.error(f"Error from SerpAPI: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None


# --- USER INTERFACE ---
with st.sidebar:
    st.header("Search Settings")
    brand_name_input = st.text_input("Enter a brand name to monitor:", "Google")
    search_button = st.button("Monitor Brand Mentions")
    st.markdown("---")
    st.markdown("### Deployment Information")
    st.markdown("To deploy this app on Render, make sure you have:")
    st.markdown("1.  This `app.py` file.")
    st.markdown("2.  A `requirements.txt` file listing dependencies.")
    st.markdown("3.  A `Procfile` with the start command.")
    st.markdown("4.  A `PYTHON_VERSION` environment variable set to `3.11.8`.")
    st.markdown("5.  Your SerpAPI key as an environment variable.")


if search_button:
    if brand_name_input:
        with st.spinner("Fetching news articles..."):
            search_results = search_brand_mentions(brand_name_input, API_KEY)

        if search_results and "news_results" in search_results:
            news_articles = search_results["news_results"]
            if news_articles:
                st.subheader(f"Latest News Mentions for '{brand_name_input}'")
                for article in news_articles:
                    with st.container(border=True):
                        st.markdown(f"**[{article.get('title', 'No Title')}]({article.get('link', '#')})**")
                        st.markdown(f"**Source:** {article.get('source', 'N/A')} | **Date:** {article.get('date', 'N/A')}")
                        st.markdown(article.get('snippet', 'No snippet available.'))
            else:
                st.warning(f"No news mentions found for '{brand_name_input}' in the last week.")
        else:
            st.error("Failed to retrieve news results. Please check your API key and try again.")
    else:
        st.warning("Please enter a brand name to begin the search.")

