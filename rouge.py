from rouge_score import rouge_scorer

def rouge(context, answer):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scoresRouge = scorer.score(context, answer)
    return scoresRouge

# ROUGE-1: Liczy nakładające się pojedyncze słowa
# ROUGE-2: Liczy nakładające się pary słów (bigramy).
# ROUGE-L: Opiera się na najdłuższej wspólnej podsekwencji (LCS - Longest Common Subsequence).
# Chodzi o znalezienie najdłuższego ciągu słów, który pojawia się w obu tekstach w tej samej kolejności, ale niekoniecznie obok siebie.
