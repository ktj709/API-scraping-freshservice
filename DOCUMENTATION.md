## 📘 System Documentation – Freshservice API RAG Assistant
## 1. Overview

This project is a Retrieval-Augmented Generation (RAG) system built for the Freshservice API Documentation.
It allows users to query the API documentation and receive natural language answers along with citations.

The system uses:

Web Scraping to extract documentation.

Preprocessing & Chunking to structure the text.

Embeddings + Vector Index to enable semantic search.

Retriever to fetch relevant context.

LLM (Gemini 1.5 Flash) to generate the final answers.

Streamlit UI + CLI for user interaction.

## 2. System Architecture
### Step 1: Scraping (scraper.py)

Fetches the Ticket Attributes page from the Freshservice API documentation.

Extracts sections based on headings (h1, h2, h3).

Stores raw results into data/raw_freshservice_docs.json.

### Step 2: Preprocessing (processor.py)

Cleans HTML text into plain text.

Splits large sections into chunks (size = 1000 characters, overlap = 200).

Saves structured chunks into data/processed_chunks.json.

### Step 3: Embeddings & Indexing (embedder.py)

Converts chunks into vector embeddings using sentence-transformers/all-MiniLM-L6-v2.

Stores index and metadata (vector_index.pkl, vector_metadata.pkl).

### Step 4: Retrieval (retriever.py)

For a user query, retrieves the Top-K most relevant chunks using cosine similarity.

### Step 5: LLM Query Handling (llm_handler.py)

Constructs a prompt with user query + retrieved context.

Sends the request to Gemini 1.5 Flash (google-generativeai).

Returns the answer along with citations.

### Step 6: User Interaction

CLI (main.py) → run pipeline commands (scrape, process, build-index, ask, all).

Streamlit App (app.py) → ask questions via web UI.

## 3. Data Flow
Scraper → Raw Docs → Processor → Chunks → Embedder → Vector Index → Retriever → LLM Handler → Answer + Citations

## 4. Example Usage
## CLI
python main.py scrape
python main.py process
python main.py build-index
python main.py ask --q "Give me the curl command to create a ticket"

## Streamlit UI
streamlit run interface.py

## 5. Example Output
=== ANSWER ===
To create a ticket, use the following cURL command:
curl -v -u api_key:X -H "Content-Type: application/json" -d '{...}' -X POST 'https://domain.freshservice.com/api/v2/tickets'

=== CITATIONS ===
- Ticket Properties — https://api.freshservice.com/#ticket_attributes
- Create Ticket with associations — https://api.freshservice.com/#ticket_attributes

## 6. Key Design Decisions

Focused Scraping: Only scrapes the Ticket Attributes page (reduces noise).

Chunking with Overlap: Ensures answers have full context without cutting important details.

Citations Included: Provides transparency and trustworthiness.

## 7. Future Improvements

Extend scraping to multiple API documentation pages.

Add vector database (e.g., FAISS, Pinecone) for large-scale indexing.

Enhance prompt templates for better structured answers.

Deploy Streamlit app online (Streamlit Cloud, Hugging Face Spaces, etc.).
