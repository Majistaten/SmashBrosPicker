import os
import tkinter as tk
from pathlib import Path
from tkinter import PhotoImage

from src.model.character import Character

BG_COLOR = "#0D1117"
CARD_COLOR = "#282828"
HOVER_COLOR = "#3c3c3c"
CARD_SELECTED_COLOR = "#0D1117"
IMAGES = os.path.join(os.path.dirname(__file__), '..', 'resources', 'smash-images')


class SelectedCharacterCard(tk.Frame):
    character: Character
    label: tk.Label
    image: PhotoImage
    name_label: tk.Label

    def __init__(self, master, name:str, character: Character, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.character = character

        self.configure(highlightbackground=BG_COLOR, bg=BG_COLOR, highlightthickness=2, padx=5, pady=5)

        if Path(IMAGES + "/" + self.character.image_full).is_file():
            self.image = PhotoImage(file=IMAGES + "/" + self.character.image_full)
        else:
            self.image = PhotoImage(file=IMAGES + "/unknown100x100.png")

        self.label = tk.Label(self, image=self.image)
        self.name_label = tk.Label(self, text=name, bg=BG_COLOR, fg="white", font=("Arial", 20))
        self.name_label.pack(side=tk.TOP)
        self.label.pack(side=tk.BOTTOM)

        self.configure(borderwidth=0)