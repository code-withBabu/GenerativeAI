from sentence_transformers import SentenceTransformer
import chromadb
import requests

# Initialize components
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

chroma_client = chromadb.PersistentClient(path="./data")
collection = chroma_client.get_collection(name="invoices")

# Ollama API endpoint
OLLAMA_API = "http://localhost:11434/api/generate"

def retrieve_relevant_chunks(query, top_k=3):
    """Search vector database for relevant chunks"""
    query_embedding = embedding_model.encode(query)
    
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )
    
    return results

def generate_answer(query, relevant_chunks):
    """Send query + context to Ollama LLM"""
    
    # Build context from retrieved chunks
    context = "\n---\n".join(relevant_chunks)
    
    # Create prompt
    prompt = f"""You are a helpful assistant that answers questions about invoices.
Use the provided invoice data to answer the question. If you cannot find the answer in the data, say "I don't have that information."

Invoice Data:
{context}

Question: {query}

Answer:"""
    
    # Call Ollama
    try:
        response = requests.post(
            OLLAMA_API,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3
            },timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]
    
    except Exception as e:
        return f"Error generating response: {e}"

def query_invoices(question):
    """Main RAG function"""
    print(f"\nQuestion: {question}")
    print("Searching documents...")
    
    # Retrieve relevant chunks
    results = retrieve_relevant_chunks(question, top_k=3)
    
    if not results["documents"] or not results["documents"][0]:
        return "No relevant invoice data found."
    
    relevant_chunks = results["documents"][0]
    sources = results["metadatas"][0]
    
    print(f"Found {len(relevant_chunks)} relevant chunks from {set([s['source'] for s in sources])}")
    
    # Generate answer
    answer = generate_answer(question, relevant_chunks)
    
    return answer

if __name__ == "__main__":
    # Test queries
    # test_queries = [
    #     "What is the total invoice amount?",
    #     "Who are the vendors mentioned?",
    #     "What are the invoice dates?",
    #     "What items were invoiced?"
    # ]
    test_queries = [
        "What is the total invoice amount?",
        "Who are the vendors mentioned?"
    ]
    
    for query in test_queries:
        answer = query_invoices(query)
        print(f"Answer: {answer}\n")