import speech_recognition as sr # type: ignore
import pyttsx3 # type: ignore
import pywhatkit # type: ignore
import wikipedia # type: ignore
import webbrowser


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)
    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

query = takeCommand().lower()

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap # type: ignore
        query = query.replace("jarvis","")
        query = query.replace("google search","")
        query = query.replace("google","")
        speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query,1)
            speak(result)

        except:
            speak("No speakable output available")

def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!") 
        query = query.replace("youtube search","")
        query = query.replace("youtube","")
        query = query.replace("jarvis","")
        web  = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from wikipedia....")
        query = query.replace("wikipedia","")
        query = query.replace("search wikipedia","")
        query = query.replace("jarvis","")
        results = wikipedia.summary(query,sentences = 2)
        speak("According to wikipedia..")
        print(results)
        speak(results)
        
        
        
        
def searchStackOverflow(query):
    if "stackoverflow" in query or "stack overflow" in query:
        speak("Searching Stack Overflow...")
        query = query.replace("search stackoverflow", "")
        query = query.replace("search stack overflow", "")
        query = query.replace("stackoverflow", "")
        query = query.replace("stack overflow", "")
        query = query.replace("jarvis", "")
        web = "https://stackoverflow.com/search?q=" + query
        webbrowser.open(web)
        speak("This is what I found for your search on Stack Overflow!")

def openGmail():
    speak("Opening Gmail...")
    web = "https://mail.google.com/mail/u/2/#inbox"
    webbrowser.open(web)
    speak("Gmail is opened for you, Sir")
    
    
def openInstagram():
        speak("Opening Instagram...") 
        web  = "https://www.instagram.com/"
        webbrowser.open(web)
        speak("Done, Sir")
        
        
# def searchAddress():
#     speak("Searching for addresses...")
#     address = query.replace("search this address", "").strip()
#     webbrowser.open(f"https://www.google.com/maps/search/{address}")
#     speak(f"Searching for {address} on Google Maps")