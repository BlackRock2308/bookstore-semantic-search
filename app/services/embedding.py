import os
import requests
from typing import List


HF_TOKEN = os.getenv("HF_TOKEN")
EMBEDDING_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text: str) -> List[float]:
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN is missing. Please check your .env file.")
    
    response = requests.post(
        EMBEDDING_URL,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": text}
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed: {response.text}")
    
    return response.json()
