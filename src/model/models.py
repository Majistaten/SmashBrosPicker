import json
import os
import tkinter as tk

from src.model.character import Character
from src.model.player import Player


class DataModel:
    RESOURCES = os.path.join(os.path.dirname(__file__), '..', 'resources')
    player_numbers: tk.IntVar
    dislike_scale: tk.IntVar
    like_scale: tk.IntVar
    players = {}
    characters = []
    settings = {}

    def __init__(self):
        self.characters = self.load_characters()

    def load_characters(self) -> list[Character]:
        with open(os.path.join(self.RESOURCES, "characters.json"), "r") as file:
            data = json.load(file)
            char_list = []
            for character in data["characters"]:
                char_list.append(Character(character["name"], character["image"]))
            return char_list

    def create_character_list(self, names: list[str]) -> list[Character]:
        char_list = []
        for name in names:
            for character in self.characters:
                if character.name == name:
                    char_list.append(character)
        return char_list

    def create_players(self, names: list[tk.StringVar]):
        for index, name in enumerate(names):
            if index < self.player_numbers.get():
                self.add_player(name)

    def add_player(self, name: tk.StringVar):
        player = Player(name.get())
        self.players[name] = player

    def add_disliked_character(self, name: tk.StringVar, character: Character):
        self.players[name].disliked_characters.append(character)

    def add_liked_character(self, name: tk.StringVar, character: Character):
        self.players[name].liked_characters.append(character)

    def init_settings(self):
        self.settings = {
            'liked_characters': tk.BooleanVar(value=False),
            'disliked_characters': tk.BooleanVar(value=False),
            'nerf_winner': tk.BooleanVar(value=True),
            'boost_loser': tk.BooleanVar(value=False),
        }
        self.player_numbers = tk.IntVar(value=2)
        self.dislike_scale = tk.IntVar(value=80)
        self.like_scale = tk.IntVar(value=80)

    def get_settings(self) -> dict:
        return self.settings

    def get_player_numbers(self) -> tk.IntVar:
        return self.player_numbers

    def get_dislike_scale(self) -> tk.IntVar:
        return self.dislike_scale

    def get_like_scale(self) -> tk.IntVar:
        return self.like_scale
