from dice import Dice
from rich import print


class Character:
    label = "character"

    def __init__(self, name, max_hp, attack_value, defend_value, dice, level=1):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.dice = dice
        self.level = level
        self.xp = 0
        self.xp_needed = self.level * 10  # XP nécessaire pour monter de niveau

    def __str__(self):
        return f"I'm {self.name} the {self.label}. I am level {self.level}"

    def is_alive(self):
        return self.hp > 0

    def decrease_hp(self, amount):
        self.hp = max(0, int(self.hp - amount))
        self.show_healthbar()

    def show_healthbar(self):
        print(f"[{'❤️' * self.hp}{'♡' * (self.max_hp - self.hp)}] {self.hp}/{self.max_hp} hp")

    def show_xpbar(self):
        percent = int((self.xp / self.xp_needed) * 20)  
        print(f"XP: [{'★' * percent}{'✩' * (20 - percent)}] {self.xp}/{self.xp_needed} xp")

    def compute_damages(self, roll):
        return self.attack_value + roll

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(f"{self.name} [red]attack[/red] with {damages} damages ({self.attack_value} atk + {roll} rng)")
        target.defend(damages)
        self.gain_xp(damages)

    def compute_defend(self, damages, roll):
        return max(0, damages - self.defend_value - roll)

    def defend(self, damages):
        roll = self.dice.roll()
        wounds = self.compute_defend(damages, roll)
        print(f"{self.name} [green]defend[/green] against {damages} and take {wounds} wounds")
        self.decrease_hp(wounds)

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
            print(f"🗡 {self.name} gagne +2 en ATK !")
        elif choice == "3":
            self.defend_value += 2
            print(f"🛡 {self.name} gagne +2 en DEF !")
        else:
            print("❌ Choix invalide, aucun bonus attribué.")


class Warrior(Character):
    label = "warrior"

    def compute_damages(self, roll):
        print("🪓 Warrior bonus : +1,5 fois ses dmg")
        return super().compute_damages(roll) + self.attack_value * 1.5



class Mage(Character):
    label = "mage"

    def compute_defend(self, damages, roll):
        wounds = super().compute_defend(damages, roll) - self.defend_value * 0.75
        print("🔮 Mage bonus : -3 wounds")
        return max(0, int(wounds))


class Thief(Character):
    label = "thief"

    def compute_defend(self, damages, roll):
        print("🗡️ Thief bonus: ignore l'armure de l'ennemi !")
        wounds = max(0, damages - roll)
        return int(wounds)


class Gamester(Character):
    label = "gamester"

    def compute_damages(self, roll):
        print("🎲 Gamester bonus: reroll dice ")

        this_roll = super().compute_damages(roll)
        r = input(f"Votre roll d'attaque est de {this_roll}. Si vous voulez le modifier, pressez X >>> ")
        if r.lower() == "x":
            roll = self.dice.roll()
            print(f"🎲 Nouveau roll: {roll}")
            return super().compute_damages(roll)


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


if __name__ == "__main__":
    char_1 = Thief("James", 20, 8, 3, Dice("red", 6), 1)
    char_2 = Mage("Elsa", 20, 8, 3, Dice("red", 6), 1)

    print(char_1)
    print(char_2)

    char_1.attack(char_2)
