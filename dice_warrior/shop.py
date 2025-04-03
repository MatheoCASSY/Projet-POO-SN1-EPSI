from dice import Dice
from character import Character
from item import Sword, Helmet, Heal_potion
from rich import print
from ui import console

class Shop:
    label = "shop"
    def __init__(self):
        self.price_per_hp = 3  # 3 or pour 1 HP

    def show_shop(self, character: Character):
        print(f"\nBienvenue à la boutique, {character.name} !")
        character.inventory.show_inventory()

        action = input(f"Voulez-vous acheter des HP ? Chaque HP coûte {self.price_per_hp} or. (o/n) : ").lower()
        if action == 'o':
            amount = int(input(f"Combien d'HP souhaitez-vous acheter ? Vous avez {character.gold} or : "))
            total_price = amount * self.price_per_hp
            if total_price > character.gold:
                print("❌ Vous n'avez pas assez d'or.")
            else:
                character.gold -= total_price
                character.max_hp += amount
                character.hp += amount
                print(f"🎉 Vous avez acheté {amount} HP !")
                print(f"Il vous reste {character.gold} or.")
        else:
            print("Merci de votre visite à la boutique !")

# Exemple d'utilisation:
if __name__ == "__main__":
    character = Character("Hero", 100, 10, 5, Dice("red", 6))
    shop = Shop()
    shop.show_shop(character)
    character.show_inventory()
