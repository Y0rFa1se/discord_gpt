from langchain_community.document_loaders import PyPDFLoader

def process_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    document = loader.load()

    for page in document:
        text = page.page_content

    return text