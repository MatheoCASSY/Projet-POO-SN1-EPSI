from item import *
from rich import print
from ui import console

class Inventaire:
    label = "inventaire"

    def __init__(self):
        self.items = []
        self.equipped_items = {}
    
    def add_item(self, item):
        self.items.append(item)
        print(f"📦 {item.name} ajouté à l'inventaire !")
    
    def remove_item(self):
        self.show_inventory()
        choice = input("Quel objet voulez-vous jeter ? (Nom exact) : ").lower()
        item = next((i for i in self.items if i.name.lower() == choice), None)
        if item:
            self.items.remove(item)
            print(f"🗑️ {item.name} a été jeté !")
        else:
            print("❌ Objet non trouvé dans l'inventaire !")
    
    def equip_item(self, character):
        self.show_inventory()
        choice = input("Quel objet voulez-vous équiper ? (Nom exact) : ").lower()
        item = next((i for i in self.items if i.name.lower() == choice and i.is_usable()), None)
        if item:
            self.equipped_items[item.label] = item
            self.items.remove(item)
            item.apply_bonus(character)
            print(f"✅ {character.name} a équipé {item.name}.")
        else:
            print("❌ Objet non trouvable ou inutilisable !")
    
    def unequip_item(self, character):
        self.show_equipped()
        choice = input("Quel objet voulez-vous déséquiper ? (Nom exact) : ").lower()
        item = next((i for i in self.equipped_items.values() if i.name.lower() == choice), None)
        if item:
            del self.equipped_items[item.label]
            self.items.append(item)
            item.remove_bonus(character)
            print(f"⚠️ {character.name} a retiré {item.name}.")
        else:
            print("❌ Objet non trouvé parmi les équipements !")
    
    def show_inventory(self):
        print("📜 Inventaire :", [item.name for item in self.items])
    
    def show_equipped(self):
        print("🛡️ Équipement :", {label: item.name for label, item in self.equipped_items.items()})

if __name__ == "__main__":
    from character import Character
    warrior = Character("Arthur", 100, 15, 8, None)
    inventory = Inventaire()

    from item import Helmet, Sword, Heal_potion
    helmet = Helmet("Steel Helmet", 10, defend_value=3)
    sword = Sword("Legendary Sword", 15, attack_value=5)
    heal_potion = Heal_potion("Extrait de Jouvence", 5)
    
    inventory.add_item(helmet)
    inventory.add_item(sword)
    inventory.add_item(heal_potion)
    
    while True:
        print("\nOptions : [1] Voir inventaire [2] Voir équipement [3] Équiper un objet [4] Déséquiper un objet [5] Jeter un objet [6] Quitter")
        action = input("Que voulez-vous faire ? : ")
        
        if action == "1":
            inventory.show_inventory()
        elif action == "2":
            inventory.show_equipped()
        elif action == "3":
            inventory.equip_item(warrior)
        elif action == "4":
            inventory.unequip_item(warrior)
        elif action == "5":
            inventory.remove_item()
        elif action == "6":
            break
        else:
            print("❌ Option invalide, essayez encore !")
