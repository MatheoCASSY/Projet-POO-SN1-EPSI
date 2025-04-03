from rich import print
from rich.console import Console

console = Console()

def print_healthbar(character):
    bar = f"[{'❤️' * character.hp}{'♡' * (character.max_hp - character.hp)}] {character.hp}/{character.max_hp} hp"
    print(bar + "\n")

def print_xpbar(character):
    percent = int((character.xp / character.xp_needed) * 20)
    print(f"XP: [{'★' * percent}{'✩' * (20 - percent)}] {character.xp}/{character.xp_needed} xp")

def print_level_up(character):
    print(f"\n🎉 {character.name} monte au niveau {character.level} ! 🎉")
    print_xpbar(character)

def print_stat_assignment(character):
    print("\n📊 Attribuez vos points de stats :")
    options = ["1. +5 HP max", "2. +2 ATK", "3. +2 DEF"]
    for opt in options:
        print(opt)

def print_invalid_choice():
    print("❌ Choix invalide, aucun bonus attribué.")

def print_battle_intro(player, enemy):
    console.print(f"[bold green]{player.name} le {player.__class__.__name__} affronte {enemy.name} ![/bold green]")

def print_health_bars(player, enemy):
    player.show_healthbar()
    enemy.show_healthbar()

def print_invalid_action_message():
    console.print("[bold red]Action invalide, veuillez réessayer.[/bold red]")

def print_victory_message(player, enemy):
    console.print(f"[bold yellow]{player.name} a vaincu {enemy.name} ![/bold yellow]")

def print_defeat_message(player, enemy):
    console.print(f"[bold red]{player.name} a été vaincu par {enemy.name}...[/bold red]")

def print_game_over_message():
    console.print("[bold red]💀 Tous les héros sont morts. Game Over![/bold red]")

def print_enemy_appearance(enemy):
    console.print(f"[bold yellow]⚔️ Un {enemy.label} apparaît: {enemy.name} ![/bold yellow]")

def print_victory_message_final():
    console.print("[bold yellow]🏆 Félicitations! Vous avez vaincu tous les ennemis et triomphé de l'aventure![/bold yellow]")

def print_class_choice_prompt(classes):
    console.print("[yellow]Choisissez une classe parmi : [/yellow]", ", ".join(classes.keys()))

def print_invalid_class_message():
    console.print("[bold red]Classe invalide, veuillez réessayer.[/bold red]")

def print_character_creation_prompt(name, class_choice, max_hp, attack_value, defend_value, dice):
    console.print(f"\n[bold green]✅ Personnage créé:[/bold green]")
    console.print(f"[yellow]Nom:[/yellow] {name}")
    console.print(f"[yellow]Classe:[/yellow] {class_choice}")
    console.print(f"[yellow]HP:[/yellow] {max_hp}")
    console.print(f"[yellow]Attaque:[/yellow] {attack_value}")
    console.print(f"[yellow]Défense:[/yellow] {defend_value}")
    console.print(f"[yellow]Dé:[/yellow] {dice.color} {dice.faces} faces")

def print_more_characters_prompt():
    return console.input("[bold blue]\nVoulez-vous créer un autre personnage ? (o/n) [/bold blue]").lower()

def print_know_classes_prompt():
    return console.input("[bold magenta]Connaissez-vous le système des classes ? (o/n) : [/bold magenta]").lower()

def print_class_details(classes):
    console.print("\n[bold magenta]Voici les détails des classes disponibles :[/bold magenta]")
    for class_name in classes.keys():
        console.print(f"[cyan]{class_name}[/cyan]: {describe_class(class_name)}")

def describe_class(class_choice):
    descriptions = {
        "Warrior": "🪓 Warrior : Bonus de dégâts de +1,5 * dégâts à l'attaque.",
        "Mage": "🔮 Mage : Défense améliorée avec une réduction de -3 blessures.",
        "Thief": "🗡️ Thief : Ignore la défense de la cible lors de l'attaque.",
        "Paladin": "🛡️ Paladin : Bénédiction pour +3 en défense.",
        "Ranger": "🏹 Ranger : Précision accrue avec +2 en dégâts à chaque attaque.",
        "Berserker": "🔥 Berserker : Bonus de dégâts basé sur les points de vie manquants.",
        "Healer": "⚕️ Healer : Peut soigner les alliés en fonction du lancer de dé.",
        "Gamester": "🎲 Gamester : Lance un dé pour infliger des dégâts aléatoires."
    }
    return descriptions.get(class_choice, "Classe non trouvée.")

# Fonctions pour la gestion des objets

def print_durability(item):
    bar = f"[{'🛡️ ' * item.durability}{'⛉ ' * (item.durability_max - item.durability)}] {item.durability}/{item.durability_max} durabilité -----> {item.name}\n"
    print(bar)

def print_item_broken(item):
    print(f"⚠️ {item.name} est cassé et ne fournit aucun bonus !")

def print_item_removed(character, item):
    print(f"⚠️ {character.name} a retiré {item.name}, perdant -{item.defend_value} DEF et -{item.attack_value} ATK !")

def print_welcome_message():
    console.print("[bold cyan]Bienvenue dans la campagne DnD![/bold cyan]")
