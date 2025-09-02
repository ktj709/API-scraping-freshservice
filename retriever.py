import pickle
import numpy as np
from typing import List, Dict, Tuple
from config import Config
from embedder import embed_texts

def _cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-12)
    b = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-12)
    return a @ b.T

def load_index() -> Tuple[np.ndarray, List[Dict]]:
    with open(Config.INDEX_PATH, "rb") as f:
        matrix = pickle.load(f)
    with open(Config.METADATA_PATH, "rb") as f:
        meta = pickle.load(f)
    return matrix, meta

def retrieve(query: str, top_k: int = None) -> List[Dict]:
    if top_k is None:
        top_k = Config.TOP_K
    matrix, meta = load_index()
    q_emb = embed_texts([query])
    sims = _cosine_sim(q_emb, matrix)
    scores = sims[0]
    idx = np.argsort(-scores)[:top_k]

    results = []
    for i in idx:
        m = meta[i].copy()
        m["score"] = float(scores[i])
        # 🔹 attach snippet of content for debugging
        if "content" in meta[i]:
            m["content"] = meta[i]["content"][:300] + "..."
        results.append(m)
    return results
