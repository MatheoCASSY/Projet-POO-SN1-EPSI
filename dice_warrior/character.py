from dice import Dice
from rich import print
from inventaire import Inventaire
from ui import print_healthbar, print_xpbar, print_level_up, print_stat_assignment, print_invalid_choice

class Character:
    label = "character"

    def __init__(self, name: str, max_hp: int, attack_value: int, defend_value: int, dice: Dice):
        """
        Initialise un personnage de base avec des valeurs par défaut pour xp, niveau, etc.
        """
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.dice = dice
        self.xp = 0
        self.level = 1
        self.xp_needed = 10
        self.inventory = Inventaire()

    def __str__(self) -> str:
        return f"I'm {self.name} the {self.label}."

    def is_alive(self):
        return self.hp > 0

    def decrease_hp(self, amount: int):
        self.hp = max(0, self.hp - amount)
        self.show_healthbar()

    def show_healthbar(self):
        print_healthbar(self)

    def show_xpbar(self):
        print_xpbar(self)

    def gain_xp(self, amount: int):
        self.xp += amount
        self.show_xpbar()
        if self.xp >= self.xp_needed:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_needed = self.level * 10
        print_level_up(self)
        self.allocate_stats()

    def allocate_stats(self):
        print_stat_assignment(self)
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
            print_invalid_choice()

    def compute_damages(self, roll: int) -> float:
        return self.attack_value + roll

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(f"{self.name} [red]attaque[/red] avec {damages} dommages ({self.attack_value} atk + {roll} rng)")
        target.defend(damages)
        self.gain_xp(2)

    def compute_defend(self, damages: int, roll: int) -> int:
        return max(0, damages - self.defend_value - roll)

    def defend(self, damages: int):
        roll = self.dice.roll()
        wounds = self.compute_defend(damages, roll)
        print(f"{self.name} [green]défend[/green] contre {damages} et prend {wounds} blessures ({damages} dmg - {self.defend_value} def - {roll} rng)")
        self.decrease_hp(wounds)

# Sous-classes spécifiques

class Warrior(Character):
    label = "warrior"

    def compute_damages(self, roll: int) -> float:
        print("🪓 Warrior bonus : +1,5 * dmg")
        return super().compute_damages(roll) + self.attack_value * 1.5

class Thief(Character):
    label = "thief"

    def compute_damages(self, roll: int) -> int:
        print("🗡️ Thief ability: Ignore la défense de la cible!")
        return self.attack_value + roll

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(f"{self.name} [red]attaque[/red] avec {damages} dommages (ignore la défense)")
        target.decrease_hp(damages)
        self.gain_xp(2)

class Paladin(Character):
    label = "paladin"

    def compute_defend(self, damages: int, roll: int) -> int:
        print("🛡️ Paladin blessing: +3 defense")
        return max(0, super().compute_defend(damages, roll) + 3)

class Ranger(Character):
    label = "ranger"

    def compute_damages(self, roll: int) -> int:
        print("🏹 Ranger precision: +2 damage")
        return super().compute_damages(roll) + 2

class Berserker(Character):
    label = "berserker"

    def compute_damages(self, roll: int) -> float:
        extra_damage = max(0, (self.max_hp - self.hp) // 5)
        print(f"🔥 Berserker fury: +{extra_damage} dmg based on missing HP")
        return super().compute_damages(roll) + extra_damage

class Healer(Character):
    label = "healer"

    def __init__(self, name: str, max_hp: int, attack_value: int, defend_value: int, dice: Dice, allies: list = None):
        super().__init__(name, max_hp, attack_value, defend_value, dice)
        self.allies = allies if allies is not None else []

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
        print(f"🎲 {self.name} gamble et inflige {gamble_value} dommages aléatoires à {target.name}")
        target.decrease_hp(gamble_value)
