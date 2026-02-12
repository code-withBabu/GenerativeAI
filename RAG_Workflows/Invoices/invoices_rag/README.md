# Invoice Q&A System - RAG Application

An intelligent document processing system that uses Retrieval-Augmented Generation (RAG) to answer questions about invoice documents. Built with open-source models running locally for complete privacy and zero API costs.

## Features

- **Local LLM Processing**: Uses Ollama with Mistral 7B—no cloud API calls, complete data privacy
- **Vector Search**: Semantic search using Sentence Transformers embeddings and Chroma vector database
- **RAG Pipeline**: Retrieves relevant invoice data and generates accurate answers using context
- **Web UI**: Interactive Streamlit interface for easy document queries
- **Extensible Architecture**: Easily swap models, embeddings, or vector databases

## Architecture

```
User Query
    ↓
Embedding Generation (Sentence Transformers)
    ↓
Vector Search (Chroma Database)
    ↓
Context Retrieval (Relevant document chunks)
    ↓
LLM Processing (Ollama + Mistral 7B)
    ↓
Answer Generation
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Ollama + Mistral 7B | Local text generation |
| **Embeddings** | Sentence Transformers | Converting text to vectors |
| **Vector DB** | Chroma | Semantic search & storage |
| **UI** | Streamlit | Web interface |
| **Language** | Python 3.10+ | Core application |

## Prerequisites

- **Python**: 3.10 or higher
- **RAM**: Minimum 8GB (recommended 16GB for optimal performance)
- **Disk Space**: 10GB (for Mistral 7B model)
- **Ollama**: Installed and running as a service
- **Optional GPU**: NVIDIA GPU with CUDA for 10-50x faster inference

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/code-withBabu/GenerativeAI/tree/98c924f648424c246b9c555be74eaac3cdc8c66e/RAG_Workflows/Invoices/invoices_rag

cd invoices-rag
```

### Step 2: Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai)

Verify installation:
```bash
ollama --version
```

### Step 3: Download Mistral Model

```bash
ollama pull mistral
```

This downloads ~4GB and runs as a background service on `localhost:11434`.

Verify the model:
```bash
ollama list
```

You should see `mistral:latest` in the list.

### Step 4: Setup Python Environment

Create and activate virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Step 5: Prepare Invoice Data

Place your PDF invoices in the `documents/` folder:

```
invoices_rag/
├── documents/
│   ├── invoice1.pdf
│   ├── invoice2.pdf
│   └── ...
├── data/
├── embeddings_setup.py
├── main.py
└── streamlit_app.py
```

## Usage

### Step 1: Build Vector Database

Create embeddings and index your invoices:

```bash
python embeddings_setup.py
```

Expected output:
```
Processing: invoice1.pdf
✓ Created 15 chunks
Processing: invoice2.pdf
✓ Created 12 chunks
...
✓ Indexed 10 documents into 145 chunks
```

This creates a local Chroma database in the `data/` folder.

### Step 2: Test RAG Pipeline

Run the command-line interface:

```bash
python main.py
```

You'll see example queries and answers:
```
Question: What is the total invoice amount?
Found 3 relevant chunks from: {'invoice1.pdf', 'invoice2.pdf'}
Generating answer...
Answer: Based on the invoices, the total amount is $15,450.00
```

### Step 3: Launch Web UI

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

Opens at `http://localhost:8501`. Features:
- Upload and query multiple PDFs
- View retrieved document chunks (sources)
- Adjust number of documents to retrieve
- Full chat history in sidebar

## Project Structure

