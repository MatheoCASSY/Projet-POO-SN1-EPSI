from dice import Dice


class Character:
    def __init__(self, name, max_hp, attack_value, defense_value, dice):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_value = attack_value
        self.defense_value = defense_value
        self.dice = dice

    # __str__

    def is_alive(self):
        pass

    def show_healthbar(self):
        pass
        # print
            # [oooooo              ] 6/14 hp

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
