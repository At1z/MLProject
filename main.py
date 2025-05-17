from ollama import ask_ollama
from OpenAiApi import ask_openai
from vector_comparing import vector_compare

def main():
    prompt = "How can my code discover the name of an object?"
    
    # print("Question: ", prompt)
    # answer = ask_openai(prompt)
    # print("OpenAI answer:", answer)

    print("Question: ", prompt)
    answer = ask_ollama(prompt)
    print("Ollama answer:", answer)
    similarity = vector_compare(prompt,answer)
    print(f"Cosine similarity: {similarity:.4f}")

if __name__ == "__main__":
    main()


# How to run
# ollama run DeepSeek-R1
# python main.py