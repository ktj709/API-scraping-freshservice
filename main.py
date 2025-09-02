import argparse
from config import Config, ensure_dirs
from scraper import scrape
from processor import process_from_file
from embedder import build_index
from retriever import retrieve
from llm_handler import answer_query

def cli():
    parser = argparse.ArgumentParser(description="Freshservice API RAG Pipeline")
    parser.add_argument("cmd", choices=["scrape", "process", "build-index", "ask", "all"], help="Command to run")
    parser.add_argument("--q", type=str, help="Query for 'ask' command")
    args = parser.parse_args()

    ensure_dirs()

    if args.cmd == "scrape":
        scrape()

    elif args.cmd == "process":
        process_from_file()

    elif args.cmd == "build-index":
        build_index()

    elif args.cmd == "ask":
        results = retrieve(args.q, top_k=Config.TOP_K)
        resp = answer_query(args.q, results)
        print("\n=== ANSWER ===\n")
        print(resp["answer"])
        print("\n=== CITATIONS ===")
        for c in resp["citations"]:
            print(f"- {c['title']} — {c['url']} (section: {c['section']})")

    elif args.cmd == "all":
        scrape()
        process_from_file()
        build_index()

if __name__ == "__main__":
    cli()
