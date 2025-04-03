from character import *
from enemies import *
from dice import Dice
import random
import inspect
from ui import *

def get_available_classes():
    return {name: cls for name, cls in inspect.getmembers(__import__('character'), inspect.isclass) if issubclass(cls, Character) and cls is not Character}


def create_character():
    characters = []
    classes = get_available_classes()
    
    while True:
        name = console.input("[bold blue]Nom du personnage : [/bold blue]")  
        print_class_choice_prompt(classes)
        class_choice = console.input("[bold green]Classe : [/bold green]")

        if class_choice == "?":
            console.print("\n[bold magenta]Détails des classes disponibles :[/bold magenta]")
            for class_name in classes.keys():
                console.print(f"[cyan]{class_name}[/cyan]: {describe_class(class_name)}")
            continue
        
        class_choice = class_choice.capitalize()

        if class_choice not in classes:
            print_invalid_class_message()
            continue

        console.print(f"[bold green]{describe_class(class_choice)}[/bold green]")

        dice_color = console.input("[bold blue]Couleur du dé (ex: rouge, bleu, vert) : [/bold blue]")  
        dice_faces = int(console.input("[bold blue]Nombre de faces du dé (ex: 6, 8, 10) : [/bold blue]"))  
        dice = Dice(dice_color, dice_faces)

        max_hp = int(console.input("[bold blue]Entrez la valeur pour max_hp : [/bold blue]"))  
        attack_value = int(console.input("[bold blue]Entrez la valeur pour attack_value : [/bold blue]"))  
        defend_value = int(console.input("[bold blue]Entrez la valeur pour defend_value : [/bold blue]"))  
        
        xp = 0  # XP initial
        level = 1  # Niveau initial
        
        chosen_class = classes[class_choice]

        if class_choice == "Healer":
            allies = [char for char in characters]
            character = chosen_class(name, max_hp, attack_value, defend_value, dice, xp, level, allies)
        else:
            character = chosen_class(name, max_hp, attack_value, defend_value, dice, xp, level)

        characters.append(character)
        
        print_character_creation_prompt(character.name, class_choice, max_hp, attack_value, defend_value, dice)

        more = print_more_characters_prompt()
        if more.lower() != 'o':
            break
            
    return characters


def battle(player, enemy):
    print_battle_intro(player, enemy)
    
    while player.is_alive() and enemy.is_alive():
        print_health_bars(player, enemy)

        action = print_action_prompt()
        
        if action == "attaquer":
            dmg = player.attack(enemy)
            enemy.defend(dmg)
            print_attack_message(player, enemy)
        elif action == "se regenerer":
            regen = player.regenerate()
            print_regeneration_message(player)
        elif action == "abandonner":
            print_abandon_message(player)
            return False
        else:
            print_invalid_action_message()
            continue
        
        if enemy.is_alive():
            dmg = enemy.attack(player)
            player.defend(dmg)
            print_enemy_attack_message(player, enemy)

    print_battle_result(player, enemy)

    if player.is_alive():
        print_victory_message(player, enemy)
        for p in [player for player in player if player.is_alive()]:
            print_xp_bar(p)
        return True
    else:
        print_defeat_message(player, enemy)
        return False

def main():
    players = []
    print_welcome_message()
    
    knows_classes = print_know_classes_prompt()
    
    if knows_classes != 'o':
        classes = get_available_classes()
        print_class_details(classes)
    
    players = create_character()
    enemies = [
        Goblin("Goblin", 12, 5, 2, Dice("green", 6), 10),
        Skeleton("Squelette", 15, 6, 2, Dice("white", 6), 15),
        Orc("Orc", 22, 9, 3, Dice("red", 6), 20),
        Troll("Troll", 30, 10, 4, Dice("blue", 6), 25),
        Boss("Seigneur Noir", 40, 12, 6, Dice("black", 8), 50)
    ]
    
    console.print("[bold cyan]Préparez-vous à combattre![/bold cyan]")
    
    for enemy in enemies:
        if all(not player.is_alive() for player in players):
            print_game_over_message()
            return
        
        print_enemy_appearance(enemy)

        for player in players:
            if player.is_alive():
                if not battle(player, enemy):
                    return
                if not enemy.is_alive():
                    console.print(f"[bold green]🎉 {enemy.name} est vaincu![/bold green]")   
                    break

    print_victory_message_final()

main()