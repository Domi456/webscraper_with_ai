import streamlit as st
from scrape import scrape_site, split_dom_content, clean_body_content, extract_body_content

st.title("Web scraper with AI")
url = st.text_input("Enter a website URL: ")

if st.button("Scrape site"):
    st.write("Scraping the website")

    result = scrape_site(url)
    body_content = extract_body_content(result)
    clean_content = clean_body_content(body_content)

    st.session_state.dom_content = clean_content

    with st.expander("View DOM content"):
        st.text_area("DOM Content", clean_content, height=400)

    print(result)
