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
            print(
                f"[{"❤️" * self.hp}{"♡" * (self.max_hp - self.hp)}] {self.hp}/{self.max_hp} hp")

    def compute_damages(self, roll):
        damages = self.attack_value + roll
        return damages

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(
            f"{self.name} [red]attack[/red] with {damages} damages ({self.attack_value} atk + {roll} rng)")
        target.defend(damages)

    def compute_defend(self, damages, roll):
        return max(0, damages - self.defend_value - roll)  


    def defend(self, damages):
        roll = self.dice.roll()
        wounds = self.compute_defend(damages, roll)
        print(f"{self.name} [green]defend[/green] against {damages} and take {wounds} wounds ({damages} dmg - {self.defend_value} def - {roll} rng)")
        self.decrease_hp(wounds)

    def allies(self,): pass

class Warrior(Character):
    label = "warrior"

    def compute_damages(self, roll):
        print("🪓 Warrior bonus : +3 dmg")
        return super().compute_damages(roll) + 3


class Mage(Character):
    label = "mage"

    def compute_defend(self, damages, roll):
        wounds = super().compute_defend(damages, roll) - 3  
        print("🔮 Mage bonus : -3 wounds")
        return max(0, wounds)
    

class Thief(Character):
    label = "thief"

    def compute_defend(self, damages, roll):
        print("🗡️ Thief bonus: ignore l'armure de l'ennemi !")
        wounds = max(0, damages - roll)  
        return wounds
    # ignore la défense de son adversaire (physique) 


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

    def heal(self, target):
        roll = self.dice.roll()
        heal_amount = 0

        print("⚕️ Healer bonus : peut soigner en fonction de son attaque.")

        if roll < self.dice.faces * 0.1:
            print("❌ Échec du soin !")
        elif self.dice.faces * 0.1 <= roll < self.dice.faces * 0.25:
            heal_amount = self.attack_value // 4
            print(f"✨ Soin réussi : {heal_amount} points de vie restaurés (1/4 de l'attaque).")
        elif self.dice.faces * 0.25 <= roll < self.dice.faces * 0.5:
            heal_amount = self.attack_value // 2
            print(f"💖 Soin réussi : {heal_amount} points de vie restaurés (1/2 de l'attaque).")
        elif self.dice.faces * 0.5 <= roll < self.dice.faces * 0.99:
            heal_amount = (self.attack_value * 3) // 4
            print(f"💖💖 Soin réussi : {heal_amount} points de vie restaurés (3/4 de l'attaque).")
        elif roll == self.dice.faces:
            heal_amount = self.attack_value
            print(f"💖💖💖 Soin parfait ! {heal_amount} points de vie restaurés (100% de l'attaque).")

        target.hp = min(target.max_hp, target.hp + heal_amount)
        target.show_healthbar()

    def attack(self, target):
        action = input("Voulez-vous attaquer (A) ou soigner (S) ? >>> ").lower()

        if action == "s":
            heal_target = input("Voulez-vous vous soigner vous-même (M) ou un allié (A) ? >>> ").lower()
            if heal_target == "m":
                self.heal(self)
            else:
                ally_name = input("Entrez le nom de l'allié à soigner : ")
                for ally in allies :
                    if ally.name.lower() == ally_name.lower():
                        self.heal(ally)
                        break
                else:
                    print("⚠️ Aucun allié trouvé avec ce nom !")
        else:
            super().attack(target)




if __name__ == "__main__":
    print("\n")

    char_1 = Thief("James", 20, 8, 3, Dice("red", 6))
    char_2 = Mage("Elsa", 20, 8, 3, Dice("red", 6))

    print(char_1)
    print(char_2)

    char_1.attack(char_2)

    # while (char_1.is_alive() and char_2.is_alive()):
    #     char_1.attack(char_2)
    #     char_2.attack(char_1)
