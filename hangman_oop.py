import random
import tkinter as tk
from functools import partial
from tkinter import messagebox
from hangman import hangman_words as words
from hangman_ui import HangmanUi

MAX_LIVES = 13

class Hangman(HangmanUi):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.link_button()
        self.lives = MAX_LIVES
        self.guessed_string = ""
        self.user_guess = []
        self.Message = None
        self.restart.config(command=self.reset_game)

    def link_button(self):
        for key in self.button:
            self.button[key].config(command=lambda k=key: self.start_game(k))

    def start_game(self, key):
        # Confirm topic
        confirmation = messagebox.askyesno(
            title=key,
            message=f"You have entered the topic as {key}\nDo you want to proceed or change the topic?"
        )
        if not confirmation:
            return

        # Disable other topic buttons
        for k in self.button:
            self.button[k].config(state="disabled")
        self.canvas.itemconfig(self.Heading, text=key.title())

        # Pick a random word
        data = words[key]
        self.guess_word = random.choice(data)
        print(self.guess_word)  # for debugging

        # Reset lives and images
        self.lives = MAX_LIVES
        self.photoimage = tk.PhotoImage(file="./images/0.png")
        self.canvas.itemconfig(self.Image, image=self.photoimage)

        # Initialize guessed string
        self.guessed_string = "".join(["_" if ch != " " else " " for ch in self.guess_word])
        self.blanks = self.canvas.create_text(
            420, 760, text=" ".join(self.guessed_string),
            font=("Arial Rounded MT Bold", 35)
        )

        # Clear previous guesses
        self.user_guess = []
        self.Message = None

        # Bind keypress
        self.window.bind("<Key>", partial(self.on_press_key, key.title()))

    def on_press_key(self, topic, event):
        # Ignore first stray key after reset
        if getattr(self, "ignore_next_key", False):
            self.ignore_next_key = False
            return

        letter = event.char.lower()

        # Allow only letters or space
        if not (letter.isalpha() or letter == " "):
            return

        # Game over condition
        if self.lives == 0:
            self.window.unbind("<Key>")
            self.canvas.itemconfig(self.blanks, text=f"The actual word was {self.guess_word}")
            self.window.update()
            messagebox.showinfo(title="Game over", message="Oops! You ran out of lives.")
            self.ask_restart()
            return

        # Already guessed letter
        if letter in self.user_guess:
            if self.Message is None:
                self.Message = self.canvas.create_text(
                    420, 730,
                    text=f"'{letter}' has already been guessed!"
                )
            else:
                self.canvas.itemconfig(self.Message, text=f"'{letter}' has already been guessed!")
            return
        else:
            # Clear previous message
            if self.Message:
                self.canvas.itemconfig(self.Message, text="")

        # Add to guessed letters
        self.user_guess.append(letter)

        # Correct guess
        if letter in self.guess_word.lower():
            indices = [i for i, ch in enumerate(self.guess_word.lower()) if ch == letter]
            guessed_list = list(self.guessed_string)
            for i in indices:
                guessed_list[i] = self.guess_word[i]  # preserve original casing
            self.guessed_string = "".join(guessed_list)
            self.canvas.itemconfig(self.blanks, text=" ".join(self.guessed_string))
        else:
            # Wrong guess
            self.lives -= 1
            image_number = MAX_LIVES - self.lives - 1
            self.photoimage = tk.PhotoImage(file=f"./images/{image_number}.png")
            self.canvas.itemconfig(self.Image, image=self.photoimage)

        # Update heading
        self.canvas.itemconfig(
            self.Heading,
            text=f"{topic}\n{self.lives} Lives Left\nGuessed letters: {' '.join(self.user_guess)}"
        )

        # Win condition
        if self.guessed_string.lower() == self.guess_word.lower():
            self.window.unbind("<Key>")
            self.canvas.itemconfig(
                self.Heading,
                text=f"{topic}\nHurray! 🎉 You guessed it right! 🥳"
            )
            self.photoimage = tk.PhotoImage(file="./win.png")
            self.canvas.itemconfig(self.Image, image=self.photoimage)
            self.window.update()  # Force update before popup
            self.ask_restart()

    def ask_restart(self):
        restart_game = messagebox.askyesno(title="Restart", message="Do you want to start again?")
        if restart_game:
            self.reset_game()
        else:
            self.window.destroy()

    def reset_game(self):
        self.lives = MAX_LIVES
        self.user_guess = []
        self.guessed_string = ""
        self.ignore_next_key = True
        self.set_ui()
        if hasattr(self, "blanks"):
            self.canvas.itemconfig(self.blanks, text="")
        self.enable_other_topics()
        self.window.unbind("<Key>")

    def enable_other_topics(self):
        for key in self.button:
            self.button[key].config(state="normal")
