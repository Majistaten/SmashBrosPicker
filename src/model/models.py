import json
import os
import tkinter as tk
import random

from src.model.character import Character
from src.model.player import Player

NORMAL_DECREASE = 30


class DataModel:
    RESOURCES = os.path.join(os.path.dirname(__file__), '..', 'resources')
    player_numbers: tk.IntVar
    dislike_scale: tk.IntVar
    like_scale: tk.IntVar
    players = []
    characters = []
    settings = {}
    winner: Player = None
    loser: Player = None

    def __init__(self):
        self.characters = self.load_characters()

    def load_characters(self) -> list[Character]:
        with open(os.path.join(self.RESOURCES, "characters.json"), "r") as file:
            data = json.load(file)
            char_list = []
            for character in data["characters"]:
                char_list.append(Character(character["name"],
                                           image_full=character["image_full"],
                                           image_small=character["image_small"],
                                           image_stock=character["image_stock"]))
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
        print(self.players)

    def add_player(self, name: tk.StringVar):
        player = Player(name.get())
        self.players.append(player)

    def add_disliked_characters(self, name: tk.StringVar, character: list[Character]):
        for player in self.players:
            if player.name == name.get():
                player.disliked_characters = character

    def add_liked_characters(self, name: tk.StringVar, character: list[Character]):
        for player in self.players:
            if player.name == name.get():
                player.liked_characters = character

    def init_settings(self):
        self.settings = {
            'liked_characters': tk.BooleanVar(value=True),
            'disliked_characters': tk.BooleanVar(value=True),
        }
        self.player_numbers = tk.IntVar(value=2)
        self.dislike_scale = tk.IntVar(value=80)
        self.like_scale = tk.IntVar(value=80)

    def pick_random_characters(self) -> dict[str, Character]:
        result = {}

        for player in self.players:
            random_value = random.randint(0, 100)
            selected_character = self.select_character_for_player(player, random_value)
            result[player.name] = selected_character

        return result

    def select_character_for_player(self, player, random_value: int) -> Character:
        if self.settings['liked_characters'].get() and self.player_numbers.get() > 1 and player is self.loser:
            return self.decide_liked(player, random_value)

        if self.settings['disliked_characters'].get() and self.player_numbers.get() > 1 and player is self.winner:
            return self.decide_disliked(player, random_value)

        if self.settings['liked_characters'].get() and random_value + NORMAL_DECREASE <= self.like_scale.get():
            print(f"{player.name} - random lucky")
            return random.choice(player.liked_characters)
        else:
            print(f"{player.name} - random normal")
            return random.choice(self.characters)

    def decide_disliked(self, player, random_value):
        if random_value <= self.dislike_scale.get():
            print(f"{player.name} - disliked")
            return random.choice(player.disliked_characters)
        else:
            print(f"{player.name} - normal")
            return random.choice(self.characters)

    def decide_liked(self, player, random_value):
        if random_value <= self.like_scale.get():
            print(f"{player.name} - liked")
            return random.choice(player.liked_characters)
        else:
            print(f"{player.name} - normal")
            return random.choice(self.characters)

    def set_winner(self, winner: Player | None):
        self.winner = winner
        if self.winner is not None:
            winner.score += 1
            print(f"Winner: {winner.name} with {winner.score} points")

    def set_loser(self, loser: Player | None):
        self.loser = loser
        if self.loser is not None:
            loser.score -= 1
            print(f"Loser: {loser.name}")

    def get_settings(self) -> dict:
        return self.settings

    def get_player_numbers(self) -> tk.IntVar:
        return self.player_numbers

    def get_dislike_scale(self) -> tk.IntVar:
        return self.dislike_scale

    def get_like_scale(self) -> tk.IntVar:
        return self.like_scale

    def get_players(self) -> list[Player]:
        return self.players

    def get_characters(self) -> list[Character]:
        return self.characters
