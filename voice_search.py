import speech_recognition as sr

def voice_to_text():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Speak Movie Name...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print(text)

        return text

    except:

        return ""