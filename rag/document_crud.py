import json, os, uuid
from typing import List, Dict, Any

DOCS_PATH = "data/documents.jsonl"

class DocumentCRUD:
    """
    Gestisce il JSONL come DB semplice.
    Ogni record ha chiave 'id' univoca.
    """
    def __init__(self):
        self.docs: Dict[str, Dict[str, Any]] = {}
        self._ensure_data_dir()
        self._load()

    def _ensure_data_dir(self):
        """Crea la cartella data se non esiste"""
        data_dir = os.path.dirname(DOCS_PATH)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
            print(f"📁 Created folder: {data_dir}")

    def _load(self):
        if os.path.exists(DOCS_PATH):
            try:
                with open(DOCS_PATH, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:  # Ignora righe vuote
                            rec = json.loads(line)
                            self.docs[rec["id"]] = rec
                print(f"📚 Loaded {len(self.docs)} documents from database")
            except Exception as e:
                print(f"⚠️ Error loading database: {e}")
                self.docs = {}

    def _save(self):
        try:
            self._ensure_data_dir()  # Assicurati che la cartella esista prima di salvare
            with open(DOCS_PATH, "w", encoding="utf-8") as f:
                for rec in self.docs.values():
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"💾 Database saved: {len(self.docs)} documents")
        except Exception as e:
            print(f"❌ Error saving database: {e}")
            raise

    def list(self) -> List[Dict[str, Any]]:
        return list(self.docs.values())

    def get(self, doc_id: str) -> Dict[str, Any] | None:
        return self.docs.get(doc_id)

    def add(self, doc: Dict[str, Any]) -> str:
        if "id" not in doc:
            doc["id"] = str(uuid.uuid4())
        self.docs[doc["id"]] = doc
        self._save()
        return doc["id"]

    def add_batch(self, docs: List[Dict[str, Any]]):
        for d in docs:
            if "id" not in d:
                d["id"] = str(uuid.uuid4())
            self.docs[d["id"]] = d
        self._save()
        print(f"✅ Added {len(docs)} documents to database")

    def update(self, doc_id: str, new_text: str):
        if doc_id in self.docs:
            self.docs[doc_id]["text"] = new_text
            self._save()
            return True
        return False

    def delete(self, doc_id: str):
        if doc_id in self.docs:
            del self.docs[doc_id]
            self._save()
            return True
        return False