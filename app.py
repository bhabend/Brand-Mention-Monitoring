import streamlit as st

st.set_page_config(page_title="Brand Mention Monitor", layout="wide")

st.title("🛡️ Brand Mention Monitor")
st.markdown("This is a test to confirm Streamlit UI is working.")

query = st.text_input("Enter a keyword to monitor")

if query:
    st.success(f"You entered: {query}")
