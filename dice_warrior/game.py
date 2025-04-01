from character import *
from enemies import *
from dice import Dice
import random
import inspect
from rich import print  # Importation correcte de `print` de rich

def get_available_classes():
    return {name: cls for name, cls in inspect.getmembers(__import__('character'), inspect.isclass) if issubclass(cls, Character) and cls is not Character}

def describe_class(class_choice):
    descriptions = {
        "Warrior": "🪓 Warrior : Bonus de dégâts de +1,5 * dégâts à l'attaque.",
        "Mage": "🔮 Mage : Défense améliorée avec une réduction de -3 blessures. Bonus de défense : -3 blessures.",
        "Thief": "🗡️ Thief : Ignore la défense de la cible lors de l'attaque.",
        "Paladin": "🛡️ Paladin : Bénédiction pour +3 en défense.",
        "Ranger": "🏹 Ranger : Précision accrue avec +2 en dégâts à chaque attaque.",
        "Berserker": "🔥 Berserker : Bonus de dégâts basé sur les points de vie manquants.",
        "Healer": "⚕️ Healer : Peut soigner les alliés, avec des chances de guérison variant en fonction du lancer de dé.",
        "Gamester": "🎲 Gamester : Lance un dé de hasard pour infliger des dégâts aléatoires."
    }
    return descriptions.get(class_choice, "Classe non trouvée.")

def create_character():
    characters = []
    classes = get_available_classes()
    
    while True:
        name = input("[bold blue]Nom du personnage : [/bold blue]")
        print("[yellow]Choisissez une classe parmi : [/yellow]", ", ".join(classes.keys()))
        class_choice = input("[bold green]Classe : [/bold green]")
        
        if class_choice == "?":
            print("\n[bold magenta]Détails des classes disponibles :[/bold magenta]")
            for class_name in classes.keys():
                print(f"[cyan]{class_name}[/cyan]: {describe_class(class_name)}")
            continue
        
        class_choice = class_choice.capitalize()
        
        if class_choice not in classes:
            print("[bold red]Classe invalide, veuillez réessayer.[/bold red]")
            continue

        print(f"[bold green]{describe_class(class_choice)}[/bold green]")
        
        dice_color = input("[bold blue]Couleur du dé (ex: rouge, bleu, vert) : [/bold blue]")
        dice_faces = int(input("[bold blue]Nombre de faces du dé (ex: 6, 8, 10) : [/bold blue]"))
        dice = Dice(dice_color, dice_faces)
        
        max_hp = int(input("[bold blue]Entrez la valeur pour max_hp : [/bold blue]"))
        attack_value = int(input("[bold blue]Entrez la valeur pour attack_value : [/bold blue]"))
        defend_value = int(input("[bold blue]Entrez la valeur pour defend_value : [/bold blue]"))
        
        chosen_class = classes[class_choice]
        if class_choice == "Healer":
            allies = [char for char in characters]
            character = chosen_class(name, max_hp, attack_value, defend_value, dice, allies)
        else:
            character = chosen_class(name, max_hp, attack_value, defend_value, dice)
        
        characters.append(character)
        
        print("\n[bold green]✅ Personnage créé:[/bold green]")
        print(f"[yellow]Nom:[/yellow] {character.name}")
        print(f"[yellow]Classe:[/yellow] {class_choice}")
        print(f"[yellow]HP:[/yellow] {max_hp}")
        print(f"[yellow]Attaque:[/yellow] {attack_value}")
        print(f"[yellow]Défense:[/yellow] {defend_value}")
        print(f"[yellow]Dé:[/yellow] {dice.color} {dice.faces} faces")
        
        more = input("[bold blue]\nVoulez-vous créer un autre personnage ? (o/n) [/bold blue]")
        if more.lower() != 'o':
            break
    return characters

def battle(player, enemy):
    print(f"[bold green]{player.name} le {player.__class__.__name__} affronte {enemy.name} ![/bold green]")
    while player.is_alive() and enemy.is_alive():
        dmg = player.attack(enemy)  
        enemy.defend(dmg)
        if enemy.is_alive():
            dmg = enemy.attack(player)  
    
    if player.is_alive():
        print(f"[bold yellow]{player.name} a vaincu {enemy.name} ![/bold yellow]")
    else:
        print(f"[bold red]{player.name} a été vaincu par {enemy.name}...[/bold red]")

def main():
    # Ajout de debug
    print("[bold cyan]Bienvenue dans la campagne DnD![/bold cyan]")
    
    knows_classes = input("[bold magenta]Connaissez-vous le système des classes ? (o/n) : [/bold magenta]").lower()
    if knows_classes != 'o':
        print("\n[bold magenta]Voici les détails des classes disponibles :[/bold magenta]")
        classes = get_available_classes()
        for class_name in classes.keys():
            print(f"[cyan]{class_name}[/cyan]: {describe_class(class_name)}")
    print()
    
    players = create_character()
    enemies = [Goblin("Goblin", 12, 5, 2, Dice("green", 6), 10), Skeleton("Squelette", 15, 6, 2, Dice("white", 6), 15), Orc("Orc", 22, 9, 3, Dice("red", 6), 20), Troll("Troll", 30, 10, 4, Dice("blue", 6), 25), Boss("Seigneur Noir", 40, 12, 6, Dice("black", 8), 50)]
    
    print("[bold cyan]Préparez-vous à combattre![/bold cyan]")
    
    for enemy in enemies:
        if all(not player.is_alive() for player in players):
            print("[bold red]💀 Tous les héros sont morts. Game Over![/bold red]")
            return
        
        print(f"[bold yellow]⚔️ Un {enemy.label} apparaît: {enemy.name} ![/bold yellow]")
        
        for player in players:
            if player.is_alive():
                battle(player, enemy)
                if not enemy.is_alive():
                    print(f"[bold green]🎉 {enemy.name} est vaincu![/bold green]")
                    break
        
    print("[bold yellow]🏆 Félicitations! Vous avez vaincu tous les ennemis et triomphé de l'aventure![/bold yellow]")

if __name__ == "__main__":
    main()
