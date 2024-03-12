import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

class ApiGpt:

    @staticmethod
    def call_gpt(prompt):
        # Initialize OpenAI API with the key from the environment
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), )

        # Process the prompt and return the result
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content

    @staticmethod
    def extract_text_between_tags(text, start_tag, end_tag):
        pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
        matches = re.findall(pattern, text, re.DOTALL)
        return matches[0].strip() if matches else ""