import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

print("=" * 70)
print("AVAILABLE GEMINI MODELS")
print("=" * 70)

for model in client.models.list():

    name = model.name or ""

    if "gemini" in name.lower():
        print(name)