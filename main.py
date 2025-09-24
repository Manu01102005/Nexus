import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import subprocess
import requests
import application
import pyaudio
import struct
#from AppOpener import open, close; appopener lib for windows
import pvporcupine
porcupine = pvporcupine.create(
  access_key='ENTER YOUR OWN API KEY',
  keyword_paths=['Nexus_en_mac_v3_0_0.ppn']
)
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)


recognizer = sr.Recognizer()
engine = pyttsx3.init()
API_KEY="ENTER YOUR OWN API KEY"



    
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
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
        speak("Volume increased")
    elif "decrease volume" in c.lower():
        subprocess.run(["osascript", "-e", "set v olume output volume (output volume of (get volume settings) - 10)"])
        speak("Volume decreased")
        
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
    speak("Initializing Nexus. I am ready to listen.")
    print("Listening...")
    while True:
        try:
            # Process audio stream for wake word detection
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)

            if result >= 0:
                print("Yes!")
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, phrase_time_limit=5)
                try:
                    command = recognizer.recognize_google(audio)
                    print(f"Command received: {command}")
                    processCommand(command)
                    
                except sr.UnknownValueError:
                    speak("Sorry, I did not understand that.")
                except Exception as e:
                    speak("An unexpected error occurred.")
                    print(f"Error: {e}")
                finally:
                    # Loop back to listening for the wake word
                    print("Listening...")
        except KeyboardInterrupt:
            print("Stopping Nexus...")
            
            
     
