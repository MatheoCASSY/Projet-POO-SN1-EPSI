from dice import Dice
from rich import print
from character import Character

class Goblin(Character):
    label = "goblin"

    def compute_damages(self, roll):
        print("👹 Goblin mischief: +1 dmg")
        return super().compute_damages(roll) + 1

    def compute_defend(self, damages, roll):
        print("👹 Goblin sneakiness: -1 wounds")
        return max(0, super().compute_defend(damages, roll) - 1)

class GoblinChief(Character):
    label = "goblin chief"

    def compute_damages(self, roll):
        print("💀 Goblin Chief leadership: +2 dmg")
        return super().compute_damages(roll) + 2

    def compute_defend(self, damages, roll):
        print("💀 Goblin Chief toughness: +2 defense")
        return max(0, super().compute_defend(damages, roll) + 2)

class Boss(Character):
    label = "boss"

    def compute_damages(self, roll):
        extra_damage = roll // 2  # Boss has stronger attack scaling
        print(f"👹 Boss's wrath: +{extra_damage} dmg")
        return super().compute_damages(roll) + extra_damage

    def compute_defend(self, damages, roll):
        print("⚔️ Boss's resilience: Reduces damage taken by 5")
        return max(0, super().compute_defend(damages, roll) + 5)

class Skeleton(Character):
    label = "skeleton"

    def compute_defend(self, damages, roll):
        print("💀 Skeleton durability: -2 wounds")
        return max(0, super().compute_defend(damages, roll) - 2)

class SkeletonArcher(Character):
    label = "skeleton archer"

    def compute_damages(self, roll):
        print("🏹 Skeleton Archer precision: +2 dmg")
        return super().compute_damages(roll) + 2

    def compute_defend(self, damages, roll):
        print("🏹 Skeleton Archer agility: -1 wounds")
        return max(0, super().compute_defend(damages, roll) - 1)

class Orc(Character):
    label = "orc"

    def compute_damages(self, roll):
        print("🪓 Orc brutality: +3 dmg")
        return super().compute_damages(roll) + 3

class Troll(Character):
    label = "troll"

    def regenerate(self):
        regen = 3
        self.hp = min(self.max_hp, self.hp + regen)
        print(f"🧌 Troll regeneration: +{regen} hp")
        self.show_healthbar()

    def defend(self, damages):
        super().defend(damages)
        self.regenerate()

if __name__ == "__main__":
    print("\n")

    goblin_1 = Goblin("Goblin Grunt", 12, 5, 2, Dice("green", 6))
    goblin_2 = Goblin("Goblin Sneak", 10, 6, 1, Dice("green", 6))
    boss = Boss("Dark Overlord", 40, 12, 6, Dice("black", 8))
    skeleton = Skeleton("Bone Walker", 15, 6, 2, Dice("white", 6))
    skeleton_archer = SkeletonArcher("Undead Marksman", 14, 7, 1, Dice("white", 6))
    orc = Orc("Orc Berserker", 22, 9, 3, Dice("red", 6))
    troll = Troll("Forest Troll", 30, 10, 4, Dice("blue", 6))

    print(goblin_1)
    print(goblin_2)
    print(boss)
    print(skeleton)
    print(skeleton_archer)
    print(orc)
    print(troll)

    goblin_1.attack(boss)
    boss.attack(goblin_1)
    goblin_2.attack(boss)
    skeleton.attack(orc)
    skeleton_archer.attack(troll)
    orc.attack(troll)
    troll.attack(skeleton)

while all(enemy.is_alive() for enemy in [goblin_1, goblin_2, boss, skeleton, skeleton_archer, orc, troll]):
    goblin_1.attack(boss)
    goblin_2.attack(boss)
    skeleton.attack(orc)
    skeleton_archer.attack(troll)
    orc.attack(troll)
    troll.attack(skeleton)
    boss.attack(goblin_1)
