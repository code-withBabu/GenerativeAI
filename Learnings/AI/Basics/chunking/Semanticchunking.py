#this script will chunk the text based on semantic meaning using the sentence transformer modelfrom sentence_transformers import SentenceTransformer

from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

text = """
Artificial intelligence is transforming the way we interact with technology. 
Machine learning models are trained on vast amounts of data to recognize patterns. 
Deep learning, a subset of machine learning, uses neural networks with many layers. 
These neural networks are inspired by the structure of the human brain. 
AI is being used in healthcare, finance, education, and many other industries.

The Eiffel Tower is one of the most iconic landmarks in the world. 
It is located in Paris, France, and was constructed between 1887 and 1889. 
The tower was designed by engineer Gustave Eiffel for the 1889 World's Fair. 
Standing at 330 meters tall, it was the tallest man-made structure for 41 years. 
Millions of tourists visit the Eiffel Tower every year, making it the most visited monument globally.

Python is one of the most popular programming languages in the world today. 
It is widely used for data science, web development, automation, and artificial intelligence. 
Python's simple and readable syntax makes it beginner-friendly and highly productive. 
Libraries like NumPy, Pandas, and Matplotlib make data analysis straightforward. 
Frameworks like Django and Flask are commonly used for building web applications in Python.

Climate change is one of the most pressing issues facing humanity today. 
Rising global temperatures are causing glaciers to melt and sea levels to rise. 
Extreme weather events such as hurricanes, droughts, and wildfires are becoming more frequent. 
Governments around the world are working to reduce carbon emissions and transition to renewable energy. 
Solar and wind energy are growing rapidly as affordable alternatives to fossil fuels.

LangChain is an open-source framework designed for building applications using large language models. 
It provides tools for chaining together prompts, memory, agents, and external data sources. 
RAG, or Retrieval Augmented Generation, combines document retrieval with LLM generation. 
Semantic chunking is a key step in RAG pipelines to ensure meaningful context is retrieved. 
Vector databases like Pinecone, Weaviate, and FAISS store embeddings for fast similarity search.
"""
# Free, runs locally on your machine
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text_splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile", breakpoint_threshold_amount=85)
chunks = text_splitter.split_text(text)

print(f"Total Chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}:\n{chunk}")