from mem0 import Memory
import os
from dotenv import load_dotenv
from google import genai
from neo4j import GraphDatabase
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": GOOGLE_API_KEY,
            "model": "models/gemini-embedding-001",
        }
    },

   "llm": {
        "provider": "openai",
        "config": {
            "api_key": os.getenv("GOOGLE_API_KEY"), 
            "model": "gemini-2.5-flash",
            "openai_base_url": "https://generativelanguage.googleapis.com/v1beta/openai/"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "mem0_gemini_coll",
            "embedding_model_dims": 768
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": uri,
            "username": user,
            "password": password
        }
    }
}

mem_client = Memory.from_config(config)

print(f"Attempting to connect to: {uri}")
print(f"Using username: {user}")

try:
    # Attempt to build the driver and verify the connection
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    print("\n✅ SUCCESS: Python is securely connected to Neo4j AuraDB!")
    driver.close()
except Exception as e:
    print("\n❌ ERROR: Connection failed. Read the error below:")
    print("-" * 40)
    print(e)
    
while True:
    
    user_input = input("> ")

    # ==========================================
    # NEW STEP: Retrieve past memories first!
    # ==========================================
    print("Thinking and checking memory...")

    past_memories = mem_client.search(query=user_input, filters={"user_id": "Adarsh"})

    # Build a context string from whatever Qdrant finds
    context = ""
    if past_memories and "results" in past_memories:
        context = "Here is what you remember about the user from previous chats:\n"
        
        # 2. Loop through the actual list INSIDE the "results" dictionary!
        for mem in past_memories["results"]:
            context += f"- {mem['memory']}\n"

    # Combine the memory with the user's current question
    final_prompt = f"""
    {context}

    Current User Message: {user_input}
    """
    # ==========================================

    # Send the combined prompt to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt 
    )

    ai_response = response.text

    print("AI: ", ai_response)

    # Save the new interaction to memory for next time
    mem_client.add(
        user_id="Adarsh",
        messages=[
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": ai_response}
        ]
    )

    print("Memory has been saved...")