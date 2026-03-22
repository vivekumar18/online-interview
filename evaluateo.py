def evaluate_answers(answers):

    score = 0

    for ans in answers:

        words = len(ans.split())

        if words > 5:
            score += 10
        else:
            score += 3

    total = len(answers) * 10

    percentage = (score / total) * 100

    if percentage > 60:
        result = "Selected"
    else:
        result = "Not Selected"

    return percentage, result