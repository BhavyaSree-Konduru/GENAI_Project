from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

from config import *
from prompts import RAG_PROMPT


embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_PATH,
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": TOP_K}
)

llm = ChatOllama(
    model=LLM_MODEL
)


def get_answer(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(
        final_prompt
    )

    return {

    "answer": response.content,

    "sources": docs,

    "context": context
}