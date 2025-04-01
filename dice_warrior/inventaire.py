from item import *  
from rich import print
from ui import *  
from dice import Dice
from character import *

class Inventaire:
    label = "inventaire"

    def __init__(self):
        self.items = []
        self.equipped_items = {}

    def add_item(self, item):
        self.items.append(item)
        print_item_added(item)

    def remove_item(self):
        self.show_inventory()
        choice = input("Quel objet voulez-vous jeter ? (Nom exact) : ").strip().lower()
        item = next((i for i in self.items if i.name.lower() == choice), None)
        if item:
            self.items.remove(item)
            print_item_removed(item)
        else:
            print("❌ Objet non trouvé dans l'inventaire !")

    def equip_item(self, character):
        self.show_inventory()
        choice = input("Quel objet voulez-vous équiper ? (Nom exact) : ").strip().lower()
        item = next((i for i in self.items if i.name.lower() == choice and i.is_usable()), None)
        if item:
            self.equipped_items[item.label] = item
            self.items.remove(item)
            item.apply_bonus(character)
            print_item_equipped(character, item)
        else:
            print("❌ Objet non trouvable ou inutilisable !")

    def unequip_item(self, character):
        self.show_equipped()
        choice = input("Quel objet voulez-vous déséquiper ? (Nom exact) : ").strip().lower()
        item = next((i for i in self.equipped_items.values() if i.name.lower() == choice), None)
        if item:
            del self.equipped_items[item.label]
            self.items.append(item)
            item.remove_bonus(character)
            print_item_unequipped(character, item)
        else:
            print("❌ Objet non trouvé parmi les équipements !")

    def show_inventory(self):
        print_inventory(self.items)

    def show_equipped(self):
        print_equipped(self.equipped_items)

def gerer_personnage(char_1, char_2):
    while True:
        # 🔹 Choix du personnage avant l'action
        print(f"[1] Quitter [2] {char_1.name} ({char_1.label}) [3] {char_2.name} ({char_2.label}) ")
        character_choice = input("Quel personnage voulez-vous gérer ? : ").strip()

        if character_choice == "1":
            character = char_1
        elif character_choice == "2":
            character = char_2
        elif character_choice == "3":
            print("👋 Fin du programme.")
            break
        else:
            print("❌ Option invalide, essayez encore !")
            continue  # Redemande de choisir un personnage

        # 🔹 Une fois le personnage choisi, affichage des options
        while True:
            print(f"\n🎭 [Gérer {character.name}]")
            print("[1] Voir inventaire [2] Voir équipement [3] Équiper un objet [4] Déséquiper un objet [5] Jeter un objet [6] Changer de personnage")

            action = input("Que voulez-vous faire ? : ").strip()

            if action == "1":
                character.inventory.show_inventory()
            elif action == "2":
                character.inventory.show_equipped()
            elif action == "3":
                character.inventory.equip_item(character)
            elif action == "4":
                character.inventory.unequip_item(character)
            elif action == "5":
                character.inventory.remove_item()
            elif action == "6":
                print("🔄 Changement de personnage...")
                break  # Sort de la boucle interne pour choisir un autre personnage
            else:
                print("❌ Option invalide, essayez encore !")



if __name__ == "__main__":
    # Création des personnages avec leur inventaire
    char_1 = Warrior("James", 20, 8, 3, Dice("red", 6), 1, 1)
    char_2 = Mage("Merlin", 80, 10, 5, Dice("bleu", 6), 1, 1)

    # Création des objets
    helmet = Helmet("Steel Helmet", 10, defend_value=3, attack_value=0, heal_amount=0)
    sword = Sword("Legendary Sword", 15, defend_value=0, attack_value=5, heal_amount=0)
    heal_potion = Heal_potion("Extrait de Jouvence", 5)

    # Ajout des objets à l'inventaire des personnages
    char_1.inventory.add_item(helmet)
    char_1.inventory.add_item(sword)
    char_2.inventory.add_item(heal_potion)

    # 🔹 Appel de la fonction pour gérer les personnages
    gerer_personnage(char_1, char_2)