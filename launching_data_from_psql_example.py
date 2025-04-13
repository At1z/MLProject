import psycopg2
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_postgres import PGVector
from dotenv import load_dotenv

load_dotenv()


POSTGRES_CONNECTION = os.getenv("POSTGRES_CONNECTION")

def get_data_from_psql():
    conn = psycopg2.connect(POSTGRES_CONNECTION)
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM faq")

    rows = cursor.fetchall()
    data = [{"question": row[0], "answer": row[1]} for row in rows]

    cursor.close()
    conn.close()
    return data