#3rd party imports
import streamlit as st
import signal
import time
#inner imports
from scrape import scrape_site, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama, stop_ollama

# def timeout_handler(singum, frame):
#     raise TimeoutError("Ollama repsonse took too long. Cancelling...")

# signal.signal(signal.SIGALRM, timeout_handler)
# signal.alarm(180) # 3 perc után cancel


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


parse_description = st.text_area("Describe what you want to parse: ")
     


if st.button("Send to Deepseek", icon="🔥"):
    if parse_description:
        st.write("🤖 **Deepseek-r1 is thinking...**")
        if st.button("Cancel query", icon="❌"):
            st.write("Cancelling...")
            stop_ollama()
        else:
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks=dom_chunks, parse_description=parse_description)
            st.write(result)
