import time
import random
import inspect
from character import *
from enemies import *
from dice import Dice
from ui import *

# Fonction utilitaire pour ajouter un délai et des sauts de ligne entre les phases
def pause_phase():
    print("\n" * 3)
    time.sleep(1)

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
        
        chosen_class = classes[class_choice]
        # Pour le healer, on passe la liste des alliés existants
        if class_choice == "Healer":
            allies = [char for char in characters]
            character = chosen_class(name, max_hp, attack_value, defend_value, dice, allies)
        else:
            character = chosen_class(name, max_hp, attack_value, defend_value, dice)
        
        character.gold = 0  # On initialise l'or à 0
        characters.append(character)
        
        print_character_creation_prompt(character.name, class_choice, max_hp, attack_value, defend_value, dice)
        pause_phase()
        
        more = print_more_characters_prompt()
        if more.lower() != 'o':
            break
    return characters

def manage_inventory(character):
    console.print("\n[bold cyan]Gestion de l'inventaire[/bold cyan]")
    console.print("[1] Afficher inventaire")
    console.print("[2] Équiper un objet")
    console.print("[3] Déséquiper un objet")
    console.print("[4] Jeter un objet")
    console.print("[r] Revenir")
    choice = console.input("[bold blue]Votre choix : [/bold blue]").lower()
    if choice == "1":
        character.inventory.show_inventory()
        character.inventory.show_equipped()
    elif choice == "2":
        character.inventory.equip_item(character)
    elif choice == "3":
        character.inventory.unequip_item(character)
    elif choice == "4":
        character.inventory.remove_item()
    elif choice == "r":
        return
    else:
        console.print("[red]Option invalide ![/red]")
    pause_phase()

def shop_phase(players):
    console.print("\n[bold magenta]Phase Boutique ![/bold magenta]")
    pause_phase()
    # Définition d'un catalogue simple
    catalogue = {
        "1": { "name": "Épée en fer", "item": Sword, "args": ("Épée en fer", 15, 5), "cost": 15 },
        "2": { "name": "Casque en acier", "item": Helmet, "args": ("Casque en acier", 10, 3), "cost": 12 },
        "3": { "name": "Potion de soin", "item": Heal_potion, "args": ("Potion de soin", 5), "cost": 8 }
    }
    for player in players:
        if not player.is_alive():
            continue
        console.print(f"\n[bold blue]{player.name}, vous avez {player.gold} or.[/bold blue]")
        choice = console.input("Voulez-vous visiter la boutique ? (o/n) : ").lower()
        if choice != "o":
            continue
        
        buying = True
        while buying:
            console.print("\n[bold yellow]Catalogue :[/bold yellow]")
            for key, article in catalogue.items():
                console.print(f"[cyan]{key}[/cyan] - {article['name']} (Coût : {article['cost']} or)")
            console.print("[r] - Retour")
            achat = console.input("[bold blue]Votre choix : [/bold blue]").lower()
            if achat == "r":
                buying = False
                continue
            if achat in catalogue:
                article = catalogue[achat]
                if player.gold >= article["cost"]:
                    player.gold -= article["cost"]
                    # Instanciation de l'objet via les arguments définis
                    item_obj = article["item"](*article["args"])
                    player.inventory.add_item(item_obj)
                    console.print(f"[bold green]{player.name} a acheté {article['name']} ![/bold green]")
                    console.print(f"Il vous reste {player.gold} or.")
                else:
                    console.print("[red]Fonds insuffisants ![/red]")
            else:
                console.print("[red]Option invalide dans la boutique ![/red]")
            pause_phase()

