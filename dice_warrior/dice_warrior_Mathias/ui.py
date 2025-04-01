from rich import print

def print_healthbar(character):
    print(f"[{'❤️' * character.hp}{'♡' * (character.max_hp - character.hp)}] {character.hp}/{character.max_hp} hp")
    print("\n")

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

def print_attack(character, target, damages, roll):
    print(f"{character.name} [red]attaque[/red] avec {damages} dommages ({character.attack_value} atk + {roll} rng)")
    target.defend(damages)

def print_defend(character, damages, wounds, roll):
    print(f"{character.name} [green]défend[/green] contre {damages} et prend {wounds} blessures ({damages} dmg - {character.defend_value} def - {roll} rng)")

def print_heal(character, target, heal_amount):
    print(f"✨ {target.name} récupère {heal_amount} HP !")
    target.show_healthbar()

def print_fail_heal():
    print("❌ Échec du soin !")

def print_success_heal(character, target, heal_amount):
    print(f"✨ {target.name} récupère {heal_amount} HP !")
    target.show_healthbar()

def print_gamble(character, target, gamble_value):
    print(f"🎲 {character.name} parie et cause {gamble_value} dommages aléatoires à {target.name}")

def print_item_equipped(character, item):
    print(f"✅ {character.name} a équipé {item.name}.")
    
def print_item_removed(character, item):
    print(f"⚠️ {character.name} a retiré {item.name}.")

def print_durability(item):
    print(f"[{'🛡️ ' * item.durability} {'⛉ ' * (item.durability_max - item.durability)}] {item.durability}/{item.durability_max} durabilité  ----->   {item.name}\n")

def print_item_equipped(character, item):
    print(f"✅ {character.name} a équipé {item.name}, gagnant +{item.defend_value} DEF et +{item.attack_value} ATK !")

def print_item_broken(item):
    print(f"⚠️ {item.name} est cassé et ne fournit aucun bonus !")

def print_item_removed(character, item):
    print(f"⚠️ {character.name} a retiré {item.name}, perdant -{item.defend_value} DEF et -{item.attack_value} ATK !")

def print_heal_potion_used(target, heal_amount):
    print(f"🧪 {target.name} utilise {target.name} et récupère {heal_amount} HP !")
    target.show_healthbar()

def print_no_need_for_heal(target, item_name):
    print(f"⚠️ {target.name} a déjà tous ses HP ! Pas besoin d'utiliser {item_name}.")