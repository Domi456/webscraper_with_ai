#3rd party imports
import streamlit as st
import signal
import time
#inner imports
from scrape import scrape_site, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama, stop_ollama

st.markdown(
    """
    <style>
        #webscraper-robot {
            font-family: 'Courier', sans-serif;
            color: #1f1f1f;
        }
        p, textarea, #text_input_1{
            font-family: 'Courier', sans-serif;
            color: #1f1f1f;
            font-size: 17px
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Webscraper robot")
url = st.text_input("Enter a website URL: ")

if 'running' not in st.session_state:
    st.session_state.running = True

if 'scraping' not in st.session_state:
    st.session_state.scraping = False

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

    if 'dom_content' not in st.session_state:
        st.session_state.dom_content = ""


    st.text_area(
        "DOM Content",
        value=st.session_state.dom_content,
        key="dom_content_textarea",
        height=400,
        position="fixed",
    )

    if 'dom_content_textarea' in st.session_state:
        st.session_state.dom_content = st.session_state.dom_content_textarea

    print(result)
    st.session_state.scraping = False
    progress_bar.progress(100)
    time.sleep(0.5)
    progress_bar.empty()
    status_message.empty()

#print("DOM content: ", st.session_state.dom_content)
parse_description = st.text_area("Describe what you want to parse: ")

if 'running' not in st.session_state:
    st.session_state.running = True
if 'processing' not in st.session_state:
    st.session_state.processing = False

def start_processing():
    st.session_state.running = False
    st.session_state.processing = True
    #print("DOM content start processing: ", st.session_state.dom_content)

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
