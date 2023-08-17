import datetime
import os
import sys
from bs4 import BeautifulSoup
import pyttsx3
import pyautogui
import requests
import speech_recognition
from tkinter import *
from INTRO import play_gif_thread
from PIL import Image, ImageTk
from pygame import mixer
from APIkey import api_data
import threading

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r=speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
      print("Listening...")
      r.pause_threshold = 1
      r.energy_threshold = 300
      audio = r.listen(source,0,4)

    try:
        print("Understanding...")
        query = r.recognize_google(audio,language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query
########################GUI###################
class GifPlayer:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = Canvas(self.parent, width=1350, height=750)
        self.canvas.pack()
        mixer.init()
        self.play_gif()

    def play_gif(self):
        self.gif = Image.open('jarvis.gif')
        self.gif_frames = []
        mixer.music.load('sound effects.mp3')
        mixer.music.play()  
        try:
            while True:
                self.gif_frames.append(ImageTk.PhotoImage(self.gif.copy()))
                self.gif.seek(len(self.gif_frames))
        
        except EOFError:
            pass

        self.idx = 0
        self.gif_len = len(self.gif_frames)
        self.anim = None
        self.update_frame()

    def update_frame(self):
        self.canvas.delete("all")
        frame = self.gif_frames[self.idx]
        self.canvas.create_image(0, 0, image=frame, anchor=NW)
        self.idx += 1
        if self.idx == self.gif_len:
            self.idx = 0
        self.anim = self.parent.after(50, self.update_frame)


def play_gif_thread(root):
    GifPlayer(root)

def new_func(root):
    play_gif_thread(root)

######################main loop#####################
if __name__ == "__main__":
    root = Tk()
    root.geometry("1350x750")
    new_func(root)

    def take_command():
        query = takeCommand().lower()
        if "wake up" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand().lower()
                if "take a rest" in query:
                    speak("Okay sir, You can call me anytime")
                    while True:
                        query = takeCommand().lower()
                        if "are you there" in query:
                            speak("Yes sir, I am always here for you")
                            break
                    
                elif "f*** you" in query:
                    speak('calm down sir')

                elif "sleep" in query:
                    speak("Terminating sir,Goodbye!")
                    root.destroy()
                    sys.exit()
                #######################TALKING NON SENSE WITH JARVIS##########################
                elif 'hey' in query:
                    from OPENAI import ANDRE
                    ANDRE(query)
                #######################Search###############################    
                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)
                #######################weather###############################
                elif "weather" in query:
                    search = "temperature in Bacoor, Cavite"
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")
                #######################Time###############################
                elif "time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")
                elif 'date' in query:
                    date = datetime.datetime.now().strftime('%A, %B %d, %Y')
                    speak(f'Today is {date}')
                #######################Controllers########################
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif 'play' in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                elif "next" in query:
                    pyautogui.press('shift'+'n')
                elif "full screen" in query:
                    pyautogui.press('f')
                    speak("Done sir, enjoy")
                elif 'escape' in query:
                    pyautogui.press('esc')
                    speak("escaping sir")
                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()
                ##########################OPEN AND CLOSE TAB OR APP####################
                elif "open" in query:
                    from Dictapp import openappweb
                    openappweb(query)
                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query) 
                ##########################PLAY GAME####################################
                elif "bonding" in query:
                    from game import game_play
                    game_play()  
                ######################SHUTDOWN OR RESTART SYSTEM#######################
                elif "shutdown" in query:
                    speak('shutting down in 5 second')
                    os.system("shutdown /s /t 1")

                elif "restart" in query:
                    speak('initiating restart in 5 second')
                    os.system("shutdown /r /t 1")

    def repeat_take_command():
        repeat_take_command_thread = threading.Thread(target=take_command)
        repeat_take_command_thread.start()

    root.after(1000, repeat_take_command)
    root.mainloop()           
