import wolframalpha  # type: ignore
import pyttsx3  # type: ignore
import speech_recognition as sr  # type: ignore

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def WolfRamAlpha(query):
    apikey = "43A936-G3KV6XKK95"
    requester = wolframalpha.Client(apikey)
    requested = requester.query(query)

    try:
        answer = next(requested.results).text
        return answer
    except Exception as e:
        speak("I couldn't find the answer to that question.")
        return None

def Calc(query):
    Term = str(query)
    Term = Term.replace("jarvis", "")
    Term = Term.replace("multiply", "*")
    Term = Term.replace("plus", "+")
    Term = Term.replace("minus", "-")
    Term = Term.replace("divide", "/")
    Term = Term.replace("into", "*")
    Term = Term.replace("by", "/")
    Term = Term.replace("add", "+")
    Term = Term.replace("subtract", "-")
    Term = Term.replace("multiply", "*")
    Term = Term.replace("multiplied by", "*")
    Term = Term.replace("divided by", "/")
    Term = Term.replace("to the power of", "^")

    Final = str(Term)
    try:
        result = WolfRamAlpha(Final)
        if result:
            print(f"The answer is: {result}")
            speak(f"The answer is: {result}")
        else:
            speak("I couldn't calculate the answer.")
    except Exception as e:
        speak("I couldn't calculate the answer.")

