from reportlab.pdfgen import canvas

def generate_report(questions, answers):

    file_name = "interview_report.pdf"

    c = canvas.Canvas(file_name)

    y = 750

    c.drawString(200, 800, "AI Interview Report")

    for i in range(len(questions)):

        c.drawString(50, y, f"Q{i+1}: {questions[i]}")
        y -= 20

        c.drawString(70, y, f"Answer: {answers[i]}")
        y -= 40

    c.save()

    return file_name