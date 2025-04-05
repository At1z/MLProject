from embeddings_data_example import get_embeddings, create_index_postgres, create_index_chroma
from launching_data_from_psql_example import get_data_from_psql
import os

def indexing_example():
    print("Ingesting data from PostgreSQL...")
    data = get_data_from_psql()

    print("Generating embeddings...")
    docs, embeddings = get_embeddings(data)

    print("Persisting embeddings...")
    postgres_conn = os.getenv("POSTGRES_CONNECTION")
    chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIR")

    if postgres_conn:
        db = create_index_postgres(docs, embeddings, postgres_conn)
    elif chroma_persist_dir:
        db = create_index_chroma(docs, embeddings)
    else:
        raise EnvironmentError("No vector store environment variables found.")
    print("Done.")
    print(db)


if __name__ == "__main__":
    indexing_example()