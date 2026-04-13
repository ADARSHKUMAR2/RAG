from google import genai
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = """
You are a helpful assistant.
Add START, PLAN, OUTPUT to the response.
""" 

message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

user_query = input("🫵🏻")
message_history.append({
    "role": "user",
    "content": user_query
})

while True:
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        response_format={"type": "json_object"},
        n=1,
        messages=message_history
        )

    raw_result = response.choices[0].message.content
    message_history.append({
        "role": "assistant",
        "content": raw_result
    })
    parsed_result = json.loads(raw_result)
    
    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("message"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("💡", parsed_result.get("message"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("💬", parsed_result.get("message"))
        break

