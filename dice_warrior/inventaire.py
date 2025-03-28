from character import *
from rich import print


class Universal_Item:
    label = "universal_item"

    def __init__(self, name, durability_max, attack_value, defend_value):
        self.name = name
        self.durability_max = durability_max
        self.durability = durability_max
        self.attack_value = attack_value
        self.defend_value = defend_value

    def __str__(self):
        return f"I'm {self.name} the {self.label}."

    def is_usable(self):
        return self.durability > 0

    def decrease_durability(self, amount):
        self.durability = max(0, self.durability - amount)
        self.show_durability()

    def show_durability(self):
        print(f"[{'🛡️ ' * self.durability} {'⛉ ' * (self.durability_max - self.durability)}] {self.durability}/{self.durability_max} durability  ----->   {self.name}")
        print("\n")

    def apply_bonus(self, character):
        if self.is_usable():
            print(f" {character.name} equipped {self.name}, gaining +{self.defend_value} DEF and +{self.attack_value} ATK!")
            character.defend_value += self.defend_value
            character.attack_value += self.attack_value
        else:
            print(f"⚠️ {self.name} is broken and provides no bonus!")

    def remove_bonus(self, character):
        print(f"⚠️ {character.name} removed {self.name}, losing -{self.defend_value} DEF and -{self.attack_value} ATK!")
        character.defend_value -= self.defend_value
        character.attack_value -= self.attack_value

    def use(self, character):
        if self.is_usable():
            self.decrease_durability(1)
            if self.durability == 0:
                self.remove_bonus(character)


class Helmet(Universal_Item):
    label = "Helmet"

    def __init__(self, name, durability_max, defend_value):
        super().__init__(name, durability_max, attack_value=0, defend_value=defend_value)


class Sword(Universal_Item):
    label = "Sword"

    def __init__(self, name, durability_max, attack_value):
        super().__init__(name, durability_max, attack_value=attack_value, defend_value=0)


# Ajout de nouveaux objets
class Shield(Universal_Item):
    label = "Shield"

    def __init__(self, name, durability_max, defend_value):
        super().__init__(name, durability_max, attack_value=0, defend_value=defend_value)


class Bow(Universal_Item):
    label = "Bow"

    def __init__(self, name, durability_max, attack_value):
        super().__init__(name, durability_max, attack_value=attack_value, defend_value=0)


class Boots(Universal_Item):
    label = "Boots"

    def __init__(self, name, durability_max, defend_value):
        super().__init__(name, durability_max, attack_value=0, defend_value=defend_value)


class Gloves(Universal_Item):
    label = "Gloves"

    def __init__(self, name, durability_max, defend_value):
        super().__init__(name, durability_max, attack_value=0, defend_value=defend_value)


class Armor(Universal_Item):
    label = "Armor"

    def __init__(self, name, durability_max, defend_value):
        super().__init__(name, durability_max, attack_value=0, defend_value=defend_value)


class Dagger(Universal_Item):
    label = "Dagger"

    def __init__(self, name, durability_max, attack_value):
        super().__init__(name, durability_max, attack_value=attack_value, defend_value=0)


class Amulet(Universal_Item):
    label = "Amulet"

    def __init__(self, name, durability_max, defend_value, attack_value):
        super().__init__(name, durability_max, attack_value=attack_value, defend_value=defend_value)


class Ring(Universal_Item):
    label = "Ring"

    def __init__(self, name, durability_max, defend_value, attack_value):
        super().__init__(name, durability_max, attack_value=attack_value, defend_value=defend_value)


# Test des objets
if __name__ == "__main__":
    class Warrior(Character):
        label = "Warrior"

    warrior = Warrior("Arthur", 100, 15, 8, None, 0, 1)
    
    helmet = Helmet("Steel Helmet", 10, 3)
    sword = Sword("Legendary Sword", 15, 5)
    shield = Shield("Iron Shield", 12, 4)
    amulet = Amulet("Mystic Amulet", 8, 2, 2)
    
    helmet.apply_bonus(warrior)
    sword.apply_bonus(warrior)
    shield.apply_bonus(warrior)
    amulet.apply_bonus(warrior)
    
    for _ in range(5):
        helmet.use(warrior)
        sword.use(warrior)
        shield.use(warrior)
        amulet.use(warrior)