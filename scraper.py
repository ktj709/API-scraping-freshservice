import json
import requests
from typing import Dict, List
from bs4 import BeautifulSoup
from config import Config, ensure_dirs

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; FreshserviceRAG/1.0)"}

def extract_sections(url: str, html: str) -> List[Dict]:
    """Extract sections (headings + content) from a single page"""
    soup = BeautifulSoup(html, "html.parser")
    docs = []

    for h in soup.find_all(["h1", "h2", "h3"]):
        title = h.get_text(" ", strip=True)
        section_id = h.get("id") or title.lower().replace(" ", "-")
        content_nodes = []
        for sib in h.next_siblings:
            if getattr(sib, "name", None) in ["h1", "h2", "h3"]:
                break
            content_nodes.append(str(sib))
        section_html = "".join(content_nodes)
        text = BeautifulSoup(section_html, "html.parser").get_text("\n", strip=True)
        if text:
            docs.append({
                "url": url,
                "title": title,
                "section_id": section_id,
                "content": text
            })

    # Fallback: whole page if no structured sections
    if not docs:
        docs.append({
            "url": url,
            "title": soup.title.get_text(strip=True) if soup.title else "Untitled",
            "section_id": "page",
            "content": soup.get_text("\n", strip=True)
        })
    return docs

def scrape(start_url: str = Config.START_URL) -> List[Dict]:
    """
    Scrape ONLY the Ticket Attributes / Ticket API page.
    Does not crawl external links.
    """
    ensure_dirs()
    results: List[Dict] = []

    try:
        resp = requests.get(start_url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        docs = extract_sections(start_url, resp.text)
        results.extend(docs)
    except Exception as e:
        print(f"❌ Error fetching {start_url}: {e}")

    with open(Config.RAW_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ Scraped {len(results)} sections from {start_url} → {Config.RAW_JSON}")
    return results

if __name__ == "__main__":
    scrape()