```
invoices_rag/
├── documents/              # Place PDF invoices here
├── data/                   # Chroma vector database (auto-generated)
├── embeddings_setup.py     # Create embeddings from PDFs
├── main.py                 # Command-line RAG interface
├── streamlit_app.py        # Web UI
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Configuration

### Adjust Model Parameters

Edit in `main.py` or `streamlit_app.py`:

```python
# Change temperature (0.0 = factual, 1.0 = creative)
json={
    "model": "mistral",
    "prompt": prompt,
    "stream": False,
    "temperature": 0.3  # Lower for factual answers
}
```

### Retrieve More/Fewer Documents

Edit retrieval count:

```python
# In main.py
results = retrieve_chunks(question, top_k=5)  # Retrieve 5 chunks instead of 3
```

### Switch to Faster Models

For faster responses on CPU, use smaller models:

```bash
ollama pull neural-chat   # ~3.5GB, 5x faster
ollama pull orca-mini     # ~1.3GB, 8x faster
```

Update code:
```python
"model": "neural-chat"  # Instead of "mistral"
```

### Enable GPU Acceleration

If you have an NVIDIA GPU, Ollama will automatically detect and use it. Provides 10-50x speedup:

```bash
# Check GPU is detected
ollama list
```

## Performance

### Expected Response Times (per query)

**On CPU (Intel i7/AMD Ryzen)**
- Mistral 7B: 20-40 seconds
- Neural-Chat: 5-10 seconds
- Orca-Mini: 2-5 seconds

**With NVIDIA GPU**
- Mistral 7B: 2-5 seconds
- Neural-Chat: 1-2 seconds

Breakdown per query:
- Embedding generation: ~1-2 seconds
- Vector search: ~0.5 seconds
- LLM inference: ~15-30 seconds (Mistral on CPU)

### Optimization Tips

1. **Use GPU**: Single biggest improvement (10-50x faster)
2. **Reduce chunk retrieval**: `top_k=2` instead of 3
3. **Use smaller model**: Neural-Chat or Orca-Mini
4. **Stream responses**: Show answers as they generate in real-time

## API Endpoints

### Ollama Generate

Used internally by the application:

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral",
    "prompt": "Your prompt here",
    "stream": false
  }'
```

### Check Ollama Status

```bash
curl http://localhost:11434/api/tags
```

## Costs

- **LLM Inference**: Free (local processing)
- **Embeddings**: Free (local processing)
- **Database**: Free (local storage)
- **Hosting**: Free (Streamlit Cloud for UI)
- **GPU**: Optional (if self-hosted) or cloud GPU ($0.30-1/hour if on cloud)

**Total: $0/month for CPU-based processing**

## Troubleshooting

### Collection Not Found Error

```
chromadb.errors.NotFoundError: Collection [invoices] does not exist
```

**Solution**: Run embeddings setup first:
```bash
python embeddings_setup.py
```

### Ollama Connection Error

```
Error: Cannot connect to Ollama. Is it running?
```

**Solution**: Start Ollama service:
```bash
ollama serve
```

### Out of Memory Error

Mistral 7B requires ~8GB RAM. Check available memory:

**Windows**: Task Manager → Memory tab
**Linux**: `free -h`
**Mac**: `top`

**Solution**: Use smaller model or increase available RAM

### Slow Inference (30+ seconds per query)

**Normal on CPU**. Options to speed up:

1. Install GPU drivers for your graphics card
2. Switch to smaller model: `ollama pull neural-chat`
3. Reduce retrieval count: `top_k=2`
4. Use streaming responses

### Ollama Server Crashed

**Solution**: Restart service:
```bash
# Kill any Ollama processes, then restart
ollama serve
```

## Future Enhancements

- [ ] Fine-tune Mistral on invoice-specific data
- [ ] Add multi-language support
- [ ] Implement caching for repeated queries
- [ ] Add structured output extraction (JSON format)
- [ ] Deploy on cloud with GPU (AWS/GCP)
- [ ] Add web crawling for online invoice sources
- [ ] Implement document upload via UI
- [ ] Add export to CSV/Excel functionality
- [ ] Build REST API for external integrations

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## References

- [Ollama Documentation](https://ollama.ai)
- [Sentence Transformers](https://www.sbert.net/)
- [Chroma DB](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [RAG Fundamentals](https://docs.anthropic.com/en/docs/build-with-claude/retrieval)

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review troubleshooting section above

## Author

Built as a Gen AI learning project combining RPA expertise with modern LLM capabilities.

---

**Last Updated**: February 2026
