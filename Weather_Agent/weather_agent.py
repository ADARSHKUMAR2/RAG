from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

def currWeather():
    user_query = input("> ") 
    response = client.chat.completions.create(
        model = "gemini-3-flash-preview",
        messages=[
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    print(f"🚀 {response.choices[0].message.content}")
