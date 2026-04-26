def score_answers(answers: str, skills: list):
    result = {}
    for skill in skills:
        result[skill] = {
            "score": 60,
            "level": "Intermediate"
        }
    return result