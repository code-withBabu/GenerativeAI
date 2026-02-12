from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
import pdfplumber
import os

# Initialize local embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Chroma with new client (simpler, no Settings needed)
chroma_client = chromadb.PersistentClient(path="./data")

# Create or get collection
collection = chroma_client.get_or_create_collection(
    name="invoices",
    metadata={"hnsw:space": "cosine"}
)

def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks"""
    chunks = []
    tokens = text.split()
    
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = " ".join(tokens[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def process_documents():
    """Extract, chunk, embed, and store documents"""
    doc_count = 0
    chunk_count = 0
    #get testdata directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdffolderpath = os.path.join(current_dir, 'documents')
    
    for pdf_file in Path(pdffolderpath).glob("*.pdf"):
        print(f"Processing: {pdf_file.name}")
        
        try:
            with pdfplumber.open(pdf_file) as pdf:
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
            
            # Chunk the text
            chunks = chunk_text(full_text, chunk_size=500, overlap=100)
            
            # Generate embeddings and store
            for i, chunk in enumerate(chunks):
                embeddings = embedding_model.encode(chunk)
                
                collection.add(
                    ids=[f"{pdf_file.stem}_chunk_{i}"],
                    embeddings=[embeddings.tolist()],
                    documents=[chunk],
                    metadatas=[{"source": pdf_file.name, "chunk": i}]
                )
            
            doc_count += 1
            chunk_count += len(chunks)
            print(f"✓ Created {len(chunks)} chunks")
        
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n✓ Indexed {doc_count} documents into {chunk_count} chunks")

if __name__ == "__main__":
    process_documents()