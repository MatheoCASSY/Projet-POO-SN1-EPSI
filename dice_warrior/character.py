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
        self.xp = 0
        self.level = 1

    def __str__(self):
        return f"I'm {self.name} the {self.label}."

    def is_alive(self):
        return self.hp > 0

    def decrease_hp(self, amount):
        self.hp = max(0, self.hp - amount)
        self.show_healthbar()

    def show_healthbar(self):
        print(f"[{'❤️' * self.hp}{'♡' * (self.max_hp - self.hp)}] {self.hp}/{self.max_hp} hp")
        print("\n")

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 2
        self.hp = self.max_hp
        self.attack_value += 1
        self.defend_value += 1
        print(f"{self.name} leveled up! Now at level {self.level}!")

    def compute_damages(self, roll):
        return self.attack_value + roll

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(f"{self.name} [red]attack[/red] with {damages} damages ({self.attack_value} atk + {roll} rng)")
        target.defend(damages)
        self.gain_xp(2)

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
        self.gain_xp(2)

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

class Healer(Character):
    label = "healer"

    def heal(self, target):
        heal_amount = self.dice.roll() + 3
        target.hp = min(target.max_hp, target.hp + heal_amount)
        print(f"✨ {self.name} heals {target.name} for {heal_amount} HP!")

class Gamester(Character):
    label = "gamester"

    def gamble(self, target):
        gamble_value = self.dice.roll()
        print(f"🎲 {self.name} gambles and causes {gamble_value} random damage to {target.name}")
        target.decrease_hp(gamble_value)

if __name__ == "__main__":
    print("\n")

    char_1 = Warrior("James", 20, 8, 3, Dice("red", 6))
    char_2 = Mage("Elsa", 20, 8, 3, Dice("red", 6))
    char_3 = Thief("Robin", 18, 7, 2, Dice("red", 6))
    char_4 = Paladin("Arthur", 22, 7, 5, Dice("blue", 6))
    char_5 = Ranger("Lina", 19, 9, 2, Dice("green", 6))
    char_6 = Berserker("Grog", 25, 10, 1, Dice("red", 6))
    char_7 = Healer("Sophia", 18, 5, 4, Dice("yellow", 6))
    char_8 = Gamester("Jack", 19, 6, 3, Dice("purple", 6))

    characters = [char_1, char_2, char_3, char_4, char_5, char_6, char_7, char_8]

    for char in characters:
        print(char)

    while all(c.is_alive() for c in characters):
        for attacker, defender in zip(characters, characters[1:] + [characters[0]]):
            if attacker.is_alive() and defender.is_alive():
                attacker.attack(defender)
        char_7.heal(characters[0])
        char_8.gamble(characters[1])  
