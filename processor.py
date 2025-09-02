import json
from typing import List, Dict
from config import Config, ensure_dirs
from utils import clean_text, chunk_text

def process_docs(raw_docs: List[Dict]) -> List[Dict]:
    chunks: List[Dict] = []
    for d in raw_docs:
        text = clean_text(d.get("content", ""))
        if not text:
            continue
        parts = chunk_text(text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
        for i, ch in enumerate(parts):
            chunks.append({
                "chunk_id": f"{d.get('url')}|{d.get('section_id')}|{i}",
                "url": d.get("url", ""),
                "title": d.get("title", ""),
                "section_id": d.get("section_id", ""),
                "content": ch
            })
    return chunks

def process_from_file() -> List[Dict]:
    ensure_dirs()
    with open(Config.RAW_JSON, "r", encoding="utf-8") as f:
        raw = json.load(f)
    chunks = process_docs(raw)
    with open(Config.PROCESSED_JSON, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    return chunks
