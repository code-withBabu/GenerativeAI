import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb
import requests

st.set_page_config(page_title="Invoice Q&A", layout="wide")
st.title("📄 Invoice Question & Answer System")

# Initialize components (cached for performance)
@st.cache_resource
def load_models():
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    chroma_client = chromadb.PersistentClient(path="./data")
    collection = chroma_client.get_collection(name="invoices")
    
    return embedding_model, collection

embedding_model, collection = load_models()

def retrieve_chunks(query, top_k=3):
    query_embedding = embedding_model.encode(query)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )
    return results

def generate_answer(query, relevant_chunks):
    context = "\n---\n".join(relevant_chunks)
    
    prompt = f"""You are a helpful assistant that answers questions about invoices.
Use the provided invoice data to answer the question. If you cannot find the answer, say "I don't have that information."

Invoice Data:
{context}

Question: {query}

Answer:"""
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {e}"

# Sidebar for settings
st.sidebar.header("Settings")
top_k = st.sidebar.slider("Number of documents to retrieve", 1, 10, 3)

# Main interface
question = st.text_input("Ask a question about your invoices:", placeholder="e.g., What's the total amount?")

if question:
    with st.spinner("Searching invoices..."):
        results = retrieve_chunks(question, top_k=top_k)
    
    if results["documents"] and results["documents"][0]:
        st.success(f"Found {len(results['documents'][0])} relevant document chunks")
        
        with st.spinner("Generating answer..."):
            answer = generate_answer(question, results["documents"][0])
        
        st.subheader("Answer:")
        st.write(answer)
        
        # Show sources
        with st.expander("📋 Sources"):
            for i, (chunk, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
                st.write(f"**Chunk {i+1}** (from {metadata['source']})")
                st.write(chunk[:300] + "...")
    else:
        st.warning("No relevant invoices found for your question.")

st.sidebar.markdown("---")
st.sidebar.info("This system uses open-source Mistral LLM and embeddings. All data is processed locally.")