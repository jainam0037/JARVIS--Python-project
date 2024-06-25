import pyttsx3      # type: ignore
import speech_recognition as sr     # type: ignore
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim       # type: ignore
from geopy.exc import GeopyError        # type: ignore
import datetime
import geocoder     # type: ignore
import pytz
from timezonefinder import TimezoneFinder # type: ignore
import re
import os
import datetime 
import winsound
import MyAlarm
import pyautogui # type: ignore
import random
import MySpotify
from whatsapp_automation import init_whatsapp, send_message
from plyer import notification # type: ignore
from pygame import mixer # type: ignore
import speedtest # type: ignore
from googletrans import Translator # type: ignore
from gtts import gTTS # type: ignore
import pygame # type: ignore


engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[0].id)
engine.setProperty("rate", 170)

# Replace with your actual Spotify app credentials
spotify_player = MySpotify.SpotifyPlayer(client_id='ca0a5fcbb1474e7cbc5ce0eabde30225', client_secret='aa2e2915d1e543ec9ddb2636c8f002f3', redirect_uri='http://localhost:8888/callback')


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,3) # this is the silence period it will wait for which is 4 seconds

    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query



def get_weather(location):
    api_key = "43736a482802c2430ddaad0e16ae7259"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + location + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        temp_fahrenheit = (temperature * 9/5) + 32
        return temperature, temp_fahrenheit, data["name"]
    else:
        return None, None, None


def get_current_location_weather():
    try:
        g = geocoder.ip('me')
        lat, lon = g.latlng
        if lat is None or lon is None:
            raise ValueError("Unable to get the location coordinates.")
        api_key = "43736a482802c2430ddaad0e16ae7259"  # Replace with your OpenWeatherMap API key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + f"lat={lat}&lon={lon}&appid=" + api_key + "&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        if response.status_code == 200:
            main = data["main"]
            temperature = main["temp"]
            temp_fahrenheit = (temperature * 9/5) + 32
            location_name = data["name"]
            return temperature, temp_fahrenheit, location_name
        else:
            return None, None, None
    except Exception as e:
        speak("Unable to get current location.")
        return None, None, None
    
 
 
city_to_timezone = {
    "new york": "America/New_York",
    "mumbai": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    # Add more cities and their respective time zones here
}

def get_time_in_city(city_name):
    try:
        timezone = city_to_timezone[city_name.lower()]
        response = requests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        data = response.json()
        if 'datetime' in data:
            city_time = data['datetime'].split('T')[1].split('.')[0]
            return city_time
        else:
            return None
    except KeyError:
        speak("I couldn't find the time for that location.")
        return None
    except Exception as e:
        speak("An error occurred while fetching the time.")
        return None


def translate_text(text, target_lang):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    print(f"Original: {text}")
    print(f"Translated: {translated.text}")
    return translated.text

