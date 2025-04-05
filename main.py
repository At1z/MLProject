from embeddings_data_example import get_embeddings
from launching_data_from_psql_example import get_data_from_psql


def main():
    print("Ingesting data from PostgreSQL...")
    data = get_data_from_psql()
    print("Generating embeddings...")
    #docs, embeddings = get_embeddings(data)

if __name__ == "__main__":
    main()