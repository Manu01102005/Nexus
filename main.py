import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import subprocess
import requests
import application
#from AppOpener import open, close appopener lib for windows


recognizer = sr.Recognizer()
engine = pyttsx3.init()
API_KEY="a681fc3f9e614a3c81adb219e7ba0e04"
'''f = open('todo.txt', 'r')
list=f.read().splitlines()'''


    
def speak(text):
    engine.say(text)
    engine.runAndWait() 
    
def processCommand(c):
    
    if "open google web" in c.lower():
        webbrowser.open("https://google.com")
    elif "open spotify web" in c.lower():
        webbrowser.open("https://spotify.com")
    elif "open youtube web" in c.lower():
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
            
    elif c.lower().startswith("launch"):
        o=c.lower().replace("launch", "").strip()
        a=application.app_name[o]
        subprocess.run(["open",a], check=True)
        
        
    elif "create to do list" in c.lower():
        print("Creating to do list")
        speak("Creating to do list")
        with sr.Microphone() as source:
            print("Speak task..i'm listening")
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=3)
            task= recognizer.recognize_google(audio)
            with open('todo.txt', 'a') as f:
                f.write(task)
                f.write("\n")
            with open('todo.txt', 'r') as f:
                s=f.read()
            print(s)
            speak(s)
            
            
            
    elif "show to do list" in c.lower():
        print("your to do list is:")
        speak("your to do list is")
        f = open('todo.txt', 'r')
        r=f.read()
        print(r)
        speak(r)

    elif "edit list" in c.lower():
        with sr.Microphone() as source:
            print("What would you like to remove from the list?")
            speak("What would you like to remove from the list?")
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=3)
            element= recognizer.recognize_google(audio)
            with open('todo.txt', 'r') as f:
                content=f.read()
            updated_content=content.replace(element,"")
            with open('todo.txt', 'w') as f:
                f.write(updated_content)
            print(element)
            speak("list edited")
        
        
    
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
     
        
