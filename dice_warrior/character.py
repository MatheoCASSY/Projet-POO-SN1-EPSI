from dice import Dice
from rich import print

class Character:
    label = "character"

    def __init__(self, name, max_hp, attack_value, defend_value, dice):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.dice = dice

    def __str__(self):
        return f"I'm {self.name} the {self.label}."

    def is_alive(self):
        return self.hp > 0

    def decrease_hp(self, amount):
        self.hp = max(0, self.hp - amount)
        self.show_healthbar()

    def show_healthbar(self):
        print(f"[{'❤️' * self.hp}{'♡' * (self.max_hp - self.hp)}] {self.hp}/{self.max_hp} hp")

    def compute_damages(self, roll):
        return self.attack_value + roll

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(f"{self.name} [red]attack[/red] with {damages} damages ({self.attack_value} atk + {roll} rng)")
        target.defend(damages)

    def compute_defend(self, damages, roll):
        return max(0, damages - self.defend_value - roll)

    def defend(self, damages):
        roll = self.dice.roll()
        wounds = self.compute_defend(damages, roll)
        print(f"{self.name} [green]defend[/green] against {damages} and take {wounds} wounds ({damages} dmg - {self.defend_value} def - {roll} rng)")
        self.decrease_hp(wounds)

class Warrior(Character):
    label = "warrior"

    def compute_damages(self, roll):
        print("🪓 Warrior bonus: +3 dmg")
        return super().compute_damages(roll) + 3

class Mage(Character):
    label = "mage"

    def compute_defend(self, damages, roll):
        print("🔮 Mage bonus: -3 wounds")
        return max(0, super().compute_defend(damages, roll) - 3)

class Thief(Character):
    label = "thief"

    def compute_damages(self, roll):
        print("🗡️ Thief ability: Ignores target defense!")
        return self.attack_value + roll

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(f"{self.name} [red]attack[/red] with {damages} damages ({self.attack_value} atk + {roll} rng, ignores defense)")
        target.decrease_hp(damages)

class Paladin(Character):
    label = "paladin"

    def compute_defend(self, damages, roll):
        print("🛡️ Paladin blessing: +3 defense")
        return max(0, super().compute_defend(damages, roll) + 3)

class Ranger(Character):
    label = "ranger"

    def compute_damages(self, roll):
        print("🏹 Ranger precision: +2 damage")
        return super().compute_damages(roll) + 2

class Berserker(Character):
    label = "berserker"

    def compute_damages(self, roll):
        extra_damage = max(0, (self.max_hp - self.hp) // 5)
        print(f"🔥 Berserker fury: +{extra_damage} dmg based on missing HP")
        return super().compute_damages(roll) + extra_damage

if __name__ == "__main__":
    print("\n")

    char_1 = Warrior("James", 20, 8, 3, Dice("red", 6))
    char_2 = Mage("Elsa", 20, 8, 3, Dice("red", 6))
    char_3 = Thief("Robin", 18, 7, 2, Dice("red", 6))
    char_4 = Paladin("Arthur", 22, 7, 5, Dice("blue", 6))
    char_5 = Ranger("Lina", 19, 9, 2, Dice("green", 6))
    char_6 = Berserker("Grog", 25, 10, 1, Dice("red", 6))

    print(char_1)
    print(char_2)
    print(char_3)
    print(char_4)
    print(char_5)
    print(char_6)

    char_1.attack(char_2)
    char_3.attack(char_1)
    char_5.attack(char_6)
    char_6.attack(char_4)

    # test combat en boucle
while char_1.is_alive() and char_2.is_alive() and char_3.is_alive() and char_4.is_alive() and char_5.is_alive() and char_6.is_alive():
    char_1.attack(char_2)
    char_2.attack(char_3)
    char_3.attack(char_4)
    char_4.attack(char_5)
    char_5.attack(char_6)
    char_6.attack(char_1)
