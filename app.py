import streamlit as st
import time
from report_generator import generate_report
from resume_parse import extract_resume_text, extract_skills_section, extract_projects_section
from questions_generator import generate_questions
from voice_utils import speak, listen
from evaluateo import evaluate_answers

# ----------- PAGE CONFIG -----------
st.set_page_config(page_title="Viku Interviewer", page_icon="🎤", layout="centered")

# ----------- SESSION STATE -----------
if "started" not in st.session_state:
    st.session_state.started = False

# ----------- UI STYLE -----------
st.markdown("""
<style>
body { background-color: #0f172a; }
.block-container { padding-top: 2rem; }

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #38bdf8;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.4);
}

.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    font-size: 18px;
    border-radius: 12px;
    padding: 12px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
st.markdown("<div class='title'>🎤 Viku Interview Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Resume-Based AI Interview System</div>", unsafe_allow_html=True)

st.write("")

# ----------- CARD -----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📄 Upload Your Resume", type=["pdf", "docx"])

    st.write("")

    # ✅ FIXED BUTTON (ONLY ONE BUTTON WITH KEY)
    start_btn = st.button("🚀 Start Interview", key="start_interview_btn")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- MAIN LOGIC -----------

if uploaded_file:
    st.success("✅ Resume uploaded successfully")

    resume_text = extract_resume_text(uploaded_file)
    skills_text = extract_skills_section(resume_text)
    projects = extract_projects_section(resume_text)

    if skills_text == "":
        st.error("❌ Skills section not detected in resume")
        st.stop()

    questions = generate_questions(skills_text, projects)
    status = st.empty()

    # -------- START BUTTON LOGIC --------
    if start_btn:
        st.session_state.started = True

    if st.session_state.started:
        st.info("Interview started... Please use your microphone 🎤")

        answers = []
        asked_questions = []

        # -------- INTRO --------
        speak("Hello. Welcome to the interview.")
        time.sleep(2)

        speak("Let's begin with a quick introduction.")
        time.sleep(2)

        first_q = "Can you please tell me about yourself?"
        speak(first_q)

        time.sleep(1)
        speak("You can answer now.")

        while True:
            status.info("🎤 Listening...")
            answer = listen(status)

            if answer == "":
                speak("I could not hear you clearly. Please try again.")
                continue

            if len(answer.split()) < 3:
                speak("Please give a complete answer.")
                continue

            break

        answers.append(answer)
        asked_questions.append(first_q)

        speak("Thank you. Let's continue.")

        # -------- QUESTIONS --------
        for question, level in questions:

            speak(question)
            time.sleep(1)
            speak("You can answer now.")

            while True:
                status.info("🎤 Listening...")
                answer = listen(status)

                if answer == "":
                    speak("Please speak clearly.")
                    continue

                if len(answer.split()) < 3:
                    speak("Please give a complete answer.")
                    continue

                if "repeat" in answer.lower():
                    speak("Repeating the question.")
                    speak(question)
                    continue

                break

            answers.append(answer)
            asked_questions.append(question)

            speak("Thank you. Moving to the next question.")

        speak("The interview is now complete.")

        # -------- RESULT --------
        percentage, result = evaluate_answers(answers)

        if result == "Selected":
            speak("Congratulations. You have been selected.")
        else:
            speak("Thank you for your time. You are not selected this time.")

        st.success(f"✅ Result: {result} ({percentage:.2f}%)")

        # -------- DOWNLOAD REPORT --------
        file = generate_report(asked_questions, answers)

        with open(file, "rb") as f:
            st.download_button(
                "📥 Download Interview Report",
                f,
                file_name="Interview_Report.pdf"
            )