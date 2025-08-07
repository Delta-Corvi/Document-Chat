import google.generativeai as genai
import os
from typing import List, Dict, Any
from .faiss_store import FaissStore

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
llm = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = (
    "You are an AI assistant for a document management system. "
    "Use the provided context to answer questions in a concise and accurate manner. "
    "If you don't find relevant information, clearly state that you don't have that information."
)

def answer(query: str, store: FaissStore) -> str:
    chunks = store.search(query, k=4)
    context = "\n\n".join(c["text"] for c in chunks)
    prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {query}"

    response = llm.generate_content(prompt)
    return response.text