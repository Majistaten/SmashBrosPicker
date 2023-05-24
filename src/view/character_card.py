import os
import textwrap
import tkinter as tk
from pathlib import Path
from tkinter import PhotoImage

from src.model.character import Character

IMAGES = os.path.join(os.path.dirname(__file__), '..', 'resources', 'smash-images')
BG_COLOR = "#0D1117"
CARD_COLOR = "#282828"
HOVER_COLOR = "#3c3c3c"
CARD_SELECTED_COLOR = "#0D1117"


class CharacterCard(tk.Frame):
    character: Character
    selected: bool
    image: PhotoImage
    canvas: tk.Canvas

    def __init__(self, master, character: Character, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.character = character
        self.selected = False
        self["bg"] = BG_COLOR
        self.configure(highlightbackground=BG_COLOR, bg=BG_COLOR, highlightthickness=2, padx=5, pady=5)

        if Path(IMAGES + "/" + self.character.image_small).is_file():
            self.image = PhotoImage(file=IMAGES + "/" + self.character.image_small)
        else:
            print("Image not found: " + IMAGES + "/" + self.character.image_small)
            self.image = PhotoImage(file=IMAGES + "/unknown100x100.png")

        self.canvas = tk.Canvas(self,
                                bg=CARD_COLOR,
                                width=self.image.width(),
                                height=self.image.height(),
                                highlightthickness=0)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        wrapped_text = textwrap.wrap(self.character.name, width=10, break_long_words=False)
        y_position = 5
        for line in wrapped_text:
            self.canvas.create_text(5, y_position, anchor=tk.NW, text=line, fill="white", font=("Arial", 12, "bold"))
            y_position += 15
        self.canvas.pack()

        self.configure(borderwidth=0)

        self.canvas.bind("<Enter>", self.on_hover)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.on_click)

    def on_hover(self, event):
        if not self.selected:
            self.canvas.config(bg=HOVER_COLOR)

    def on_leave(self, event):
        if not self.selected:
            self.canvas.config(bg=CARD_COLOR)

    def on_click(self, event):
        self.selected = not self.selected
        if self.selected:
            self.configure(relief="solid", highlightbackground="blue", bg=CARD_SELECTED_COLOR)
        else:
            self.configure(relief="flat", highlightbackground=BG_COLOR, bg=CARD_COLOR)

    def reset(self):
        self.selected = False
        self.configure(relief="flat", highlightbackground=BG_COLOR, bg=CARD_COLOR)
