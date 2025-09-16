import tkinter as tk
from hangman import hangman_words as words
class HangmanUi:
    def __init__(self):
        self.window=tk.Tk()
        self.window.title("Hangman")
        self.canvas=tk.Canvas(self.window,width=800,height=1000,bg="lavender blush")
        self.canvas.pack()
        self.button={}
        self.Message=None
        self.Image=None
        self.Heading=None
        self.photoimage=None
        self.topics=[]
        self.restart=tk.Button(text="Restart",fg="dark orchid",highlightthickness=0)
        self.create_buttons()
    def create_buttons(self):
        for key in words:
                self.button[key]=tk.Button(text=key,fg="dark orchid",highlightthickness=0,)
       
    def set_ui(self):
            if self.topics:
                for i in self.topics:
                    self.canvas.delete(i)
            if self.Heading is None:
                self.Heading=self.canvas.create_text(425,100,text="HANGMAN",fill="violet red",font=("Arial Rounded MT Bold",35))
            else:
                self.canvas.itemconfig(self.Heading,text="HANGMAN",fill="violet red",font=("Arial Rounded MT Bold",35))
            
            self.photoimage=tk.PhotoImage(file="./pic.png")
            if self.Image is None:
                self.Image=self.canvas.create_image(425,400,image=self.photoimage)
            else:
                self.canvas.itemconfig(self.Image,image=self.photoimage)
            rules=self.canvas.create_text(400,740,text="Hangman is a word-guessing game where player tries to guess it one letter at a time\n Each incorrect guess brings a stick-figure\n"
                   "'Hangman' closer to being fully drawn\nThe goal is to guess the word before the hangman is completed.\n",fill="medium orchid",font=("Apple Chancery",18),tag='rules')
            button=tk.Button(text="Click to Play!",fg="dark orchid",highlightthickness=0,command=self.display_topics)
            
            play_button=self.canvas.create_window(300,800,window=button,tag="play_button")
            restart_button=self.canvas.create_window(400,800,window=self.restart,tag="restart_button")
    def display_topics(self):
        
            self.canvas.delete("rules")
            self.topics.append(self.canvas.create_window(200,670,window=self.button['countries']))
            self.topics.append(self.canvas.create_window(280,670,window=self.button['foods']))
            self.topics.append(self.canvas.create_window(360,670,window=self.button['movies']))
            self.topics.append(self.canvas.create_window(440,670,window=self.button['animals']))
            self.topics.append(self.canvas.create_window(520,670,window=self.button['sports']))
            self.topics.append(self.canvas.create_window(600,670,window=self.button['fruits']))
            self.topics.append(self.canvas.create_window(680,670,window=self.button['colors']))
            self.topics.append(self.canvas.create_window(280,705,window=self.button['cities']))
            self.topics.append(self.canvas.create_window(370,705,window=self.button['celebrities']))
            self.topics.append(self.canvas.create_window(480,705,window=self.button['pokemon']))
            self.topics.append(self.canvas.create_window(560,705,window=self.button['cars']))
