import openai
import os
import re
from dotenv import load_dotenv
import ast

# Load environment variables from .env
load_dotenv()

def callGpt(prompt):
    # Initialize OpenAI API with the key from the environment
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    # Process the prompt and return the result
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Choose the appropriate chat model
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message['content']

def extract_text_between_tags(text, start_tag="[stocks]", end_tag="[/stocks]"):
    pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0].strip() if matches else ""