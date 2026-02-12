#This workflow will extract the text from the invoice and return it as a string.

from pathlib import Path
import pdfplumber
import os

# This function takes a path to a directory containing PDF files, extracts the text from each PDF, and returns a list of dictionaries with the filename and extracted text.
def extract_text_from_pdf(document_path):
    extracted_data = []
    for pdffile in Path(document_path).glob('*.pdf'):
        print(f"Extracting text from {pdffile}...")

        try:
            with pdfplumber.open(pdffile) as pdf:
                full_text = ''
                for page in pdf.pages:
                    full_text += page.extract_text() + '\n'
                extracted_data.append({
                    "filename": pdffile.name,
                    "text": full_text
                })
                print(f"✓ Extracted {len(full_text)} characters")
        except Exception as e:
            print(f"Error processing {pdffile}: {e}")                                                   
    return extracted_data

if __name__ == "__main__":     
      #get testdata directory
      current_dir = os.path.dirname(os.path.abspath(__file__))
      pdffolderpath = os.path.join(current_dir, 'documents')
      print(f"Current directory: {current_dir}")
      extracted_invoices = extract_text_from_pdf(pdffolderpath)
      print(f"\nSuccessfully extracted {len(extracted_invoices)} documents")
    
      # Print first 500 characters to see what you're working with
      if extracted_invoices:
        print("\nSample text from first document:")
        print(extracted_invoices[0]["text"][:500])