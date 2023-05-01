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


class ResultCard(tk.Frame):
    label: tk.Label

    def __init__(self, master, label_text: str, players: list[Player], *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.player_cards = {}
        self.selected_player = None

        self["bg"] = BG_COLOR
        self.label = tk.Label(self, text=label_text, bg=BG_COLOR, fg="white", font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=2, sticky=tk.EW)

        self.__generate_cards(players)

    def __generate_cards(self, players: list[Player]):
        for i, player in enumerate(players):
            card = self.PlayerCard(self, player)
            card.grid(row=i + 1, column=0, padx=5, pady=5)
            card.bind("<<OnClicked>>", self.set_player)
            self.player_cards[player.name] = card

    def set_player(self, event):
        for card in self.player_cards.values():
            if card.clicked:
                card.configure(relief="solid", highlightbackground="blue")
                self.selected_player = card.player
                card.clicked = False
                card.configure(bg=CARD_SELECTED_COLOR)
            else:
                card.configure(relief="flat", highlightbackground=BG_COLOR)

    def update_frame(self, selections: dict[str, Character]):
        for player_name, character in selections.items():
            self.player_cards[player_name].set_character(character)

    def get_selected_player(self) -> Player:
        return self.selected_player

    class PlayerCard(tk.Frame):
        character: Character
        player: Player
        label: tk.Label
        image: PhotoImage
        player_label: tk.Label

        def __init__(self, master, player: Player, character: Character = None, *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.character = character
            self.player = player
            self.clicked: bool = False

            self.configure(highlightbackground=BG_COLOR, bg=BG_COLOR, highlightthickness=2, padx=5, pady=5)

            self.__load_image()

            self.label = tk.Label(self, image=self.image, bg=BG_COLOR)
            self.player_label = tk.Label(self,
                                         text=player.name,
                                         bg=BG_COLOR,
                                         fg="white",
                                         font=("Arial", 20))
            self.player_label.pack(side=tk.TOP)
            self.label.pack(side=tk.BOTTOM)

            self.label.bind("<Button-1>", self.on_click)
            self.player_label.bind("<Button-1>", self.on_click)

        def on_click(self, event):
            self.clicked = True
            self.event_generate("<<OnClicked>>")

        def __load_image(self):
            if self.character is not None:
                if Path(IMAGES + "/" + self.character.image_stock).is_file():
                    self.image = PhotoImage(file=IMAGES + "/" + self.character.image_stock)
                else:
                    self.image = PhotoImage(file=IMAGES + "/unknown200x200.png")
            else:
                print("Character is None")
                self.image = PhotoImage(file=IMAGES + "/unknown200x200.png")

        def set_character(self, character: Character):
            self.character = character
            self.__load_image()
            self.__update_character_label()
            self.label.configure(image=self.image)

        def __update_character_label(self):
            self.player_label.configure(text=self.player.name)
