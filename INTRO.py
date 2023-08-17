from tkinter import *
from PIL import Image, ImageTk
import threading
from pygame import mixer


class GifPlayer:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = Canvas(self.parent, width=1000, height=500)
        self.canvas.pack()
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
    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    root.geometry("1200x600")
    thread = threading.Thread(target=play_gif_thread, args=(root,))
    thread.start()