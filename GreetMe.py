import pyttsx3
import datetime

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=11:
        speak("Good Morning Sir")
    
    elif hour>=12 and hour<=15:
        speak("Good Afternoon sir")
    
    else:
        speak("Good Evening sir")
    
    speak("Please tell me, How can I help you?")
