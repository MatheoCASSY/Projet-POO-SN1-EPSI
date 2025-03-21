from dice import Dice


class Character:
    def __init__(self, name, max_hp, attack_value, defense_value, dice):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_value = attack_value
        self.defense_value = defense_value
        self.dice = dice

    #__str__

    def is_alive(self, hp):
        self.hp = hp
        return self.hp > 0

    def show_healthbar(self):
        print(f"[{self.hp * "o"}{" "*{self.max_hp - self.hp}}] {self.hp}/{self.max_hp}hp")


    def attack(self):
        print(f"Attack value: {self.attack_value + self.dice.roll()}")

    def defense(self):
        print(f"Defense value: {11 - self.defense_value - self.dice.roll()}")


if __name__ == "__main__":
    print("\n")

    char_1 = Character("James", 20, 8, 3, Dice("red", 6))
    char_2 = Character("Elsa", 20, 8, 3, Dice("red", 6))

    char_1.attack()
    char_1.defense()
    char_1.is_alive()