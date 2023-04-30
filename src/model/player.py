from src.model.character import Character


class Player:
    name: str
    score: int
    liked_characters: list[Character] = []
    disliked_characters: list[Character] = []

    def __init__(self, name: str, liked_characters=None, disliked_characters=None):
        if liked_characters is not None:
            self.liked_characters = liked_characters
        if disliked_characters is not None:
            self.disliked_characters = disliked_characters
        self.name = name
        self.score = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + " " + \
            str(self.score) + " " + \
            str(self.liked_characters) + " " + \
            str(self.disliked_characters)
