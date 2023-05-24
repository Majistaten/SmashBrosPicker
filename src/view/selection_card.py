import os
import tkinter as tk
from pathlib import Path
from tkinter import PhotoImage

from src.model.character import Character
from src.model.player import Player

BG_COLOR = "#0D1117"
CARD_COLOR = "#282828"
HOVER_COLOR = "#3c3c3c"
CARD_SELECTED_COLOR = "#0D1117"
IMAGES = os.path.join(os.path.dirname(__file__), '..', 'resources', 'smash-images')


class SelectionCard(tk.Frame):
    character: Character
    player: Player
    label: tk.Label
    image: PhotoImage
    name_label: tk.Label
    character_label: tk.Label

    def __init__(self, master, player: Player, character: Character = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.character = character
        self.player = player

        self.configure(highlightbackground=BG_COLOR, bg=BG_COLOR, highlightthickness=2, padx=5, pady=5)

        self.__load_image()

        self.label = tk.Label(self, image=self.image, bg=BG_COLOR)
        self.name_label = tk.Label(self,
                                   text=player.name + " - score: " + str(player.score),
                                   bg=BG_COLOR,
                                   fg="white",
                                   font=("Arial", 20))
        self.name_label.pack(side=tk.TOP)
        self.character_label = tk.Label(self,
                                        text="Roll to get selection",
                                        bg=BG_COLOR,
                                        fg="white",
                                        font=("Arial", 20))
        self.character_label.pack(side=tk.TOP)
        self.label.pack(side=tk.BOTTOM)

        self.configure(borderwidth=0)

    def __load_image(self):
        if self.character is not None:
            if Path(IMAGES + "/" + self.character.image_full).is_file():
                self.image = PhotoImage(file=IMAGES + "/" + self.character.image_full)
            else:
                self.image = PhotoImage(file=IMAGES + "/unknown400x400.png")
        else:
            self.image = PhotoImage(file=IMAGES + "/unknown400x400.png")

    def set_character(self, character: Character):
        self.character = character
        self.__load_image()
        self.__update_player_score_label()
        self.__update_character_label()
        self.label.configure(image=self.image)

    def __update_player_score_label(self):
        self.name_label.configure(text=self.player.name + " - score: " + str(self.player.score))

    def __update_character_label(self):
        self.character_label.configure(text=self.character.name)
