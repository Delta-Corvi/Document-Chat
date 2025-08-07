import json, os, numpy as np
import faiss
from typing import List, Dict, Any
from .embedding import embed_texts

VECTOR_DIM = 768        # dimensione degli embedding Gemini
INDEX_PATH = "data/faiss.index"
METADATA_PATH = "data/metadata.jsonl"

class FaissStore:
    def __init__(self):
        self.index = None
        self.metadata = []
        # Crea la cartella data se non esiste
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Crea la cartella data se non esiste"""
        data_dir = os.path.dirname(INDEX_PATH)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
            print(f"📁 Created folder: {data_dir}")

    def load_or_create(self):
        self._ensure_data_dir()  # Assicurati che la cartella esista sempre

        if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
            try:
                self.index = faiss.read_index(INDEX_PATH)
                with open(METADATA_PATH, "r", encoding="utf-8") as f:
                    self.metadata = [json.loads(line) for line in f if line.strip()]
                print(f"📚 Loaded existing index with {self.index.ntotal} documents")
            except Exception as e:
                print(f"⚠️ Error loading existing index: {e}")
                print("🔄 Creating new index...")
                self.index = faiss.IndexFlatIP(VECTOR_DIM)  # cosine similarity
                self.metadata = []
        else:
            self.index = faiss.IndexFlatIP(VECTOR_DIM)  # cosine similarity
            self.metadata = []
            print("🆕 Created new FAISS index")

    def add_documents(self, docs: List[Dict[str, Any]]):
        if not docs:
            return

        texts = [d["text"] for d in docs]
        try:
            embeddings = embed_texts(texts)
            vectors = np.array(embeddings).astype("float32")
            self.index.add(vectors)
            self.metadata.extend(docs)
            self._persist()
            print(f"✅ Added {len(docs)} documents to index")
        except Exception as e:
            print(f"❌ Error adding documents: {e}")
            raise

    def _persist(self):
        try:
            self._ensure_data_dir()  # Assicurati che la cartella esista prima di salvare
            faiss.write_index(self.index, INDEX_PATH)
            with open(METADATA_PATH, "w", encoding="utf-8") as f:
                for m in self.metadata:
                    f.write(json.dumps(m, ensure_ascii=False) + "\n")
            print(f"💾 Index saved: {self.index.ntotal} documents")
        except Exception as e:
            print(f"❌ Error saving index: {e}")
            raise

    def search(self, query: str, k: int = 4):
        if self.index.ntotal == 0 or not self.metadata:
            print("⚠️ No documents in index")
            return []

        try:
            query_vec = np.array(embed_texts([query])).astype("float32")
            scores, indices = self.index.search(query_vec, k)

            # indici validi e unici
            valid = []
            seen = set()
            for i in indices[0]:
                if 0 <= i < len(self.metadata) and i not in seen:
                    valid.append(i)
                    seen.add(i)
            results = [self.metadata[i] for i in valid]
            print(f"🔍 Found {len(results)} results for query")
            return results
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []