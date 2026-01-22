import os
import openai
from typing import List
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url = "https://api.mistral.ai/v1")

# This model will geneate an emebddigs of dim 1024
EMBEDDING_MODEL = "mistral-embed"

def embed_text(text: str) -> List[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding