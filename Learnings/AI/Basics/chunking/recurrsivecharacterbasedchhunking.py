#this script will chunk the text based on recursive character-based splitting using LangChain's RecursiveCharacterTextSplitter

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Sample text to be chunked
text = """Natural language processing (NLP) is a subfield of artificial intelligence (AI) that focuses on the interaction between computers and humans through natural language. The ultimate goal of NLP is to enable computers to understand, interpret, and generate human language in a valuable way. NLP combines computational linguistics with machine learning, deep learning, statistical modeling, and more. It has a wide range of applications, including language translation, sentiment analysis, chatbots, and information retrieval.""" 

# Create an instance of the RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)

# Split the text into chunks
chunks = text_splitter.split_text(text)

# Print the resulting chunks
for i, chunk in enumerate(chunks):  
    print(f"Chunk {i+1}:\n{chunk}\n")   