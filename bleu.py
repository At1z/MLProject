from nltk.translate.bleu_score import sentence_bleu

def bleu(content, answer):
    references = [content.split()]  
    candidate = answer.split()
    scoreBleu = sentence_bleu(references, candidate)
    return scoreBleu

# Liczy ile n-gramów (np. 1-, 2-, 3-, 4-słowych sekwencji)