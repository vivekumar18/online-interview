import pdfplumber
import docx2txt

def extract_resume_text(file):

    text = ""

    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)

    return text.lower()


def extract_skills_section(text):

    lines = text.split("\n")

    skills = []
    capture = False

    for line in lines:

        # detect skills heading
        if "skills" in line:
            capture = True
            continue

        # stop if new section appears
        if capture and any(section in line for section in [
            "education","project","experience","summary","certification"
        ]):
            break

        if capture:
            skills.append(line.strip())

    return " ".join(skills)
def extract_projects_section(text):

    lines = text.split("\n")

    projects = []
    capture = False

    for line in lines:

        if "project" in line:
            capture = True
            continue

        if capture and any(x in line for x in ["education","skills","experience"]):
            break

        if capture:
            if line.strip() != "":
                projects.append(line.strip())

    return projects