
class Character:
    name: str
    image_full: str
    image_small: str
    image_stock: str

    def __init__(self, name: str, image_full: str, image_small: str, image_stock) -> None:
        self.name = name
        self.image_full = image_full
        self.image_small = image_small
        self.image_stock = image_stock

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name
