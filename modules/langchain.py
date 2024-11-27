from langchain.document_loaders import PyPDFLoader

def process_pdf(pdf_binary):
    loader = PyPDFLoader(pdf_binary)
    text = loader.get_text()

    print(text)

    return text