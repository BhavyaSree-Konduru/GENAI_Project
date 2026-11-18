from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from config import *


def replace_source_documents(vectorstore, chunks, source):
    vectorstore.delete(where={"source": source})
    vectorstore.add_documents(chunks)


def ingest_pdf():
    if not PDF_PATH.is_file():
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    documents = PyPDFLoader(str(PDF_PATH)).load()
    for document in documents:
        document.metadata["source"] = SOURCE_PATH

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError(f"No text could be extracted from {PDF_PATH}")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=DB_PATH,
        embedding_function=embeddings,
    )

    # Replace this PDF's existing chunks so reruns also pick up document changes.
    replace_source_documents(vectorstore, chunks, SOURCE_PATH)
    print(f"Indexed {len(chunks)} chunks from {PDF_PATH.name}")


if __name__ == "__main__":
    ingest_pdf()
