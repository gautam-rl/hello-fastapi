#!/usr/bin/env python

import os
import warnings

from dotenv import load_dotenv
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from rich import print

warnings.filterwarnings("ignore")

load_dotenv()

llm = ChatOpenAI(model="gpt-4-turbo")


def load_embeddings(path: str):
    return FAISS.load_local(
        path, embeddings=OpenAIEmbeddings(model="text-embedding-3-large")
    )


def embed_codebase():
    """
    Loads the codebase and returns the vector store.
    """
    # TODO If we have an existing vector store file, just load it.

    loader = GenericLoader.from_filesystem(
        "/Users/gautam/source/runloop/java/",
        glob="**/*",
        suffixes=[".java"],
        show_progress=True,
        parser=LanguageParser(language="java"),
    )
    docs = loader.load()

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector = FAISS.from_documents(docs, embeddings)
    vector.save_local("runloop_java.vectorstore")
    return vector


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def chat_with_codebase(vector):
    retriever = vector.as_retriever()
    template = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.

    {context}

    Question: {question}

    Helpful Answer:"""
    custom_rag_prompt = PromptTemplate.from_template(template)

    # rag_chain = (
    #     {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #     | custom_rag_prompt
    #     | llm
    #     | StrOutputParser()
    # )

    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    # rag_chain_with_source.invoke("What is Task Decomposition")


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
        
        # print(f" Answer: {rag_chain_with_source.invoke(question)}")


if __name__ == "__main__":
    # If runloop_java.vectorstore exists, just load it.
    if os.path.exists("runloop_java.vectorstore"):
        vector = load_embeddings("runloop_java.vectorstore")
    else:
        vector = embed_codebase()
    chat_with_codebase(vector)
