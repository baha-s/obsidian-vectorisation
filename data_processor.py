import aiohttp
from bs4 import BeautifulSoup
import openai
import os
from gpt_handler import format_data_with_gpt

async def fetch_html(url, session):
    async with session.get(url) as response:
        return await response.text()

def html_to_markdown(html):
    soup = BeautifulSoup(html, 'html.parser')
    return ' '.join(soup.stripped_strings)

def format_to_json(extracted_text):
    lines = extracted_text.split('\n')
    json_data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            json_data[key.strip()] = value.strip()
    return json_data

async def process_url(url, fields):
    async with aiohttp.ClientSession() as session:
        html = await fetch_html(url, session)
    markdown = html_to_markdown(html)
    extracted_text = await format_data_with_gpt(markdown, fields)
    json_data = format_to_json(extracted_text)
    json_data['URL'] = url
    return json_data