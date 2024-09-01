import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """
    Set up and return a Selenium WebDriver for Chrome.
    
    :return: Configured WebDriver instance
    """
    service = Service('path/to/chromedriver')  # Update this path
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    return webdriver.Chrome(service=service, options=options)

def scrape_template_list(url, driver):
    """
    Scrape the Miro template list page using Selenium.
    
    :param url: URL of the Miro templates page
    :param driver: Selenium WebDriver instance
    :return: List of tuples containing template names and their URLs
    """
    driver.get(url)
    
    # Wait for the template cards to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='template-card']"))
    )
    
    templates = []
    template_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='template-card']")
    
    for card in template_cards:
        link = card.find_element(By.TAG_NAME, 'a')
        template_url = link.get_attribute('href')
        template_name = card.find_element(By.CSS_SELECTOR, "h3[data-testid='template-card-title']").text
        templates.append((template_name, template_url))
    
    return templates

def scrape_template_details(template_url, driver):
    """
    Scrape details from an individual Miro template page using Selenium.
    
    :param template_url: URL of the specific template page
    :param driver: Selenium WebDriver instance
    :return: Dictionary containing template title, description, and URL
    """
    driver.get(template_url)
    
    # Wait for the title to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1[data-testid='template-name']"))
    )
    
    title = driver.find_element(By.CSS_SELECTOR, "h1[data-testid='template-name']").text
    
    # The description might be in a different location, adjust as needed
    description_elem = driver.find_element(By.CSS_SELECTOR, "div[data-testid='template-description']")
    description = description_elem.text if description_elem else 'No description'

    return {
        'title': title,
        'description': description,
        'url': template_url
    }

def scrape_templates(start_url):
    """
    Main scraping function that coordinates the scraping process.
    
    :param start_url: URL of the Miro templates page
    :return: List of dictionaries containing scraped template data
    """
    driver = setup_driver()
    try:
        # First, get the list of all templates
        templates = scrape_template_list(start_url, driver)
        data = []

        # Then, scrape details for each individual template
        for template_name, template_url in templates:
            print(f"Scraping template: {template_name}")
            template_data = scrape_template_details(template_url, driver)
            if template_data:
                data.append(template_data)

        return data
    finally:
        driver.quit()

def save_to_csv(data, filename='scraped_miro_templates.csv'):
    """
    Save the scraped data to a CSV file.
    
    :param data: List of dictionaries containing template data
    :param filename: Name of the output CSV file
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    start_url = "https://miro.com/miroverse/popular/?sort=likes"
    
    # Start the scraping process
    scraped_data = scrape_templates(start_url)
    
    # Save the scraped data to a CSV file
    save_to_csv(scraped_data)
    
    print(f"Scraped {len(scraped_data)} templates. Data saved to scraped_miro_templates.csv")

# Explanation of changes and reasoning:
# 1. We switched to using Selenium WebDriver instead of requests and BeautifulSoup. This is because the Miro website
#    likely uses JavaScript to load its content dynamically, which simple requests can't handle.
# 2. The setup_driver() function is added to configure Selenium WebDriver with Chrome in headless mode.
# 3. In scrape_template_list(), we now use Selenium to wait for the template cards to load and then extract
#    information from them. We use data-testid attributes where possible, as these are less likely to change
#    than class names or XPaths.
# 4. In scrape_template_details(), we again use Selenium to navigate to each template page and extract the
#    title and description. We use data-testid attributes here as well.
# 5. The main scraping logic in scrape_templates() remains similar, but now uses a single WebDriver instance
#    for all operations, which is more efficient.
# 6. We've updated the start_url to the provided Miro templates page.
# 7. Error handling and WebDriverWait are used to make the scraping more robust against timing issues or
#    slow-loading elements.

# Note: This code assumes you have Selenium and the Chrome WebDriver installed. You'll need to install these
# dependencies and update the path to the ChromeDriver in the setup_driver() function.



