#!/usr/bin/env python

import warnings
from tempfile import TemporaryDirectory

from dotenv import load_dotenv
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

warnings.filterwarnings("ignore")
from pprint import pprint

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language

import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatOpenAI(model="gpt-4-turbo")


def load_codebase():
    """
    Loads the codebase and returns the vector store.
    """
    # TODO If we have an existing vector store file, just load it.

    loader = GenericLoader.from_filesystem(
        "/Users/gautam/source/runloop/java/src/main/java/ai/runloop/net/",
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

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    while True:
        question = input("Enter your question:")
        print(f" Answer: {rag_chain.invoke(question)}")


if __name__ == "__main__":
    # If runloop_java.vectorstore exists, just load it.
    if os.path.exists("runloop_java.vectorstore"):
    else:
        vector = load_codebase()
    chat_with_codebase(vector)
