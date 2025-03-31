import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def scrape_site(webURL):
    print("Launching webpage in background..")

    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\\Users\\domie\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")  # Helps with some rendering issues
    options.add_argument("--no-sandbox")  # Avoids some permission issues
    options.add_argument("--disable-dev-shm-usage")  # Helps with resource management

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(webURL)
        print("Page loaded..")
        html = driver.page_source
        #time.sleep()
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    if body:
        return str(body)
    return ""

def clean_body_content(body):
    soup = BeautifulSoup(body, "html.parser")

    for scriptORstyle in soup(["script", "style"]):
        scriptORstyle.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content(dom_content, max_length = 6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
