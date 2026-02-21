#this script will chunk the text based on paragraph boundaries using LangChain's ParagraphTextSplitter
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

text = """
Artificial intelligence is transforming technology.
Machine learning models recognize patterns in data.

The Eiffel Tower is located in Paris, France.
It was built in 1889 by Gustave Eiffel.

Python is a popular programming language.
It is widely used for data science and AI.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n"]   # ← this makes it a paragraph chunker
)

chunks = splitter.split_text(text)

# Print the resulting chunks
for i, chunk in enumerate(chunks):  
    print(f"Chunk {i+1}:\n{chunk}\n")