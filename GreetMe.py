import pyttsx3 # type: ignore
import speech_recognition as sr # type: ignore
import datetime

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[0].id)
engine.setProperty("rate", 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
    
    
def greetMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12: 
        speak("Good Morning!")
    elif hour >= 12 and hour <= 18:
        speak("Good Afternoon!")
    
    else:
        speak(" Good Evening!")
        
    
    speak("Please tell me, How can i help you?")
    