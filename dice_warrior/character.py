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

    def show_xpbar(self):
        percent = int((self.xp / self.xp_needed) * 20)  
        print(f"XP: [{'★' * percent}{'✩' * (20 - percent)}] {self.xp}/{self.xp_needed} xp")
    def gain_xp(self, amount):
        self.xp += amount
        self.show_xpbar()
        if self.xp >= self.xp_needed:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_needed = self.level * 10
        print(f"\n🎉 {self.name} monte au niveau {self.level} ! 🎉")
        self.show_xpbar()
        self.allocate_stats()

    def allocate_stats(self):
        print("\n📊 Attribuez vos points de stats :")
        options = ["1. +5 HP max", "2. +2 ATK", "3. +2 DEF"]
        for opt in options:
            print(opt)

        choice = input("Choisissez une amélioration (1/2/3) >>> ")
        if choice == "1":
            self.max_hp += 5
            self.hp += 5
            print(f"❤️ {self.name} gagne +5 HP max !")
        elif choice == "2":
            self.attack_value += 2
            print(f"🔫 {self.name} gagne +2 en ATK !")
        elif choice == "3":
            self.defend_value += 2
            print(f"🛡️ {self.name} gagne +2 en DEF !")
        else:
            print("❌ Choix invalide, aucun bonus attribué.")

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
        print("🪓 Warrior bonus : + 1,5 * dmg")
        return super().compute_damages(roll) + self.attack_value * 1.5

class Mage(Character):
    label = "mage"
    def compute_defend(self, damages, roll):
        wounds = super().compute_defend(damages, roll) - self.defend_value * 0.75
        print("🔮 Mage bonus : -3 wounds")
        return max(0, int(wounds))

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

    def __init__(self, name, max_hp, attack_value, defend_value, dice, characters):
        super().__init__(name, max_hp, attack_value, defend_value, dice)
        self.allies = [char for char in characters if char is not self]

    def heal(self, target):
        roll = self.dice.roll()
        heal_amount = 0
        print("⚕️ Healer utilise son pouvoir de soin !")

        if roll < self.dice.faces * 0.1:
            print("❌ Échec du soin !")
        elif self.dice.faces * 0.1 <= roll < self.dice.faces * 0.25:
            heal_amount = self.attack_value // 4
        elif self.dice.faces * 0.25 <= roll < self.dice.faces * 0.5:
            heal_amount = self.attack_value // 2
        elif self.dice.faces * 0.5 <= roll < self.dice.faces * 0.99:
            heal_amount = (self.attack_value * 3) // 4
        elif roll == self.dice.faces:
            heal_amount = self.attack_value

        if heal_amount > 0:
            print(f"✨ {target.name} récupère {heal_amount} HP !")
            target.hp = min(target.max_hp, target.hp + heal_amount)
            target.show_healthbar()

    def attack(self, target):
        action = input("Voulez-vous attaquer (A) ou soigner (S) ? >>> ").lower()

        if action == "s":
            print("\n📜 Liste des alliés :")
            for i, ally in enumerate(self.allies):
                print(f"{i + 1}. {ally.name} ({ally.hp}/{ally.max_hp} HP)")

            choice = input("Entrez le numéro de l'allié à soigner ou 'M' pour vous soigner vous-même >>> ").lower()

            if choice == "m":
                self.heal(self)
            else:
                try:
                    ally_index = int(choice) - 1
                    if 0 <= ally_index < len(self.allies):
                        self.heal(self.allies[ally_index])
                    else:
                        print("⚠️ Choix invalide !")
                except ValueError:
                    print("⚠️ Entrée non valide !")
        else:
            super().attack(target)

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
