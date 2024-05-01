#!/usr/bin/env python

import os
import warnings

from dotenv import load_dotenv
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from rich import print

warnings.filterwarnings("ignore")

load_dotenv()

llm = ChatOpenAI(model="gpt-4-turbo")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
VECTOR_STORE_PATH = "runloop_java.vectorstore"


def load_vector_store(path: str):
    return FAISS.load_local(path, embeddings=embeddings)


def embed_codebase(sources_path="/Users/gautam/source/runloop/java/"):
    """
    Loads the codebase and returns the vector store.
    """
    # TODO If we have an existing vector store file, just load it.

    loader = GenericLoader.from_filesystem(
        sources_path,
        glob="**/*",
        suffixes=[".java"],
        show_progress=True,
        parser=LanguageParser(language="java"),
    )
    docs = loader.load()

    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)
    return vector_store


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def chat_with_codebase(vector_store):
    retriever = vector_store.as_retriever()
    template = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.

    {context}

    Question: {question}

    Helpful Answer:"""
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    # Question/answer loop.
    # TODO - save/clear history
    while True:
        question = input("Enter your question:")
        output = {}
        curr_key = None
        for chunk in rag_chain_with_source.stream(question):
            for key in chunk:
                if key not in output:
                    output[key] = chunk[key]
                else:
                    output[key] += chunk[key]
                if key != curr_key:
                    print(f"\n\n{key}: {chunk[key]}", end="", flush=True)
                else:
                    print(chunk[key], end="", flush=True)
                curr_key = key
        print("\n")


if __name__ == "__main__":
    # If runloop_java.vectorstore exists, just load it.
    if os.path.exists(VECTOR_STORE_PATH):
        vector_store = load_vector_store(VECTOR_STORE_PATH)
    else:
        vector_store = embed_codebase()

    chat_with_codebase(vector_store)
