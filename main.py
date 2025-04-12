from ollama import ask_ollama

def main():
    prompt = "How can my code discover the name of an object?"
    answer = ask_ollama(prompt)
    print("Ollama:", answer)

if __name__ == "__main__":
    main()


# How to run
# ollama run DeepSeek-R1
# python main.py