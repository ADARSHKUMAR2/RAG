import os
import logging
from dotenv import load_dotenv
from mem0 import Memory

# 1. Turn on maximum debugging so we can see the LLM's raw thoughts
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "model": "models/gemini-embedding-001",
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": os.getenv("GITHUB_TOKEN"), # Your GH Token
            "model": "gpt-4o-mini",               # Or "Llama-3.1-70b-Instruct"
            "openai_base_url": "https://models.inference.ai.azure.com" # GitHub's endpoint
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
            "url": os.getenv("NEO4J_URI"),
            "username": os.getenv("NEO4J_USERNAME"),
            "password": os.getenv("NEO4J_PASSWORD")
        }
    }
}

print("Initializing Memory...")
m = Memory.from_config(config)

print("Sending prompt to Graph Extractor...")

# Use a new fake user ID
test_prompt = "Vatsa is the CEO of Jabali. Jabali is an AI company."
m.add(test_prompt, user_id="fresh_test_user_02")

print("Finished!")