import kagglehub
import pandas as pd
import os
import psycopg2

path = kagglehub.dataset_download("williamalabi/python-faq-chatgpt-gemini")
print("Path to dataset files:", path)

csv_file = None
for file in os.listdir(path):
    if file.endswith(".csv"):
        csv_file = os.path.join(path, file)
        break

print(csv_file)
if csv_file:
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    # for idx, row in df.iterrows():
    #     print(f"Q{idx + 1}: {row['Questions']}\nA{idx + 1}: {row['Answers']}\n{'-' * 80}")
else:
    print("❌ No CSV file found in the directory:", path)


conn = psycopg2.connect(
    dbname="faq_db",  # Nazwa bazy danych
    user="postgres",  # Użytkownik bazy danych
    password="postgres",  # Hasło do bazy danych
    host="localhost",  # Host bazy danych
    port="5432"        # Port, na którym działa PostgreSQL
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        id SERIAL PRIMARY KEY,
        question TEXT,
        answer TEXT
    );
""")

conn.commit()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO faq (question, answer) VALUES (%s, %s);
    """, (row['Questions'], row['Answers']))

conn.commit()

cursor.close()
conn.close()

print("✅ Dane zostały dodane do bazy danych!")
