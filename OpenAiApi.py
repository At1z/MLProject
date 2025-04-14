import openai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def api_caller():


    print("DEBUG: API_KEY =", os.getenv("API_KEY")) 
    openai.api_key = API_KEY

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Opowiedz dowcip o programistach."}
    ]
    )

    print(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    api_caller()