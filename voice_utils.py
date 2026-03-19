import pyttsx3
import speech_recognition as sr

def speak(text):

    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.setProperty('rate', 170)

    engine.say(text)
    engine.runAndWait()


def listen(status):

    r = sr.Recognizer()

    with sr.Microphone() as source:

        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except:
            return ""

    try:
        return r.recognize_google(audio).lower()
    except:
        return ""