import os
import requests
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from google import genai 

load_dotenv()

# 1. Initialize the Native Google Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Download the image from the URL so Gemini can see it
image_url = "https://images.pexels.com/photos/34703257/pexels-photo-34703257.png"
image_response = requests.get(image_url)
img = Image.open(BytesIO(image_response.content))

# 3. Use the native models.generate_content method
# Notice how you can just pass the text and the image in a simple list!
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Generate a caption for this image", 
        img
    ]
)

# 4. Native Gemini response format
print("Response :", response.text)