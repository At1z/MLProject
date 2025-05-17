from transformers import AutoTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_postgres import PGVector
from langchain_core.documents import Document

import os

EMBEDDING_MODEL = "thenlper/gte-large" # - Medium fast / great accuracy
#EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2" - fast / medium accuracy
#EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5" - slow / excellent accuracy 
#EMBEDDING_MODEL = "intfloat/e5-large-v2" - slow / excellent accuracy 


def get_embeddings(data):
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer,
        separators=["\n \n", "\n\n", "\n", " ", ""],
        chunk_size=512,
        chunk_overlap=0,
        ## to do sprawdzić jak to lepiej zrobić
    )

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    all_docs = []
    for item in data:
        text = f"Q: {item['question']} A: {item['answer']}"
        docs = text_splitter.split_text(text)
        all_docs.extend([Document(page_content=doc) for doc in docs])

    return all_docs, embeddings

def create_index_postgres(docs, embeddings, connection_string):
    print("creating with postgres")
    db = PGVector.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="doc_index",
        connection=connection_string
    )
    return db