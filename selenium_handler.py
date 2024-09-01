from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio

async def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    return webdriver.Chrome(options=chrome_options)

async def fetch_template_urls(driver, main_url):
    print(f"Navigating to main URL: {main_url}")
    await asyncio.to_thread(driver.get, main_url)
    print("Waiting for page to load...")
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='card-footer-title']")))
    except Exception as e:
        print(f"Error waiting for page load: {str(e)}")
        print("Attempting to find elements anyway...")

    print("Finding all template links...")
    template_links = set()  # Use a set to avoid duplicates
    
    # Scroll to load all content
    last_height = await asyncio.to_thread(driver.execute_script, "return document.body.scrollHeight")
    while True:
        await asyncio.to_thread(driver.execute_script, "window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(2)  # Wait for page to load
        new_height = await asyncio.to_thread(driver.execute_script, "return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find links using multiple selectors
    selectors = [
        "[data-testid='card-footer-title']",
        "a[href*='/miroverse/']",
        ".BaseCardstyles__FullAreaLink-sc-17x4iqf-0"
    ]

    for selector in selectors:
        elements = await asyncio.to_thread(driver.find_elements, By.CSS_SELECTOR, selector)
        for element in elements:
            try:
                if element.tag_name == 'a':
                    href = await asyncio.to_thread(element.get_attribute, "href")
                else:
                    parent_a = await asyncio.to_thread(element.find_element, By.XPATH, "./ancestor::a")
                    href = await asyncio.to_thread(parent_a.get_attribute, "href")
                if href and '/miroverse/' in href and not href.endswith('/miroverse/') and 'profile' not in href:
                    template_links.add(href)
            except Exception as e:
                print(f"Error finding link for element: {str(e)}")

    template_urls = list(template_links)
    print(f"Found {len(template_urls)} unique template URLs")
    for url in template_urls:
        print(url)
    return template_urls