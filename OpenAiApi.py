import requests
import os
from dotenv import load_dotenv
from searching_example import searching
from vector_comparing import vector_compare
from check_semantic_match_openai import semantic_match_openai

load_dotenv()

def ask_openai(prompt, model="gpt-4o-mini"):
    docs_scores = searching(prompt)

    context = "\n\n".join([doc.page_content for doc, _ in docs_scores])
    #print("Content from OpenAI: ", context)

    final_prompt = (
        "You are a helpful assistant. Using the context below, answer the question in a few sentences.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {prompt}\n"
        "Answer:"
    )
    
    url = "https://api.openai.com/v1/chat/completions"  
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}", 
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
        vector_similarity = vector_compare(context,reply)
        semantic_similarity = semantic_match_openai(context, reply)
        return reply, vector_similarity,semantic_similarity
    
    except Exception as e:
        return f"Error while querying OpenAI: {e}"
