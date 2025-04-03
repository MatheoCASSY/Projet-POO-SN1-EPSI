import random

class Dice:
    def __init__(self, color: str, faces: int):
        self.color = color
        self.faces = faces

    def __str__(self) -> str:
        return f"I'm {self.color} a dice with {self.faces} faces"

    def __eq__(self, another_dice) -> bool:
        return self.faces == another_dice.faces

    def roll(self) -> int:
        return random.randint(1, self.faces)

class RiggedDice(Dice):
    def roll(self) -> int:
        return self.faces
