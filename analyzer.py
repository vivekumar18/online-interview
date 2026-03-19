def analyze_answer(answer):

    words = len(answer.split())

    if words < 10:
        score = 40
        feedback = "Answer is too short. Try explaining more."

    elif words < 30:
        score = 70
        feedback = "Good answer but can add more details."

    else:
        score = 90
        feedback = "Excellent detailed answer."

    return score, feedback