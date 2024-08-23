from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

def generate_background(prompt, output_path):
    # Generate an image using DALL-E
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0]['url']

    # Download the image and save it to the specified path
    image_data = requests.get(image_url).content
    with open(output_path, 'wb') as handler:
        handler.write(image_data)
