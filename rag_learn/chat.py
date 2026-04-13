from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
from openai import OpenAI

load_dotenv()

#Vector-embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

#take user input
user_query = input("Ask something: ")

#relevant chunks from vector db
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata.get('page', result.metadata.get('page_label', 'Unknown'))}\n"
    f"File location: {result.metadata.get('source', 'Unknown')}"
    for result in search_results
])

SYSTEM_PROMPT = f"""
You are a helpful AI assistant who answers user query based on the available context retireved from a PDF file
along with page_contents & page number.
You should only ans the user based on the following context & navigate the user to open the right page number to know more.

Context: 
{context}
"""

response = client.chat.completions.create(
        model = "gemini-3-flash-preview",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

print(f"🚀 {response.choices[0].message.content}")