import os
import openai
from typing import List
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url = "https://api.mistral.ai/v1")

# This model will geneate an emebddigs of dim 1024
EMBEDDING_MODEL = "mistral-embed"

def embed_text(text: str,embedding_model:str=EMBEDDING_MODEL) -> List[float]:
    '''
    embed any piece of text into a 1024 dim vector based on choice of model used!
    Args:
        text (str): The text you want to embed
        embedding_model (str): which model to use

    Returns:
        List[float]: The vector of the piece of text.
    '''
    response = client.embeddings.create(
        model=embedding_model,
        input=text,
    )
    return response.data[0].embedding