def speak_text(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_file = "translated_audio.mp3"
    tts.save(audio_file)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Properly close the pygame mixer
    pygame.mixer.music.unload()
    pygame.mixer.quit()
        

    # Remove the audio file
    try:
        os.remove(audio_file) # type: ignore
    except PermissionError:
        print("Failed to delete the audio file. It might still be in use.")


if __name__ == "__main__":
    
    

    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok sir , You can call anytime")
                    break 
                
                elif "hello" in query:
                    speak("Hello sir, how are you ?")
                elif "i am fine" in query:
                    speak("that's great, sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("you are welcome, sir")
                
                
                
                # elif "pause" in query:
                #     pyautogui.press("k")
                #     speak("video paused")
                # elif "play" in query:
                #     pyautogui.press("k")
                #     speak("video played")
                # elif "mute" in query:
                #     pyautogui.press("m")
                #     speak("video muted")

        
                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()
                    
                    
                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter") 
                
                elif "open" in query:
                    from Dictapp import openappweb
                    openappweb(query)
                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)
                
                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)
                elif "stackoverflow" in query or "stack overflow" in query:
                    from SearchNow import searchStackOverflow
                    searchStackOverflow(query)
                elif "gmail" in query or "mail" in query or "google email" in query:
                    from SearchNow import openGmail
                    openGmail()
                elif "instagram" in query:
                    from SearchNow import openInstagram
                    openInstagram()
                
                elif "news" in query:
                    from NewsRead import latestnews
                    latestnews()
                    
                # elif "search this address" in query:
                #     from SearchNow import searchAddress
                #     searchAddress()
                    
                    
                elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha
                    from Calculatenumbers import Calc
                    query = query.replace("calculate","")
                    query = query.replace("jarvis","")
                    Calc(query)
                
                elif "temperature" in query or "weather" in query:
                    if "in" in query:
                        location = query.split("in")[-1].strip()
                        temperature, temp_fahrenheit, location_name = get_weather(location)
                    else:
                        temperature, temp_fahrenheit, location_name = get_current_location_weather()

                    if temperature is not None and temp_fahrenheit is not None:
                        speak(f"The current temperature in {location_name} is {temperature} degrees Celsius and {temp_fahrenheit} degrees Fahrenheit")
                    else:
                        speak("I couldn't find the temperature for that location.")
                        
                elif "set an alarm" in query or "alarm" in query:
                    speak("Sir, please tell me the time to set an alarm. For example: set alarm to 5:30 am")
                    tt = takeCommand()
                    tt = tt.replace("set alarm to", "").replace("set alarm for", "").replace(".", "").strip()
                    tt = tt.upper()
                    import MyAlarm
                    MyAlarm.alarm(tt)
                    
                
                elif "the time" in query:
                    if "in" in query:
                        city_name = query.split("in")[-1].strip()
                        city_time = get_time_in_city(city_name)
                        if city_time is not None:
                            speak(f"The time in {city_name} is {city_time}")
                    else:
                        strTime = datetime.datetime.now().strftime("%H:%M")    
                        speak(f"Sir, the time is {strTime}")
                        
                        
                elif "finally sleep" in query:
                    speak("Going to sleep,sir")
                    exit()
                    
                    
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("jarvis","")
                    speak("You told me to"+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me to " + remember.read())
                    
                
                # Updated Spotify commands
                elif "play spotify" in query or "play music on spotify" in query:
                    spotify_player.play_random_song()
                    speak("Playing a random song from your Spotify library.")

                elif "stop spotify" in query or "stop music on spotify" in query:
                    spotify_player.stop_song()
                    speak("The music has been stopped.")
                    
                elif "schedule my day" in query:
                    tasks = [] #Empty list 
                    speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = takeCommand().lower()
                    if "yes" in query:
                        file = open("tasks.txt","w")
                        file.write(f"")
                        file.close()
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i = 0
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                    elif "no" in query:
                    
                        i = 0
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()


                if "translate" in query:
                    # Get the text to be translated
                    speak("Please say the text you want to translate")
                    text_to_translate = takeCommand()

                    if text_to_translate != "None":
                        # Get the target language
                        speak("Please say the target language")
                        target_language = takeCommand().lower()

                        # Map the spoken language to the language code
                        language_map = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 
                                        'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 
                                        'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 
                                        'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 
                                        'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 
                                        'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 
                                        'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 
                                        'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 
                                        'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 
                                        'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 
                                        'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 
                                        'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 
                                        'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 
                                        'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 
                                        'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 
                                        'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 
                                        'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 
                                        'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 
                                        'yoruba': 'yo', 'zulu': 'zu'}

                        if target_language in language_map:
                            target_lang_code = language_map[target_language]
                            translated_text = translate_text(text_to_translate, target_lang_code)
                            speak_text(translated_text, target_lang_code)
                        else:
                            speak("Sorry, I do not support this language.")

    
                if 'whatsapp' in query:
                    driver = init_whatsapp()
                    speak("What would you like to do? 'send message'.")
                    action = takeCommand()


                    if 'send message' in action:
                        speak("Who would you like to send a message to?")
                        contact_name = takeCommand()
                        speak("What is your message?")
                        message = takeCommand()
                        send_message(driver, contact_name, message)

                    else:
                        speak("I did not understand your command. Please try again.")

                elif "shutdown the system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        break
                
                elif "internet speed" in query:
                    try:
                        wifi = speedtest.Speedtest()
                        wifi.get_best_server()  # Optional: to select the best server
                        download_net = round(wifi.download() / 1048576, 2)  # Megabytes and rounded to 2 decimal places
                        upload_net = round(wifi.upload() / 1048576, 2)  # Megabytes and rounded to 2 decimal places
                        print(f"Wifi Download Speed is {download_net} Mbps")
                        print(f"Wifi Upload Speed is {upload_net} Mbps")
                        speak(f"Wifi download speed is {download_net} megabits per second")
                        speak(f"Wifi upload speed is {upload_net} megabits per second")
                    except Exception as e:
                        speak("Unable to check internet speed at the moment.")
                        print(f"Error: {e}")

                elif "screenshot" in query:
                     import pyautogui # type: ignore #pip install pyautogui
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")
                     
                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("enter")
                
                    
                
                elif "shutdown" in query:
                    os.system("shutdown /s /t 5")

                elif "sleep the system" in query:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")             
                elif 'exit' in query:
                    speak("Goodbye!")
                    break