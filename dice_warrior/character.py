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

    def is_alive(self, hp):
        self.hp = hp
        if self.hp <= 0:
            print(f"HP = {self.hp}, your charachter is dead!")
            return False
        else: return True

    def show_healthbar(self):
        print(f"[{self.hp * "o"}] {self.hp}/{self.max_hp}hp")


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

    class Assassin(Character):
     label = "assassin"

    def __init__(self, name, max_hp, attack_value, defend_value, dice):
        super().__init__(name, max_hp, attack_value, defend_value, dice)
        self.poisoned_targets = {}  

    def attack(self, target):
        roll = self.dice.roll()
        damage = self.compute_damages(roll)  
        print(f" {self.name} attaque et inflige {damage} dégâts !")

        
        if roll > self.dice.faces // 2:  
            poison_duration = 3  
            poison_damage = 2  
            self.poisoned_targets[target] = (poison_damage, poison_duration)  
            print(f" {target.name} est empoisonné ! Il perdra {poison_damage} HP pendant {poison_duration} tours.")

        target.defend(damage)  

    def apply_poison_effects(self):
        for target, (poison_damage, turns_left) in list(self.poisoned_targets.items()):
            if turns_left > 0:
                target.decrease_hp(poison_damage)  
                print(f" {target.name} souffre du poison et perd {poison_damage} HP ! ({turns_left - 1} tours restants)")
                self.poisoned_targets[target] = (poison_damage, turns_left - 1)  
            else:
                del self.poisoned_targets[target]  
                print(f" {target.name} n'est plus empoisonné !")