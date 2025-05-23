import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_postgres import PGVector

COLLECTION_NAME = "doc_index"
EMBEDDING_MODEL = "thenlper/gte-large" # - Medium fast / great accuracy
#EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2" - fast / medium accuracy
#EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5" - slow / excellent accuracy 
#EMBEDDING_MODEL = "intfloat/e5-large-v2" - slow / excellent accuracy 

load_dotenv()

def searching(prompt):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    db = get_embed_db(embeddings)

    # prompt = (
    #     "How can my code discover the name of an object?¶"
    # )

    # print(f"Finding document matches for: '{prompt}'")
    docs_scores = db.similarity_search_with_score(prompt, k=1)

    # for doc, score in docs_scores:
    #     print(f"\nSimilarity score (lower is better): {score}")
    #     print(f"Document content: {doc.page_content}")
    return docs_scores


def get_embed_db(embeddings):
    postgres_conn = os.getenv("POSTGRES_CONNECTION")

    if postgres_conn:
        return get_postgres_db(embeddings, postgres_conn)
    else:
        raise EnvironmentError("No vector store environment variables found.")


def get_postgres_db(embeddings, connection_string):

    db = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=connection_string
    )
    return db