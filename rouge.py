from rouge_score import rouge_scorer

def rouge(context, answer):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scoresRouge = scorer.score(context, answer)
    return scoresRouge
