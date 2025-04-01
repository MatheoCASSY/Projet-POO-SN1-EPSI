from character import *
from dice import Dice
import random
import inspect

def get_available_classes():
    return {name: cls for name, cls in inspect.getmembers(__import__('character'), inspect.isclass) if issubclass(cls, Character) and cls is not Character}

def create_character():
    characters = []
    classes = get_available_classes()
    
    while True:
        name = input("Nom du personnage : ")
        print("Choisissez une classe parmi : ", ", ".join(classes.keys()))
        class_choice = input("Classe : ").capitalize()
        
        if class_choice not in classes:
            print("Classe invalide, veuillez réessayer.")
            continue
        
        dice_color = input("Couleur du dé (ex: rouge, bleu, vert) : ")
        dice_faces = int(input("Nombre de faces du dé (ex: 6, 8, 10) : "))
        dice = Dice(dice_color, dice_faces)
        
        # Demander les valeurs nécessaires pour la classe du personnage
        max_hp = int(input("Entrez la valeur pour max_hp : "))
        attack_value = int(input("Entrez la valeur pour attack_value : "))
        defend_value = int(input("Entrez la valeur pour defend_value : "))

        # Si la classe est Healer, demander la liste des alliés
        chosen_class = classes[class_choice]
        if class_choice == "Healer":
            allies = [char for char in characters]  # Liste des autres personnages déjà créés
            character = chosen_class(name, max_hp, attack_value, defend_value, dice, allies)
        else:
            character = chosen_class(name, max_hp, attack_value, defend_value, dice)
        
        characters.append(character)

        more = input("Voulez-vous créer un autre personnage ? (o/n) ")
        if more.lower() != 'o':
            break
    return characters


def create_enemy():
    enemies = [Goblin("Goblin", 12, 5, 2, Dice("green", 6), 10),
               Skeleton("Squelette", 15, 6, 2, Dice("white", 6), 15),
               Orc("Orc", 22, 9, 3, Dice("red", 6), 20),
               Troll("Troll", 30, 10, 4, Dice("blue", 6), 25),
               Boss("Seigneur Noir", 40, 12, 6, Dice("black", 8), 50)]
    return random.choice(enemies)

def battle(player, enemy):
    print(f"{player.name} le {player.__class__.__name__} affronte {enemy.name} !")
    while player.is_alive() and enemy.is_alive():
        dmg = player.attack()
        enemy.defend(dmg)
        if enemy.is_alive():
            dmg = enemy.attack(player)
    
    if player.is_alive():
        print(f"{player.name} a vaincu {enemy.name} !")
    else:
        print(f"{player.name} a été vaincu par {enemy.name}...")

def main():
    print("Bienvenue dans la campagne DnD!")
    players = create_character()
    print("Préparez-vous à combattre!")
    
    for player in players:
        print(f"Bienvenue, {player.name} le {player.__class__.__name__}!")
        while player.is_alive():
            enemy = create_enemy()
            battle(player, enemy)
            if not player.is_alive():
                print("Game Over!")
                break
            cont = input("Voulez-vous continuer l'aventure? (o/n) ")
            if cont.lower() != 'o':
                print("Fin de la campagne. Bravo!")
                break

if __name__ == "__main__":
    main()