import asyncio
import json
import pandas as pd
from selenium_handler import setup_selenium, fetch_template_urls
from data_processor import process_url
from config import MAIN_URL, FIELDS, TEST_LIMIT

async def main():
    driver = await setup_selenium()
    try:
        template_urls = await fetch_template_urls(driver, MAIN_URL)
        if not template_urls:
            print("No template URLs found. Exiting.")
            return []

        # Limit to TEST_LIMIT links for testing
        template_urls = template_urls[:TEST_LIMIT]
        print(f"Processing {len(template_urls)} links for testing.")

        tasks = [process_url(url, FIELDS) for url in template_urls]
        all_data = await asyncio.gather(*tasks)
        
        if all_data:
            export_data(all_data)
            print(f"Processed {len(all_data)} templates.")
        else:
            print("No data to export.")
        
        return all_data
    finally:
        await asyncio.to_thread(driver.quit)

def export_data(data):
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=2)
    df = pd.DataFrame(data)
    df.to_excel('output.xlsx', index=False)

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
