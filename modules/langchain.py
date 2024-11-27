from langchain_community.document_loaders import PyPDFLoader

def process_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    text = loader.load()

    print(text.document.page_content)

    return text