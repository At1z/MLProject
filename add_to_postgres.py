import pandas as pd
import psycopg2
import os

# Path to the additional CSV file
additional_csv_path = "extra_data.csv"  # 🔁 Replace with actual path

# Load the additional CSV file
if os.path.exists(additional_csv_path):
    df_additional = pd.read_csv(additional_csv_path, encoding='ISO-8859-1')
    print("📄 CSV loaded successfully!")
else:
    print("❌ CSV file not found:", additional_csv_path)
    exit()

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname="faq_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Insert new data into the faq table
    for _, row in df_additional.iterrows():
        cursor.execute("""
            INSERT INTO faq (question, answer) VALUES (%s, %s);
        """, (row['Questions'], row['Answers']))

    conn.commit()
    print("✅ Additional data added to the database!")

except Exception as e:
    print("❌ Error while connecting/inserting:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
