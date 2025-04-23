import requests
import json
import os
from dotenv import load_dotenv
from searching_example import searching

# Load environment variables from .env file
load_dotenv()

def ask_openai(prompt, model="gpt-4o-mini"):  # You can change the model as needed
    docs_scores = searching(prompt)

    context = "\n\n".join([doc.page_content for doc, _ in docs_scores])
    #print("Content from OpenAI: ", context)

    # Prepare the prompt for OpenAI API
    final_prompt = (
        "You are a helpful assistant. Using the context below, answer the question in a few sentences.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {prompt}\n"
        "Answer:"
    )
    
    url = "https://api.openai.com/v1/chat/completions"  # OpenAI API endpoint
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",  # Get the API key from environment variable
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": final_prompt}],
        #"max_tokens": 150  # Adjust as needed
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        return reply
    except Exception as e:
        return f"Error while querying OpenAI: {e}"
