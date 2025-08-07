import fitz, os, uuid, json
from typing import List, Dict, Any
from .faiss_store import FaissStore
from .document_crud import DocumentCRUD

def process_pdf(file_path: str, store: FaissStore, crud: DocumentCRUD,
                chunk_size: int = 800, overlap: int = 100) -> None:
    """
    - file_path: percorso al PDF
    - chunk_size / overlap: suddivisione testo
    - crea un record per ogni chunk
    """
    with fitz.open(file_path) as doc:
        full_text = ""
        for page in doc:
            full_text += page.get_text()

    chunks = []
    start = 0
    doc_id = str(uuid.uuid4())
    while start < len(full_text):
        end = start + chunk_size
        chunk_text = full_text[start:end]
        if not chunk_text.strip():
            break
        record = {
            "id": f"{doc_id}_{len(chunks)}",
            "source": os.path.basename(file_path),
            "page": None,  # si può migliorare mantenendo page info
            "text": chunk_text
        }
        chunks.append(record)
        start += chunk_size - overlap

    store.add_documents(chunks)
    crud.add_batch(chunks)