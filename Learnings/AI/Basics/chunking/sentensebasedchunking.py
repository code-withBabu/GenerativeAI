#This script will explain the concept of sentence based chunking in text processing. Sentence based chunking is a method of splitting text into smaller pieces (chunks) based on sentences. This can be useful for various applications such as natural language processing, machine learning, and data analysis.
#Sentence based chunking

from langchain_classic.text_splitter import NLTKTextSplitter
import nltk
TextInput = "This is an example of sentence based chunking. We will split this text into chunks based on sentences."

# if nltk.data.find('tokenizers/punkt') is None:
#     nltk.download('punkt')
# else:
#     print("Punkt tokenizer is already available.")
import nltk
nltk.download('punkt_tab')

def sentence_based_chunking(text):
    text_splitter = NLTKTextSplitter(chunk_size = 100, chunk_overlap = 0)
    chunks = text_splitter.split_text(text)
    return chunks
totalchunks = sentence_based_chunking(TextInput)
print(f"Sentence Based Chunking: Total Chunks: {len(totalchunks)}")

for chunk in totalchunks:
    print(f"Chunk: {chunk}")