def battle(player, enemy):
    print_battle_intro(player, enemy)
    pause_phase()
    
    while player.is_alive() and enemy.is_alive():
        print_health_bars(player, enemy)
        pause_phase()
        
        console.print("[bold yellow]Actions disponibles :[/bold yellow]")
        console.print(" - [green]attaquer[/green]")
        console.print(" - [blue]inventaire[/blue] (pour gérer vos objets)")
        console.print(" - [red]abandonner[/red]")
        action = console.input("[bold blue]Que faites-vous ? [/bold blue]").lower()
        pause_phase()
        
        if action == "attaquer":
            # Le joueur attaque
            player.attack(enemy)
            pause_phase()
            if enemy.is_alive():
                # L'ennemi contre-attaque
                enemy.attack(player)
                pause_phase()
            else:
                console.print(f"[bold green]🎉 {enemy.name} est vaincu ![/bold green]")
                pause_phase()
                break

        elif action == "inventaire":
            manage_inventory(player)
            continue

        elif action == "abandonner":
            print_abandon_message(player)
            pause_phase()
            return False

        else:
            print_invalid_action_message()
            pause_phase()
            continue

    print_battle_result(player, enemy)
    pause_phase()

    if player.is_alive():
        print_victory_message(player, enemy)
        pause_phase()
        return True
    else:
        print_defeat_message(player, enemy)
        pause_phase()
        return False

def main():
    players = []
    print_welcome_message()
    pause_phase()
    
    knows_classes = print_know_classes_prompt()
    if knows_classes != 'o':
        classes = get_available_classes()
        print_class_details(classes)
        pause_phase()
    
    players = create_character()
    pause_phase()
    
    enemies = [
        Goblin("Goblin", 12, 5, 2, Dice("green", 6), xp_reward=10),
        Skeleton("Squelette", 15, 6, 2, Dice("white", 6), xp_reward=15),
        Orc("Orc", 22, 9, 3, Dice("red", 6), xp_reward=20),
        Troll("Troll", 30, 10, 4, Dice("blue", 6), xp_reward=25),
        Boss("Seigneur Noir", 40, 12, 6, Dice("black", 8), xp_reward=50)
    ]
    
    console.print("[bold cyan]Préparez-vous à combattre ![/bold cyan]")
    pause_phase()
    
    for enemy in enemies:
        if all(not player.is_alive() for player in players):
            print_game_over_message()
            return
        
        print_enemy_appearance(enemy)
        pause_phase()
        
        # Combat par tour : chaque joueur vivant intervient
        while enemy.is_alive() and any(player.is_alive() for player in players):
            for player in players:
                if enemy.is_alive() and player.is_alive():
                    console.print(f"\n[bold blue]{player.name}, c'est votre tour ![/bold blue]")
                    pause_phase()
                    if not battle(player, enemy):
                        console.print("[red]L'aventure s'arrête ici...[/red]")
                        return
            # Si l'ennemi est toujours vivant, il attaque un joueur aléatoire vivant
            if enemy.is_alive():
                target = random.choice([p for p in players if p.is_alive()])
                console.print(f"\n[bold red]{enemy.name} attaque spontanément {target.name} ![/bold red]")
                pause_phase()
                enemy.attack(target)
                pause_phase()
                if not target.is_alive():
                    console.print(f"[red]{target.name} est hors de combat ![/red]")
                    pause_phase()
                    
        # Récompense : chaque joueur vivant reçoit de l'or (le xp_reward de l'ennemi)
        if not enemy.is_alive():
            for player in players:
                if player.is_alive():
                    player.gold += enemy.xp_reward
                    console.print(f"[bold green]{player.name} gagne {enemy.xp_reward} or ! (Total: {player.gold} or)[/bold green]")
                    pause_phase()
            # Message spécial pour le boss final
            if enemy.label == "boss":
                console.print("[bold magenta]GG, vous avez vaincu le Seigneur Noir ! L'aventure est terminée ![/bold magenta]")
                pause_phase()
        
        # Phase Boutique entre chaque combat
        shop_phase(players)
        pause_phase()
    
    print_victory_message_final()
    pause_phase()

if __name__ == "__main__":
    main()
