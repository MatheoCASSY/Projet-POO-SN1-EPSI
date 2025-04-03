from dice import Dice
from rich import print
from character import Character

class Enemy:
    label = "enemy"

    def __init__(self, name: str, max_hp: int, attack_value: int, defend_value: int, dice: Dice, xp_reward: int = 15):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.dice = dice
        self.xp_reward = xp_reward

    def __str__(self) -> str:
        return f"I'm {self.name} the {self.label}."

    def is_alive(self) -> bool:
        return self.hp > 0

    def decrease_hp(self, amount: int):
        self.hp = max(0, self.hp - amount)
        self.show_healthbar()

    def show_healthbar(self):
        print(f"[{'❤️' * self.hp}{'♡' * (self.max_hp - self.hp)}] {self.hp}/{self.max_hp} hp\n")

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        if damages is not None:
            print(f"{self.name} attaque avec {damages} dommages ({self.attack_value} atk + {roll} rng)")
            target.defend(damages)
        else:
            print(f"Attack failed! {self.name} could not calculate damages.")

    def defend(self, damages: int):
        roll = self.dice.roll()
        wounds = self.compute_defend(damages, roll)
        print(f"{self.name} défend contre {damages} et subit {wounds} blessures ({damages} dmg - {self.defend_value} def - {roll} rng)")
        self.decrease_hp(wounds)
        if not self.is_alive():
            self.drop_xp()

    def compute_damages(self, roll: int) -> int:
        if roll is None:
            print(f"{self.name} failed to roll a dice!")
            return 0
        return self.attack_value + roll

    def compute_defend(self, damages: int, roll: int) -> int:
        if damages is None:
            print(f"{self.name} cannot compute defense with invalid damages!")
            return 0
        return max(0, damages - self.defend_value - roll)

    def drop_xp(self):
        print(f"🎉 {self.name} est vaincu ! Le joueur gagne {self.xp_reward} XP !\n")

class Goblin(Enemy):
    label = "goblin"

    def compute_damages(self, roll: int) -> int:
        print("👹 Goblin mischief: +1 dmg")
        return super().compute_damages(roll) + 1

    def compute_defend(self, damages: int, roll: int) -> int:
        print("👹 Goblin sneakiness: -1 wounds")
        return max(0, super().compute_defend(damages, roll) - 1)

class GoblinChief(Enemy):
    label = "goblin chief"

    def compute_damages(self, roll: int) -> int:
        print("💀 Goblin Chief leadership: +2 dmg")
        return super().compute_damages(roll) + 2

    def compute_defend(self, damages: int, roll: int) -> int:
        print("💀 Goblin Chief toughness: +2 defense")
        return max(0, super().compute_defend(damages, roll) + 2)

class Boss(Enemy):
    label = "boss"

    def compute_damages(self, roll: int) -> int:
        extra_damage = roll // 2
        print(f"👹 Boss's wrath: +{extra_damage} dmg")
        return super().compute_damages(roll) + extra_damage

    def compute_defend(self, damages: int, roll: int) -> int:
        print("⚔️ Boss's resilience: Réduit les dégâts subis de 5")
        return max(0, super().compute_defend(damages, roll) + 5)

class Skeleton(Enemy):
    label = "skeleton"

    def compute_defend(self, damages: int, roll: int) -> int:
        print("💀 Skeleton durability: -2 wounds")
        return max(0, super().compute_defend(damages, roll) - 2)

class Orc(Enemy):
    label = "orc"

    def compute_damages(self, roll: int) -> int:
        print("🪓 Orc brutality: +3 dmg")
        return super().compute_damages(roll) + 3

class Troll(Enemy):
    label = "troll"

    def regenerate(self):
        regen = 3
        self.hp = min(self.max_hp, self.hp + regen)
        print(f"🧌 Troll regeneration: +{regen} hp")
        self.show_healthbar()

    def defend(self, damages: int):
        super().defend(damages)
        self.regenerate()
