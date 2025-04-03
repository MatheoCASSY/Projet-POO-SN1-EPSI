from rich import print
from ui import print_durability, print_item_broken, print_item_removed

class Universal_Item:
    label = "universal_item"

    def __init__(self, name: str, durability_max: int, attack_value: int = 0, defend_value: int = 0, heal_amount: int = 0):
        self.name = name
        self.durability_max = durability_max
        self.durability = durability_max
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.heal_amount = heal_amount

    def __str__(self) -> str:
        return f"I'm {self.name} the {self.label}."

    def is_usable(self) -> bool:
        return self.durability > 0

    def decrease_durability(self, amount: int):
        self.durability = max(0, self.durability - amount)
        self.show_durability()

    def show_durability(self):
        print_durability(self)

    def apply_bonus(self, character):
        if self.is_usable():
            print(f"{character.name} équipe {self.name}, gagnant +{self.defend_value} DEF et +{self.attack_value} ATK!")
            character.defend_value += self.defend_value
            character.attack_value += self.attack_value
        else:
            print_item_broken(self)

    def remove_bonus(self, character):
        print_item_removed(character, self)
        character.defend_value -= self.defend_value
        character.attack_value -= self.attack_value

    def use(self, character):
        if self.is_usable():
            self.decrease_durability(1)
            if self.durability == 0:
                self.remove_bonus(character)

class Heal_potion(Universal_Item):
    label = "Heal_potion"

    def __init__(self, name: str, heal_amount: int):
        super().__init__(name, durability_max=1, heal_amount=heal_amount)
    
    def use(self, target):
        if target.hp < target.max_hp:
            healed_hp = min(target.max_hp - target.hp, self.heal_amount)
            target.hp += healed_hp
            print(f"🧪 {target.name} utilise {self.name} et récupère {healed_hp} HP !")
            target.show_healthbar()
            self.durability = 0  # Potion consommée
        else:
            print(f"⚠️ {target.name} a déjà tous ses HP ! Pas besoin d'utiliser {self.name}.")

class Helmet(Universal_Item):
    label = "Helmet"

class Sword(Universal_Item):
    label = "Sword"

class Shield(Universal_Item):
    label = "Shield"

class Amulet(Universal_Item):
    label = "Amulet"

if __name__ == "__main__":
    from character import Character
    warrior = Character("Arthur", 10000, 15, 8, None)
    warrior.hp -= 40  
    warrior.show_healthbar()  
    
    helmet = Helmet("Casque en Cuir", 10, defend_value=3)
    sword = Sword("Epee du Grand Monarque", 15, attack_value=5)
    shield = Shield("Bouclier en Fer", 12, defend_value=4)
    amulet = Amulet("Amulette Mystique", 8, defend_value=2, attack_value=2)
    heal_potion = Heal_potion("Extrait de Jouvence", 5)
    
    helmet.apply_bonus(warrior)
    sword.apply_bonus(warrior)
    shield.apply_bonus(warrior)
    amulet.apply_bonus(warrior)
    
    for _ in range(5):
        helmet.use(warrior)
        sword.use(warrior)
        shield.use(warrior)
        amulet.use(warrior)
        heal_potion.use(warrior)
