import spacy

nlp = spacy.load("en_core_web_trf")

def evaluate_answer(answer):

    doc = nlp(answer)

    word_count = len(answer.split())

    score = min(word_count * 2, 100)

    feedback = "Good answer"

    if word_count < 10:
        feedback = "Answer is too short"

    if word_count > 40:
        feedback = "Very detailed answer"

    return score, feedback