from openai import OpenAI
import os
import requests

# Set your OpenAI API key
client = OpenAI()

def generate_background(prompt, output_path):
    # Generate an image using DALL-E
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="512x512",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url

    # Download the image and save it to the specified path
    image_data = requests.get(image_url).content
    with open(output_path, 'wb') as handler:
        handler.write(image_data)
