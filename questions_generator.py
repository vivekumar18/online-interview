import random

# -------- Clean Skills --------
def clean_skills(skills_text):

    skills = skills_text.replace("\n", ",").split(",")

    clean = []

    for skill in skills:
        skill = skill.strip()

        if len(skill) > 2 and skill.lower() not in clean:
            clean.append(skill)

    return clean


# -------- Skill-Based Questions --------
def generate_skill_questions(skills):

    templates = [
        "I noticed you have experience with {skill}. Can you walk me through how you used it in a project?",
        "Can you tell me about a real project where you applied {skill}?",
        "From your resume, I see {skill}. What challenges did you face while working with it?",
        "How comfortable are you with {skill}, and where have you used it practically?",
        "Can you explain one important concept of {skill} that you have implemented?"
    ]

    follow_up = [
        "That sounds interesting. Can you explain a bit more?",
        "Can you give a specific example?",
        "What was your role in that project?",
        "How did you solve that problem?"
    ]

    questions = []
    used = set()

    for skill in skills:

        if skill.lower() in ["and", "or", "with", "using", "skills"]:
            continue

        q = random.choice(templates).replace("{skill}", skill)

        if q not in used:
            questions.append((q, "medium"))
            used.add(q)

            # add follow-up
            questions.append((random.choice(follow_up), "easy"))

    return questions


# -------- Project-Based Questions --------
def generate_project_questions(projects):

    templates = [
        "Can you explain your {project} project?",
        "What was your role in the {project} project?",
        "What challenges did you face while working on {project}?",
        "What technologies did you use in {project}?",
        "What did you learn from your {project} project?"
    ]

    questions = []

    for proj in projects:

        if len(proj) > 3:

            q = random.choice(templates).replace("{project}", proj)

            questions.append((q, "medium"))

    return questions


# -------- Behavioral Questions --------
def generate_behavioral_questions():

    return [
        ("Tell me about yourself.", "easy"),
        ("What are your strengths and weaknesses?", "easy"),
        ("Describe a challenging situation you faced and how you handled it.", "medium"),
        ("Why do you want to work in this field?", "easy"),
        ("Where do you see yourself in the next 5 years?", "easy"),
        ("Can you describe a time when you worked in a team?", "medium"),
        ("How do you handle pressure or deadlines?", "medium")
    ]


# -------- MAIN FUNCTION --------
def generate_questions(skills_text, projects=None):

    skills = clean_skills(skills_text)

    questions = []

    # ✅ Behavioral FIRST (important)
    questions.extend(generate_behavioral_questions())

    # Skill-based
    questions.extend(generate_skill_questions(skills))

    # Project-based
    if projects:
        questions.extend(generate_project_questions(projects))

    return questions