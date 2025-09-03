import streamlit as st
from config import Config
from retriever import retrieve
from llm_handler import answer_query

st.set_page_config(page_title="Freshservice API RAG", layout="wide")

st.title("🔎 Freshservice API RAG Assistant")

query = st.text_input("Ask about Freshservice API:")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        results = retrieve(query, top_k=Config.TOP_K)
        resp = answer_query(query, results)
        
        st.subheader("Answer")
        st.markdown(resp["answer"])
        
        st.subheader("Citations")
        for c in resp["citations"]:
            st.write(f"- **{c['title']}** — {c['url']} (section: {c['section']})")
