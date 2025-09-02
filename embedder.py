import os
import pickle
import json
from typing import List, Dict
import numpy as np
from config import Config, ensure_dirs
from sentence_transformers import SentenceTransformer

def embed_texts(texts: List[str]) -> np.ndarray:
    model = SentenceTransformer(Config.EMBEDDING_MODEL)
    embs = model.encode(texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)
    return embs.astype(np.float32)

def build_index() -> None:
    ensure_dirs()
    with open(Config.PROCESSED_JSON, "r", encoding="utf-8") as f:
        chunks: List[Dict] = json.load(f)

    texts = [c["content"] for c in chunks]
    embeddings = embed_texts(texts)

    metadata = [{"chunk_id": c["chunk_id"], "url": c["url"], "title": c["title"], "section_id": c["section_id"]} for c in chunks]

    with open(Config.INDEX_PATH, "wb") as f:
        pickle.dump(embeddings, f)
    with open(Config.METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"Index built with {len(chunks)} chunks.")
