#This script will be explaining the concept of fixed size chunking in text processing. Fixed size chunking is a method of splitting text into smaller pieces (chunks) of a specific size. This can be useful for various applications such as natural language processing, machine learning, and data analysis.

#Fixed size chunking
from langchain_classic.text_splitter import CharacterTextSplitter
TextInput = "This is an example of fixed size chunking. We will split this text into chunks of a specific size."

def fixed_size_chunking(text, chunk_size):
    text_splitter = CharacterTextSplitter(separator=" ",chunk_size = chunk_size, chunk_overlap = 0)
    chunks = text_splitter.split_text(text)
    return chunks

totalchunks = fixed_size_chunking(TextInput, 10)
print(f"Fixed Size Chunking: Total Chunks: {len(totalchunks)}")

for chunk in totalchunks:
    print(f"Chunk: {chunk}")