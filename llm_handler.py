import json
from typing import List, Dict
from config import Config
from google import genai

SYSTEM_PROMPT = """You are a helpful assistant for Freshservice API users.
Answer strictly using the provided documentation context.

Guidelines:
- Always prefer the **main ticket creation endpoint** (/api/v2/tickets) when user asks "create a ticket".
- Include a complete **cURL example**.
- List and explain all **parameters** (description, subject, email, priority, status, cc_emails, workspace_id, etc.) using details from the docs.
- Be concise and structured (use bullet points for parameters).
- Cite the section title and URL at the end.
- If the answer is not found in context, clearly say so.
"""

def _get_gemini_client():
    if not Config.GEMINI_API_KEY:
        raise RuntimeError("❌ GEMINI_API_KEY not set in .env file")
    return genai.Client(api_key=Config.GEMINI_API_KEY)

def build_prompt(query: str, contexts: List[Dict], full_chunks: Dict[str, str]) -> str:
    """Builds the final prompt with context for Gemini"""
    ctx_blocks = []
    for c in contexts:
        cid = c["chunk_id"]
        ctx_text = full_chunks.get(cid, "")
        ctx_blocks.append(
            f"### Source\nTitle: {c.get('title')}\nURL: {c.get('url')}\n\n{ctx_text}"
        )
    ctx_str = "\n\n---\n\n".join(ctx_blocks)
    return f"{SYSTEM_PROMPT}\n\nContext:\n{ctx_str}\n\nUser Question:\n{query}"

def load_full_chunks() -> Dict[str, str]:
    with open(Config.PROCESSED_JSON, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return {c["chunk_id"]: c["content"] for c in chunks}

def answer_query(query: str, retrieved: List[Dict]) -> Dict:
    """Generate an answer from Gemini using retrieved docs"""
    full_chunks = load_full_chunks()
    prompt = build_prompt(query, retrieved, full_chunks)

    if Config.USE_GEMINI_LLM:
        client = _get_gemini_client()
        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=[prompt]
        )
        text = response.text
    else:
        stitched = "\n\n".join(full_chunks.get(r["chunk_id"], "") for r in retrieved)
        text = f"Answer (fallback, no LLM):\n\n{stitched[:1000]}"

    # Clean citations (remove duplicate anchors)
    citations = []
    seen = set()
    for r in retrieved:
        key = (r["title"], r["url"])
        if key not in seen:
            citations.append({
                "url": r["url"],
                "title": r["title"],
                "section": r.get("section_id", "")
            })
            seen.add(key)

    return {
        "answer": text,
        "citations": citations
    }
