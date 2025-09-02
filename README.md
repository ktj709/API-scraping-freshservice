## 📘 Freshservice API RAG Assistant (Gemini 2.0 Flash)

This project implements a Retrieval-Augmented Generation (RAG) pipeline to interact with the Freshservice API documentation
.
It scrapes the API docs, processes them into semantic chunks, builds a vector index, and answers user queries using Gemini 2.0 Flash (with OpenAI fallback).

## 🚀 Features

Scrapes Freshservice API docs (Ticket Attributes section).

Cleans and chunks documentation text.

Generates embeddings with SentenceTransformers.

Retrieves top-k relevant chunks for a query.

Answers questions using Gemini 2.0 Flash (fallback to OpenAI GPT-4o-mini).

Provides source citations with every answer.

Includes a Streamlit UI for interactive search.


## 🛠️ Setup

1. Clone the Repo

git clone https://github.com/ktj709/API-scraping-freshservic)



2. Install Dependencies

Run this inside your project folder:

pip install -r requirements.txt


3. Add API Keys

Create a .env file in the project root and add your keys:

GEMINI_API_KEY=your_gemini_api_key


## ⚡ Usage

### CLI Workflow

1. Scrape docs

python main.py scrape


2. Process into chunks

python main.py process


3. Build vector index

python main.py build-index


4. Ask a question

python main.py ask --q "Give me the curl command to create a ticket"


Or run the full pipeline in one step:

python main.py all

## Streamlit UI

Launch the interactive assistant:

streamlit run interface.py

## 📂 Project Structure

├── interface.py         # Streamlit frontend    
├── README.md            # This file
├── main.py              # CLI entrypoint
├── config.py            # Configuration + API keys
├── scraper.py           # Scraping docs
├── processor.py         # Cleaning + chunking
├── embedder.py          # Embedding + vector index
├── retriever.py         # Semantic retrieval
├── llm_handler.py       # Gemini / OpenAI query handler
├── utils.py             # Text cleaning + helpers
├── data/                # JSON and index files
└── requirements.txt

## ✅ Example Query

python main.py ask --q "How do I create a ticket?"

## Output:

=== ANSWER ===
To create a ticket, you can use the following cURL command...

=== CITATIONS ===
- Ticket Properties — https://api.freshservice.com/#ticket_attributes
- Create Ticket with associations — https://api.freshservice.com/#ticket_attributes
