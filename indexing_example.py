from embeddings_data_example import get_embeddings, create_index_postgres
from launching_data_from_psql_example import get_data_from_psql
import os

def indexing_example():
    print("Ingesting data from PostgreSQL...")
    data = get_data_from_psql()

    print("Generating embeddings...")
    docs, embeddings = get_embeddings(data)

    print("Persisting embeddings...")
    postgres_conn = os.getenv("POSTGRES_CONNECTION")

    if postgres_conn:
        db = create_index_postgres(docs, embeddings, postgres_conn)
    else:
        raise EnvironmentError("No vector store environment variables found.")
    print("Done.")
    print(db)


if __name__ == "__main__":
    indexing_example()