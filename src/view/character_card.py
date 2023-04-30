import os
import tkinter as tk
from pathlib import Path
from tkinter import PhotoImage

from src.model.character import Character

BG_COLOR = "#0D1117"
CARD_COLOR = "#282828"
HOVER_COLOR = "#3c3c3c"
CARD_SELECTED_COLOR = "#0D1117"


class CharacterCard(tk.Frame):
    IMAGES = os.path.join(os.path.dirname(__file__), '..', 'resources', 'smash-images')
    character: Character
    selected: bool
    label: tk.Label
    image: PhotoImage

    def __init__(self, master, character, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.character = character
        self.selected = False
        self["bg"] = BG_COLOR
        self.configure(highlightbackground=BG_COLOR, bg=BG_COLOR, highlightthickness=2, padx=5, pady=5)

        if Path(self.IMAGES + "/" + self.character.image_full).is_file():
            self.image = PhotoImage(file=self.IMAGES + "/" + self.character.image_full)
        else:
            self.image = PhotoImage(file=self.IMAGES + "/unknown100x100.png")

        self.label = tk.Label(self, image=self.image, bg=CARD_COLOR)
        self.label.pack()

        self.configure(borderwidth=0)

        self.label.bind("<Enter>", self.on_hover)
        self.label.bind("<Leave>", self.on_leave)
        self.label.bind("<Button-1>", self.on_click)

    def on_hover(self, event):
        if not self.selected:
            self.label.configure(bg=HOVER_COLOR)

    def on_leave(self, event):
        if not self.selected:
            self.label.configure(bg=CARD_COLOR)

    def on_click(self, event):
        self.selected = not self.selected
        if self.selected:
            self.configure(relief="solid", highlightbackground="blue", bg=CARD_SELECTED_COLOR)
        else:
            self.configure(relief="flat", highlightbackground=BG_COLOR, bg=CARD_COLOR)

    def reset(self):
        self.selected = False
        self.configure(relief="flat", highlightbackground=BG_COLOR, bg=CARD_COLOR)
