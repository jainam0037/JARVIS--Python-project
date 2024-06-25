import requests
import json
import pyttsx3  # type: ignore
import speech_recognition as sr  # type: ignore

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 3)  # this is the silence period it will wait for which is 3 seconds

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

def get_news_url(field):
    api_dict = {
        "business": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=e0820ff3735b456bbdf5415d5a985a60",
        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=e0820ff3735b456bbdf5415d5a985a60",
        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=e0820ff3735b456bbdf5415d5a985a60",
        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=e0820ff3735b456bbdf5415d5a985a60",
        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=e0820ff3735b456bbdf5415d5a985a60",
        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=e0820ff3735b456bbdf5415d5a985a60"
    }

    return api_dict.get(field.lower(), None)

def latestnews():
    speak("Which field news do you want? Business, Health, Technology, Sports, Entertainment, or Science")
    field = takeCommand().lower()
    url = get_news_url(field)
    
    if not url:
        speak("I couldn't understand the field you requested. Please try again.")
        return

    while True:
        news = requests.get(url).text
        news = json.loads(news)
        speak(f"Here is the news from the {field} field.")

        arts = news["articles"]
        for articles in arts:
            article = articles["title"]
            print(article)
            speak(article)
            news_url = articles["url"]
            print(f"For more info visit: {news_url}")

            speak("Do you want to hear more news? Say 'yes' to continue or 'stop' to end.")
            user_response = takeCommand().lower()

            if 'stop' in user_response:
                speak("That's all for now.")
                return
            elif 'yes' in user_response:
                speak("Do you want to continue with the current field or switch to a different field? Say 'continue' to proceed with more news from the current field or say the new field name to switch.")
                user_response = takeCommand().lower()
                if 'continue' in user_response:
                    continue
                else:
                    url = get_news_url(user_response)
                    if not url:
                        speak("I couldn't understand the field you requested. Please try again.")
                        return
                    else:
                        field = user_response
                        break  # Break the for loop to get news for the new field
