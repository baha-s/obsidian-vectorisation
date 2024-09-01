import asyncio
import json
import pandas as pd
from .selenium_handler import setup_selenium, fetch_template_urls
from .data_processor import process_url
from .config import MAIN_URL, FIELDS, TEST_LIMIT

async def main():
    # ... (rest of the code remains the same)

def export_data(data):
    # ... (rest of the code remains the same)

# Remove the if __name__ == "__main__": block from here