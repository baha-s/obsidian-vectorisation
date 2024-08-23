import openai
import os
import requests

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_background(prompt, output_path):
    # Generate an image using DALL-E
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']

    # Download the image and save it to the specified path
    image_data = requests.get(image_url).content
    with open(output_path, 'wb') as handler:
        handler.write(image_data)
