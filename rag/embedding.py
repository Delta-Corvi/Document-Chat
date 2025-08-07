import os
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "models/embedding-001"

def embed_texts(texts: List[str]) -> List[List[float]]:
    """Restituisce gli embedding di una lista di testi."""
    response = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=texts,
        task_type="retrieval_document"
    )
    return response["embedding"]