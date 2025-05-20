from nltk.translate.bleu_score import sentence_bleu

def bleu(content, answer):
    references = [content.split()]  # poprawka tutaj
    candidate = answer.split()
    scoreBleu = sentence_bleu(references, candidate)
    return scoreBleu
