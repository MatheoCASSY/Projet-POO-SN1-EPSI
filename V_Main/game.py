import time
import random
import inspect
from character import *
from enemies import *
from dice import Dice
from ui import *

# Fonction utilitaire pour ajouter un délai entre les phases
def pause_phase():
    print("\n" * 3)
    time.sleep(1)

def get_available_classes():
    # Récupère toutes les sous-classes de Character (hors Character lui-même)
    return {name: cls for name, cls in inspect.getmembers(__import__('character'), inspect.isclass)
            if issubclass(cls, Character) and cls is not Character}

def create_character():
    characters = []
    classes = get_available_classes()

    while True:
        name = console.input("[bold blue]Nom du personnage : [/bold blue]")
        print_class_choice_prompt(classes)
        class_choice = console.input("[bold green]Classe : [/bold green]").capitalize()

        if class_choice == "?":
            console.print("\n[bold magenta]Détails des classes disponibles :[/bold magenta]")
            for cls_name in classes.keys():
                console.print(f"[cyan]{cls_name}[/cyan]: {describe_class(cls_name)}")
            continue

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
        if class_choice == "Healer":
            # Pour le Healer, passer la liste des alliés déjà créés
            character = chosen_class(name, max_hp, attack_value, defend_value, dice, allies=characters)
        else:
            character = chosen_class(name, max_hp, attack_value, defend_value, dice)

        character.gold = 0  # Initialiser l'or à 0
        characters.append(character)

        print_character_creation_prompt(character.name, class_choice, max_hp, attack_value, defend_value, dice)
        pause_phase()

        more = console.input("[bold blue]\nVoulez-vous créer un autre personnage ? (o/n) [/bold blue]").lower()
        if more != 'o':
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
    from shop import Shop
    shop = Shop()
    for player in players:
        if not player.is_alive():
            continue
        console.print(f"\n[bold blue]{player.name}, vous avez {player.gold} or.[/bold blue]")
        choice = console.input("Voulez-vous visiter la boutique ? (o/n) : ").lower()
        if choice != "o":
            continue
        shop.show_shop(player)
        pause_phase()

def random_event(players):
    events = [
        "Un piège s'active ! Un joueur perd 10 HP.",
        "Un marchand louche propose une affaire risquée...",
        "Un bandit vole 10 or à un joueur au hasard !",
        "Une fontaine magique restaure 5 HP à tous les joueurs !"
    ]
    event = random.choice(events)
    console.print(f"[bold yellow]{event}[/bold yellow]")

    if "piège" in event:
        unlucky_player = random.choice(players)
        unlucky_player.hp = max(0, unlucky_player.hp - 10)
    elif "bandit" in event:
        unlucky_player = random.choice(players)
        unlucky_player.gold = max(0, unlucky_player.gold - 10)
    elif "fontaine" in event:
        for player in players:
            player.hp = min(player.max_hp, player.hp + 5)


def battle(players, enemy): 
    from ui import print_battle_intro, print_health_bars, print_invalid_action_message, print_victory_message, print_defeat_message
    print_battle_intro(players, enemy)
    pause_phase()

    while any(player.is_alive() for player in players) and enemy.is_alive():
        # Affichage des barres de santé
        print_health_bars(players, enemy)
        pause_phase()

        # Chaque joueur attaque à tour de rôle
        for player in players:
            if player.is_alive():
                console.print(f"\n[bold blue]{player.name}, c'est votre tour ![/bold blue]")
                console.print("[bold yellow]Actions disponibles :[/bold yellow]")
                console.print(" - [green]attaquer[/green]")
                console.print(" - [blue]inventaire[/blue] (pour gérer vos objets)")
                console.print(" - [red]abandonner[/red]")
                console.print(" - [orange]rien faire[/orange]")
                action = console.input("[bold blue]Que faites-vous ? [/bold blue]").lower()
                pause_phase()

                if action == "attaquer":
                    # Attaque du joueur
                    player.attack(enemy)
                    pause_phase()
                    if enemy.is_alive():
                        console.print(f"[bold red]{enemy.name} riposte après l'attaque de {player.name} ![/bold red]")
                        enemy.attack(player)
                        pause_phase()
                elif action == "rien faire":
                    console.print(f"[yellow]{player.name} a choisi de ne rien faire...[/yellow]")
                    pause_phase()
                elif action == "inventaire":
                    manage_inventory(player)
                    continue
                elif action == "abandonner":
                    console.print(f"[bold red]{player.name} a abandonné la bataille...[/bold red]")
                    pause_phase()
                    return False
                else:
                    print_invalid_action_message()
                    pause_phase()
                    continue

        # Si l'ennemi est encore en vie, il attaque un personnage aléatoire
        if enemy.is_alive():
            target = random.choice([p for p in players if p.is_alive()])
            console.print(f"\n[bold red]{enemy.name} attaque spontanément {target.name} ![/bold red]")
            pause_phase()
            enemy.attack(target)
            pause_phase()

        # Vérification de la fin du combat
        if all(not player.is_alive() for player in players):
            print_defeat_message(players, enemy)
            pause_phase()
            return False

    if enemy.is_alive():
        print_defeat_message(players, enemy)
        return False
    else:
        print_victory_message(players, enemy)
        return True


def main():
    from ui import print_welcome_message, print_enemy_appearance, print_victory_message_final
    print_welcome_message()
    pause_phase()

    if print_know_classes_prompt() != 'o':
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

        while enemy.is_alive() and any(player.is_alive() for player in players):
            for player in players:
                if enemy.is_alive() and player.is_alive():
                    console.print(f"\n[bold blue]{player.name}, c'est votre tour ![/bold blue]")
                    pause_phase()
                    if not battle(players, enemy):
                        console.print("[red]L'aventure s'arrête ici...[/red]")
                        return
            if enemy.is_alive():
                target = random.choice([p for p in players if p.is_alive()])
                console.print(f"\n[bold red]{enemy.name} attaque spontanément {target.name} ![/bold red]")
                pause_phase()
                enemy.attack(target)
                pause_phase()
                if not target.is_alive():
                    console.print(f"[red]{target.name} est hors de combat ![/red]")
                    pause_phase()

        if not enemy.is_alive():
            for player in players:
                if player.is_alive():
                    player.gold += enemy.xp_reward
                    console.print(f"[bold green]{player.name} gagne {enemy.xp_reward} or ! (Total: {player.gold} or)[/bold green]")
                    pause_phase()
            if enemy.label == "boss":
                console.print("[bold magenta]GG, vous avez vaincu le Seigneur Noir ! L'aventure est terminée ![/bold magenta]")
                pause_phase()

        shop_phase(players)
        pause_phase()

    print_victory_message_final()
    pause_phase()

if __name__ == "__main__":
    main()
