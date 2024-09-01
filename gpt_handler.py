import openai
import os

async def format_data_with_gpt(markdown, fields):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    client = openai.AsyncOpenAI(api_key=api_key)
    
    prompt = f"""Extract the following fields from the given text: {', '.join(fields)}. 
    Format the output as plain text, with each field on a new line in the format 'Field: Value'.
    The text is from a Miro template page."""
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured data from text."},
                {"role": "user", "content": f"{prompt}\n\nText:\n{markdown}"}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error: Unable to extract data"