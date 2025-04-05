import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import PGVector

COLLECTION_NAME = "doc_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

load_dotenv()

def main():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    db = get_embed_db(embeddings)

    prompt = (
        "What is Python good for?"
    )

    print(f"Finding document matches for: '{prompt}'")
    docs_scores = db.similarity_search_with_score(prompt)

    for doc, score in docs_scores:
        print(f"\nSimilarity score (lower is better): {score}")
        print(f"Document content: {doc.page_content}")


def get_embed_db(embeddings):
    chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIR")
    postgres_conn = os.getenv("POSTGRES_CONNECTION")

    if postgres_conn:
        return get_postgres_db(embeddings, postgres_conn)
    elif chroma_persist_dir:
        return get_chroma_db(embeddings, chroma_persist_dir)
    else:
        raise EnvironmentError("No vector store environment variables found.")


def get_chroma_db(embeddings, persist_dir):
    db = Chroma(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=persist_dir,
    )
    return db


def get_postgres_db(embeddings, connection_string):
    db = PGVector(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        connection_string=connection_string,
    )
    return db


if __name__ == "__main__":
    main()
