from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_chroma import Chroma

from config import *

loader = PyPDFLoader(
    "data/genai_notes.pdf"
)

documents = loader.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

chunks = splitter.split_documents(
    documents
)
print("Total Chunks:", len(chunks))

for i in range(min(10, len(chunks))):

    print(f"\nChunk {i}")
    print("-"*50)

    print(chunks[i].page_content[:500])
    
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_PATH,
    embedding_function=embeddings
)

count = vectorstore._collection.count()

if count == 0:

    vectorstore.add_documents(chunks)

    print("PDF Indexed Successfully")

else:

    print("PDF Already Indexed")


print("Database Created Successfully")