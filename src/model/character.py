
class Character:
    name: str
    image: str

    def __init__(self, name: str, image: str) -> None:
        self.name = name
        self.image = image

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name