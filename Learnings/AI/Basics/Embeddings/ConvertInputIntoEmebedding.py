#import data file
from pypdf import PdfReader

def extract_text_from_pdf(pdfpath:str):
    try:      
         if not pdfpath:
            print("file path not found. please provide valid path")
            raise FileNotFoundError("Pdf file not Found")
         else:
             print(f"started processign the pdf : {pdfpath}")    
             pdfcontent = PdfReader(pdfpath)
             #Iterating through each page
             text = []
             i = 1
             for page in  pdfcontent.pages:
                 print(f"Started Extracting data from {i}")
                 text.append(page.extract_text())
                 i = i+1
         return text            
    except FileExistsError as e:
        print(f'exception message : {e}')

pdftext = extract_text_from_pdf("C:\\Users\\BabuR\\Documents\\AI-ML\\GenerativeAI\\RAG_Workflows\\Invoices\\invoices_rag\\documents\\invoice_001.pdf")
#print(pdftext)

#clean Text
import re


def clean_text(text):
    # Handle None, lists, or other types
    if isinstance(text, list):
        text = " ".join(text)  # flatten list to string
    if text is None:
        return ""
    text = str(text)  # convert anything else to string
    
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'Page \d+ of \d+', '', text)
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = text.strip()
    text = text.replace("\n","")
    return text

clean_text = clean_text(pdftext)
print(f"\n------------\n{clean_text}")
listtext = list(clean_text)

from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

def chunking(inputtext):
    print("starting chunking....")
    text_spllitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
    chunks = text_spllitter.split_text(inputtext)
    return chunks

totalchunks = chunking(clean_text)

print(len(totalchunks))
i = 0
for chunk in enumerate(totalchunks):
    print(f" chunk {i} : {chunk}")
    i = i+1

    
     