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

if 'scraping' not in st.session_state:
    st.session_state.scraping = True

def start_scraping():
    st.session_state.scraping = True

st.button("Scrape site", disabled=not st.session_state.running, on_click=start_scraping)

if st.session_state.scraping:
    status_message = st.empty()
    progress_bar = st.progress(0)

    status_message.write("Scraping the website..")
    
    for i in range(1, 101, 10):
        time.sleep(0.3)
        progress_bar.progress(i)

    result = scrape_site(url)
    body_content = extract_body_content(result)
    clean_content = clean_body_content(body_content)

    st.session_state.dom_content = clean_content

    with st.expander("View DOM content"):
        st.text_area("DOM Content", clean_content, height=400)

    print(result)
    st.session_state.scraping = False
    progress_bar.progress(100)
    time.sleep(0.5)
    progress_bar.empty()
    status_message.empty()

parse_description = st.text_area("Describe what you want to parse: ")

if 'running' not in st.session_state:
    st.session_state.running = True
if 'processing' not in st.session_state:
    st.session_state.processing = False

def start_processing():
    st.session_state.running = False
    st.session_state.processing = True

def cancel_processing():
    st.session_state.running = True
    st.session_state.processing = False
    stop_ollama("ollama.exe")

st.button("Ask AI", disabled=not st.session_state.running, on_click=start_processing)

if st.session_state.processing:
    status_message = st.empty()
    progress_bar = st.progress(0)

    status_message.write("🤖 **AI is thinking...**")
    
    for i in range(1, 101, 10):
        time.sleep(0.3)
        progress_bar.progress(i)


    # "Cancel query" gomb csak akkor jelenik meg, ha processing = True
    st.button("Cancel query", on_click=cancel_processing)
    dom_chunks = split_dom_content(st.session_state.dom_content)
    result = parse_with_ollama(dom_chunks=dom_chunks, parse_description=parse_description)
    st.session_state.processing = False
    st.session_state.running = True
    st.write(result)
    stop_ollama("ollama.exe")
    progress_bar.progress(100)
    time.sleep(0.5)
    progress_bar.empty()
    status_message.empty()
