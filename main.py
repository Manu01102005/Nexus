import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import subprocess
import requests


recognizer = sr.Recognizer()
engine = pyttsx3.init()
API_KEY="a681fc3f9e614a3c81adb219e7ba0e04"

def speak(text):
    engine.say(text)
    engine.runAndWait() 
    
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song=c.lower().replace("play", "").strip()
        link=musiclibrary.music[song]
        webbrowser.open(link)
    elif "increase volume" in c.lower():
        # osascript to increase volume
        # This script increases the volume by a small increment
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
        speak("Volume increased.")
    elif "decrease volume" in c.lower():
        # osascript to decrease volume
        # This script decreases the volume by a small increment
        subprocess.run(["osascript", "-e", "set v olume output volume (output volume of (get volume settings) - 10)"])
        speak("Volume decreased.")
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}")
        print("API Status Code:", r.status_code)
        print("API Response:", r.json())
        if r.status_code==200:
            data=r.json()
            articles=data.get('articles',[])
            for article in articles:
                speak(article["title"])
                if articles:
                    for article in articles:
                        speak(article["title"])
                else:
                    speak("Sorry, I could not find any news headlines at the moment.")
        else:
            speak("I'm having trouble connecting to the news service.")
    
if __name__ == "__main__": 
    speak("Initializing jarvis...")
    while True:
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                # listen INSIDE the with block
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=1)  
            # once audio is captured, you can process it
            word = recognizer.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Ya")
                #listen for command
                with sr.Microphone() as source:
                    print("jarvis active ...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    
                    processCommand(command)
                    
        except Exception as e:
            print("Error: {0}".format(e)) 
        
        
        
