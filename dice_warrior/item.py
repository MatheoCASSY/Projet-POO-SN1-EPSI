from rich import print


class Universal_Item:
    label = "universal_item"

    def __init__(self, name, durability_max, attack_value=0, defend_value=0, heal_amount=0):
        self.name = name
        self.durability_max = durability_max
        self.durability = durability_max
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.heal_amount = heal_amount

    def __str__(self):
        return f"I'm {self.name} the {self.label}."

    def is_usable(self):
        return self.durability > 0

    def decrease_durability(self, amount):
        self.durability = max(0, self.durability - amount)
        self.show_durability()

    def show_durability(self):
        print(f"[{'🛡️ ' * self.durability} {'⛉ ' * (self.durability_max - self.durability)}] {self.durability}/{self.durability_max} durability  ----->   {self.name}\n")

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

class Heal_potion(Universal_Item):
    label = "Heal_potion"

    def __init__(self, name, heal_amount):
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

# Test des objets
if __name__ == "__main__":
    from character import Character

    class Warrior(Character):
        label = "Warrior"
    
    warrior = Warrior("Arthur", 100, 15, 8, None, 0, 1)
    warrior.hp -= 40  
    warrior.show_healthbar()  
    
    helmet = Helmet("Steel Helmet", 10, defend_value=3)
    sword = Sword("Legendary Sword", 15, attack_value=5)
    shield = Shield("Iron Shield", 12, defend_value=4)
    amulet = Amulet("Mystic Amulet", 8, defend_value=2, attack_value=2)
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
        heal_potion.use(warrior)  # Test de la potion

      
