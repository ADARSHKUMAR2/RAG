import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from google import genai 

load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

# 2. Native Gemini Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def process_query(query:str):
    search_results = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([
        f"Page Content: {result.page_content}\n"
        f"Page Number: {result.metadata.get('page', result.metadata.get('page_label', 'Unknown'))}\n"
        f"File location: {result.metadata.get('source', 'Unknown')}"
        for result in search_results
    ])

    SYSTEM_PROMPT = f"""
    You are a helpful AI assistant who answers user query based on the available context retrieved from a PDF file.
    You should only ans the user based on the following context & navigate the user to open the right page number to know more.

    Context: 
    {context}
    """

    # 3. Native generation method!
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=query,
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
    
    print(f"🚀 {response.text}")
    return response.text