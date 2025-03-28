from dice import Dice
from rich import print
from character import *

class Enemy:
    label = "enemy"

    def __init__(self, name, max_hp, attack_value, defend_value, dice, xp_reward):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.dice = dice
        self.xp_reward = xp_reward

    def __str__(self):
        return f"I'm {self.name} the {self.label}."

    def is_alive(self):
        return self.hp > 0

    def decrease_hp(self, amount):
        self.hp = max(0, self.hp - amount)
        self.show_healthbar()

    def show_healthbar(self):
        print(f"[{'❤️' * self.hp}{'♡' * (self.max_hp - self.hp)}] {self.hp}/{self.max_hp} hp")
        print("\n")

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(f"{self.name} attacks with {damages} damages ({self.attack_value} atk + {roll} rng)")
        target.defend(damages)

    def defend(self, damages):
        roll = self.dice.roll()
        wounds = self.compute_defend(damages, roll)
        print(f"{self.name} defends against {damages} and takes {wounds} wounds ({damages} dmg - {self.defend_value} def - {roll} rng)")
        self.decrease_hp(wounds)
        
        if not self.is_alive():
            self.drop_xp()

    def compute_damages(self, roll):
        return self.attack_value + roll

    def compute_defend(self, damages, roll):
        return max(0, damages - self.defend_value - roll)

    def drop_xp(self):
        print(f"🎉 {self.name} is defeated! The player gains {self.xp_reward} XP!")
        print("\n")

class Goblin(Enemy):
    label = "goblin"

    def compute_damages(self, roll):
        print("👹 Goblin mischief: +1 dmg")
        return super().compute_damages(roll) + 1

    def compute_defend(self, damages, roll):
        print("👹 Goblin sneakiness: -1 wounds")
        return max(0, super().compute_defend(damages, roll) - 1)


class GoblinChief(Enemy):
    label = "goblin chief"

    def compute_damages(self, roll):
        print("💀 Goblin Chief leadership: +2 dmg")
        return super().compute_damages(roll) + 2

    def compute_defend(self, damages, roll):
        print("💀 Goblin Chief toughness: +2 defense")
        return max(0, super().compute_defend(damages, roll) + 2)


class Boss(Enemy):
    label = "boss"

    def compute_damages(self, roll):
        extra_damage = roll // 2
        print(f"👹 Boss's wrath: +{extra_damage} dmg")
        return super().compute_damages(roll) + extra_damage

    def compute_defend(self, damages, roll):
        print("⚔️ Boss's resilience: Reduces damage taken by 5")
        return max(0, super().compute_defend(damages, roll) + 5)

class Skeleton(Enemy):
    label = "skeleton"

    def compute_defend(self, damages, roll):
        print("💀 Skeleton durability: -2 wounds")
        return max(0, super().compute_defend(damages, roll) - 2)


class Orc(Enemy):
    label = "orc"

    def compute_damages(self, roll):
        print("🪓 Orc brutality: +3 dmg")
        return super().compute_damages(roll) + 3


class Troll(Enemy):
    label = "troll"

    def regenerate(self):
        regen = 3
        self.hp = min(self.max_hp, self.hp + regen)
        print(f"🧌 Troll regeneration: +{regen} hp")
        self.show_healthbar()

    def defend(self, damages):
        super().defend(damages)
        self.regenerate()


# Exemple
if __name__ == "__main__":
    print("\n")

    goblin_1 = Goblin("Goblin Grunt", 12, 5, 2, Dice("green", 6), xp_reward=10)
    goblin_2 = Goblin("Goblin Sneak", 10, 6, 1, Dice("green", 6), xp_reward=15)
    boss = Boss("Dark Overlord", 40, 12, 6, Dice("black", 8), xp_reward=50)
    skeleton = Skeleton("Bone Walker", 15, 6, 2, Dice("white", 6), xp_reward=20)
    orc = Orc("Orc Berserker", 22, 9, 3, Dice("red", 6), xp_reward=25)
    troll = Troll("Forest Troll", 30, 10, 4, Dice("blue", 6), xp_reward=30)

    enemies = [goblin_1, goblin_2, boss, skeleton, orc, troll]

    goblin_1.attack(boss)
    boss.attack(goblin_1)
    goblin_2.attack(boss)
    skeleton.attack(orc)
    orc.attack(troll)
    troll.attack(skeleton)

    while all(enemy.is_alive() for enemy in enemies):
        for enemy in enemies:
            if enemy.is_alive():
                target = enemies[0]
                enemy.attack(target)
                target.attack(enemy)
