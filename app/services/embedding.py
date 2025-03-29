import os
import requests
from typing import List
import asyncio


HF_TOKEN = os.getenv("HF_TOKEN")
EMBEDDING_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

async def generate_embedding(text: str) -> list[float]:
    """Asynchronously fetches embedding from Hugging Face API."""
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,  # Runs in the default ThreadPoolExecutor
        lambda: requests.post(
            EMBEDDING_URL,
            headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"},
            json={"inputs": text}
        )
    )
    
    if response.status_code != 200:
        raise ValueError(f"Request failed: {response.text}")
    
    return response.json()
