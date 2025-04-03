# 📜 Documentation du Code

## 📖 Table des Matières
1. [📌 Introduction](#introduction)
2. [🎮 game.py](#gamepy)
   - [⏸️ pause_phase()](#pause_phase)
   - [📜 get_available_classes()](#get_available_classes)
   - [🛡️ create_character()](#create_character)
   - [🎒 manage_inventory(character)](#manage_inventorycharacter)
   - [🛍️ shop_phase(character)](#shop_phasecharacter)
   - [⚔️ battle()](#battle)
   - [🕹️ main()](#main)
3. [💀 GameOver.py](#gameoverpy)
   - [🎭 display_game_over()](#display_game_over)
4. [🎒 inventaire.py](#inventairepy)
   - [➕ add_item(item)](#add_itemitem)
   - [➖ remove_item()](#remove_item)
   - [🛡️ equip_item(character)](#equip_itemcharacter)
   - [❌ unequip_item(character)](#unequip_itemcharacter)
   - [📜 show_inventory()](#show_inventory)
   - [🛡️ show_equipped()](#show_equipped)
5. [🛠️ item.py](#itempy)
   - [🔄 Universal_Item](#universal_item)
   - [🧪 Heal_potion](#heal_potion)
   - [⛑️ Helmet](#helmet)
   - [⚔️ Sword](#sword)
   - [🛡️ Shield](#shield)
   - [🔮 Amulet](#amulet)
   - [📉 decrease_durability(amount)](#decrease_durabilityamount)
   - [🛠️ use(character)](#usecharacter)
   - [📈 apply_bonus(character)](#apply_bonuscharacter)
   - [📉 remove_bonus(character)](#remove_bonuscharacter)
   - [🔍 show_durability()](#show_durability)
6. [🏪 shop.py](#shoppy)
   - [🛒 show_shop(character)](#show_shopcharacter)
7. [🖥️ ui.py](#uipy)
   - [💻 console()](#console)
   - [📉 print_durability(item)](#print_durabilityitem)
   - [💔 print_item_broken(item)](#print_item_brokenitem)
   - [❌ print_item_removed(character, item)](#print_item_removedcharacter-item)
   - [💬 display_message(message)](#display_messagemessage)
   - [⌨️ prompt_input(prompt)](#prompt_inputprompt)
   - [🧹 clear_screen()](#clear_screen)
   - [📜 show_menu(options)](#show_menuoptions)
   - [🎯 get_user_choice()](#get_user_choice)
   - [✨ print_healthbar(character)](#print_healthbarcharacter)
   - [📊 print_xpbar(character)](#print_xpbarcharacter)
   - [🚀 print_level_up(character)](#print_level_upcharacter)
   - [📝 print_stat_assignment(character)](#print_stat_assignmentcharacter)
   - [❗ print_invalid_choice()](#print_invalid_choice)
   - [🚫 print_invalid_class_message()](#print_invalid_class_message)
   - [📝 print_character_creation_prompt(name, class_choice, max_hp, attack_value, defend_value, dice)](#print_character_creation_prompt)
   - [👾 print_enemy_appearance(enemy)](#print_enemy_appearanceenemy)
   - [💀 print_game_over_message()](#print_game_over_message)
   - [🏆 print_victory_message_final()](#print_victory_message_final)
   - [🔍 describe_class(class_name)](#describe_classclassname)
   - [❓ print_class_choice_prompt()](#print_class_choice_prompt)
   - [📚 print_know_classes_prompt()](#print_know_classes_prompt)
   - [📝 print_class_details(classes)](#print_class_detailsclasses)
   - [🎬 print_battle_intro(player, enemy)](#print_battle_intropalyerenemy)
   - [📊 print_health_bars(player, enemy)](#print_health_barsplayerenemy)
   - [⚠️ print_invalid_action_message()](#print_invalid_action_message)
   - [🎉 print_victory_message(player, enemy)](#print_victory_messageplayerenemy)
   - [💔 print_defeat_message(player, enemy)](#print_defeat_messageplayerenemy)
   - [👋 print_welcome_message()](#print_welcome_message)

---

## 📌 Introduction
Ce projet est un jeu textuel conçu pour offrir une expérience interactive de création de personnage, de combats contre divers ennemis et de gestion d'inventaire. Chaque module a été pensé pour séparer les responsabilités : la logique de jeu, la gestion des objets, la boutique, et l'interface utilisateur. L'objectif est de rendre le code modulaire et facilement extensible.

---

## 🎮 game.py

### ⏸️ pause_phase()
**Comment :**  
Cette fonction ajoute une pause entre différentes phases du jeu en affichant quelques lignes vides et en appelant `time.sleep(1)`. Cela permet d'améliorer la lisibilité et de donner du temps à l'utilisateur pour suivre l'évolution du jeu.  
**Pourquoi :**  
Pour éviter que le texte ne s'affiche trop rapidement, ce qui pourrait nuire à la compréhension des événements du jeu.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 📜 get_available_classes()
**Comment :**  
Elle utilise le module `inspect` pour récupérer dynamiquement toutes les sous-classes de la classe `Character` définies dans le module `character`.  
**Pourquoi :**  
Cette approche rend le système de création de personnage flexible et permet d'ajouter facilement de nouvelles classes sans modifier la logique de sélection.

- **Paramètres** : Aucun  
- **Retourne** : `list[str]` ou `dict[str, type]` (selon l'implémentation, il peut s'agir d'une liste ou d'un dictionnaire associant le nom de la classe à sa référence)

---

### 🛡️ create_character()
**Comment :**  
Cette fonction interagit avec l'utilisateur pour créer un personnage. Elle demande le nom, la classe, et les valeurs initiales (HP, attaque, défense, etc.), puis crée une instance de la classe choisie.  
**Pourquoi :**  
Pour offrir une personnalisation du personnage et intégrer les choix de l'utilisateur dès le début de la partie.

- **Paramètres** : Aucun  
- **Retourne** : `Character` (l'instance du personnage créé)

---

### 🎒 manage_inventory(character)
**Comment :**  
Elle affiche un menu permettant au joueur de gérer l'inventaire (voir, équiper, déséquiper, jeter des objets) via des entrées utilisateur.  
**Pourquoi :**  
Permet d'interagir avec l'inventaire du personnage de manière interactive et de gérer l'équipement pour améliorer les statistiques du personnage.

- **Paramètres** :  
  - `Character character` — L'instance du personnage dont l'inventaire est géré  
- **Retourne** : `None`

---

### 🛍️ shop_phase(character)
**Comment :**  
Cette fonction propose au joueur de visiter la boutique pour acheter des points de vie (HP) en fonction de l'or accumulé. Elle affiche les options et met à jour les ressources du personnage.  
**Pourquoi :**  
Permet d'intégrer une dimension économique au jeu, offrant des moyens de renforcer le personnage entre les combats.

- **Paramètres** :  
  - `Character character` — Le personnage effectuant l'achat  
- **Retourne** : `None`

---

### ⚔️ battle()
**Comment :**  
Elle orchestre le déroulement d'un combat entre le joueur et un ennemi. La fonction gère l'alternance des tours, les actions (attaquer, gérer l'inventaire, abandonner) et la vérification de l'état de vie des participants.  
**Pourquoi :**  
C'est le cœur de la mécanique de combat du jeu, permettant d'engager et de simuler les échanges de dégâts entre le joueur et l'ennemi.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 🕹️ main()
**Comment :**  
La fonction principale qui initialise le jeu. Elle affiche un message de bienvenue, gère la création des personnages, lance les combats, et orchestre l'ensemble des phases de jeu (création, combat, boutique).  
**Pourquoi :**  
Elle sert de point d'entrée et de coordination pour l'ensemble des modules du jeu.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

## 💀 GameOver.py

### 🎭 display_game_over()
**Comment :**  
Cette fonction (ou bloc de code encapsulé en fonction) utilise la bibliothèque `pyfiglet` pour générer et afficher un ASCII art représentant le message "GAME OVER".  
**Pourquoi :**  
Pour offrir une conclusion visuelle marquante lorsque le joueur perd la partie.

- **Dépendance** : `pyfiglet`  
- **Retourne** : `None`

---

## 🏪 shop.py

### 🛒 show_shop(character)
**Comment :**  
La fonction affiche le contenu de la boutique, présente le prix des HP et gère les achats en vérifiant si le personnage a suffisamment d'or.  
**Pourquoi :**  
Elle permet d'intégrer une interaction économique dans le jeu, offrant au joueur la possibilité de renforcer son personnage via l'achat de ressources.

- **Paramètres** :  
  - `Character character` — Le personnage qui visite la boutique  
- **Retourne** : `None`

---

## 🎒 inventaire.py

### ➕ add_item(item)
**Comment :**  
Ajoute un objet à la liste d'items de l'inventaire et affiche un message de confirmation.  
**Pourquoi :**  
Pour enrichir l'inventaire du personnage et lui fournir des objets utilisables durant le jeu.

- **Paramètres** :  
  - `Item item` — L'objet à ajouter  
- **Retourne** : `None`

---

### ➖ remove_item()
**Comment :**  
Permet au joueur de choisir et retirer un objet de l'inventaire via une saisie (le nom de l'objet).  
**Pourquoi :**  
Pour offrir la possibilité de gérer l'espace d'inventaire et de se débarrasser des objets inutiles ou encombrants.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 🛡️ equip_item(character)
**Comment :**  
Cette fonction permet de sélectionner un objet dans l'inventaire et de l'équiper sur le personnage, en appliquant immédiatement ses bonus.  
**Pourquoi :**  
Pour améliorer les statistiques du personnage grâce aux équipements et personnaliser son style de jeu.

- **Paramètres** :  
  - `Character character` — Le personnage qui équipe l'objet  
- **Retourne** : `None`

---

### ❌ unequip_item(character)
**Comment :**  
Permet de retirer un objet équipé du personnage et de retirer les bonus qui lui étaient appliqués.  
**Pourquoi :**  
Pour gérer le changement d'équipement et ajuster les statistiques du personnage en conséquence.

- **Paramètres** :  
  - `Character character` — Le personnage qui déséquipe l'objet  
- **Retourne** : `None`

---

### 📜 show_inventory()
**Comment :**  
Affiche sous forme de liste tous les objets présents dans l'inventaire du personnage.  
**Pourquoi :**  
Pour permettre au joueur de visualiser facilement son stock d'objets et prendre des décisions concernant leur utilisation ou leur élimination.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 🛡️ show_equipped()
**Comment :**  
Affiche la liste des objets actuellement équipés par le personnage.  
**Pourquoi :**  
Pour que le joueur connaisse les bonus actifs et les objets qui influencent les performances du personnage.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

## 🛠️ item.py

### 🔄 Universal_Item
**Comment :**  
Il s'agit de la classe de base pour tous les objets du jeu. Elle définit des attributs communs tels que le nom, la durabilité maximale, et les bonus éventuels (attaque, défense, soin).  
**Pourquoi :**  
Pour standardiser le comportement et les propriétés des objets, facilitant ainsi leur gestion et leur utilisation dans le jeu.

- **Attributs** :  
  - `name`  
  - `durability_max`  
  - `attack_value`  
  - `defend_value`  
  - `heal_amount`  
- **Retourne** : `None` (en tant que constructeur)

---

### 📉 decrease_durability(amount)
**Comment :**  
Réduit la durabilité de l'objet d'un montant donné, vérifiant que la durabilité ne descend pas en dessous de zéro, et appelle éventuellement une fonction d'affichage pour montrer l'état de l'objet.  
**Pourquoi :**  
Pour simuler l'usure des objets et rendre leur utilisation limitée dans le temps, ce qui ajoute une dimension stratégique.

- **Paramètres** :  
  - `int amount` — La quantité de durabilité à retirer  
- **Retourne** : `None`

---

### 🛠️ use(character)
**Comment :**  
Cette méthode permet d'utiliser l'objet sur un personnage (par exemple, soigner avec une potion ou appliquer un bonus d'arme). Selon l'objet, son état peut changer (comme la durabilité qui diminue).  
**Pourquoi :**  
Pour appliquer l'effet spécifique de l'objet et permettre son utilisation dans différentes situations de jeu.

- **Paramètres** :  
  - `Character character` — La cible de l'utilisation  
- **Retourne** : `None`

---

### 📈 apply_bonus(character)
**Comment :**  
Applique les bonus (ajouts aux valeurs d'attaque et de défense) de l'objet sur le personnage. Cette méthode modifie directement les statistiques du personnage.  
**Pourquoi :**  
Pour offrir un avantage stratégique au joueur en équipant des objets qui améliorent ses performances durant les combats.

- **Paramètres** :  
  - `Character character` — Le personnage qui reçoit les bonus  
- **Retourne** : `None`

---

### 📉 remove_bonus(character)
**Comment :**  
Inverse l'effet de `apply_bonus`, en retirant les bonus qui avaient été appliqués au personnage lorsque l'objet était équipé.  
**Pourquoi :**  
Pour rétablir les statistiques du personnage lorsqu'il se déséquipe d'un objet, permettant ainsi un changement d'équipement dynamique.

- **Paramètres** :  
  - `Character character` — Le personnage dont les bonus doivent être retirés  
- **Retourne** : `None`

---

### 🔍 show_durability()
**Comment :**  
Affiche l'état actuel de la durabilité de l'objet, souvent sous forme de barre ou de compteur.  
**Pourquoi :**  
Pour informer le joueur de l'état d'usure de l'objet et l'aider à décider s'il doit le remplacer ou l'utiliser avant qu'il ne soit inutilisable.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

## 🖥️ ui.py

### 💻 console()
**Comment :**  
Retourne ou initialise un gestionnaire de console interactif (souvent basé sur une bibliothèque comme Rich).  
**Pourquoi :**  
Pour centraliser les interactions avec la console, permettant des affichages colorés et une meilleure gestion des entrées/sorties.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 📉 print_durability(item)
**Comment :**  
Affiche la durabilité de l'objet dans la console, ce qui permet au joueur de voir l'état de l'équipement.  
**Pourquoi :**  
Pour fournir un feedback visuel immédiat sur l'état de l'objet et aider à la gestion de l'inventaire.

- **Paramètres** :  
  - `Item item` — L'objet dont la durabilité est affichée  
- **Retourne** : `None`

---

### 💔 print_item_broken(item)
**Comment :**  
Affiche un message spécifique indiquant que l'objet est cassé ou inutilisable.  
**Pourquoi :**  
Pour avertir le joueur que l'objet ne peut plus être utilisé et qu'il doit éventuellement le remplacer.

- **Paramètres** :  
  - `Item item` — L'objet concerné  
- **Retourne** : `None`

---

### ❌ print_item_removed(character, item)
**Comment :**  
Affiche un message confirmant que l'objet a été retiré de l'équipement du personnage, souvent suite à une désélection ou à une usure complète.  
**Pourquoi :**  
Pour informer le joueur de la modification de l'état de l'inventaire ou de l'équipement.

- **Paramètres** :  
  - `Character character` — Le personnage concerné  
  - `Item item` — L'objet retiré  
- **Retourne** : `None`

---

### 💬 display_message(message)
**Comment :**  
Affiche un message stylisé sur la console. La fonction peut appliquer des formats ou des couleurs pour mettre en avant l'information.  
**Pourquoi :**  
Pour communiquer efficacement avec le joueur, que ce soit pour des instructions, des alertes ou des notifications.

- **Paramètres** :  
  - `str message` — Le message à afficher  
- **Retourne** : `None`

---

### ⌨️ prompt_input(prompt)
**Comment :**  
Affiche un message d'invite et récupère la saisie de l'utilisateur.  
**Pourquoi :**  
Pour permettre une interaction dynamique, recueillir des choix ou des informations auprès du joueur.

- **Paramètres** :  
  - `str prompt` — Le message d'invite  
- **Retourne** : `str` — La réponse saisie par l'utilisateur

---

### 🧹 clear_screen()
**Comment :**  
Efface l'écran de la console afin de présenter une interface propre et faciliter la lecture des nouvelles informations.  
**Pourquoi :**  
Pour améliorer l'expérience utilisateur en supprimant les anciens messages et en mettant en avant les informations actuelles.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 📜 show_menu(options)
**Comment :**  
Affiche un menu interactif sous forme de liste d'options numérotées, permettant au joueur de voir et de choisir parmi plusieurs actions possibles.  
**Pourquoi :**  
Pour guider l'utilisateur dans ses choix et simplifier la navigation dans le jeu.

- **Paramètres** :  
  - `list[str] options` — La liste des options à afficher  
- **Retourne** : `None`

---

### 🎯 get_user_choice()
**Comment :**  
Demande à l'utilisateur de choisir une option (par exemple via une saisie) et retourne le choix effectué.  
**Pourquoi :**  
Pour capturer l'interaction de l'utilisateur et exécuter l'action correspondante dans le jeu.

- **Paramètres** : Aucun  
- **Retourne** : `str` — Le choix de l'utilisateur

---

### ✨ print_healthbar(character)
**Comment :**  
Affiche visuellement la barre de vie du personnage dans la console, indiquant son état de santé actuel par rapport à son maximum.  
**Pourquoi :**  
Pour donner au joueur une représentation immédiate de sa vitalité et l'aider à prendre des décisions en combat.

- **Paramètres** :  
  - `Character character` — Le personnage dont la barre de vie est affichée  
- **Retourne** : `None`

---

### 📊 print_xpbar(character)
**Comment :**  
Affiche la barre d'expérience du personnage, montrant la progression vers le prochain niveau.  
**Pourquoi :**  
Pour informer le joueur de sa progression et l'encourager à continuer à combattre pour améliorer son niveau.

- **Paramètres** :  
  - `Character character` — Le personnage dont la barre d'XP est affichée  
- **Retourne** : `None`

---

### 🚀 print_level_up(character)
**Comment :**  
Affiche un message de félicitations indiquant que le personnage a gagné un niveau et qu'il va bénéficier d'une amélioration.  
**Pourquoi :**  
Pour renforcer la satisfaction du joueur et signaler une amélioration de ses statistiques.

- **Paramètres** :  
  - `Character character` — Le personnage ayant gagné un niveau  
- **Retourne** : `None`

---

### 📝 print_stat_assignment(character)
**Comment :**  
Affiche un prompt permettant au joueur d'attribuer des points de statistiques (HP, attaque, défense) après un level-up.  
**Pourquoi :**  
Pour offrir une personnalisation supplémentaire et permettre au joueur d'adapter son personnage à son style de jeu.

- **Paramètres** :  
  - `Character character` — Le personnage en cours de level-up  
- **Retourne** : `None`

---

### ❗ print_invalid_choice()
**Comment :**  
Affiche un message d'erreur indiquant que l'entrée de l'utilisateur n'est pas valide.  
**Pourquoi :**  
Pour aider l'utilisateur à corriger son choix et garantir que le jeu reçoit des entrées correctes.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 🚫 print_invalid_class_message()
**Comment :**  
Affiche un message d'erreur spécifique lorsque l'utilisateur choisit une classe qui n'existe pas ou est invalide.  
**Pourquoi :**  
Pour guider l'utilisateur dans le choix d'une classe valide lors de la création du personnage.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 📝 print_character_creation_prompt(name, class_choice, max_hp, attack_value, defend_value, dice)
**Comment :**  
Affiche un récapitulatif de la création du personnage avec tous ses attributs et le dé choisi, confirmant ainsi la configuration initiale.  
**Pourquoi :**  
Pour permettre au joueur de vérifier et valider les informations de son personnage avant de commencer l'aventure.

- **Paramètres** :  
  - `str name` — Nom du personnage  
  - `str class_choice` — Classe choisie par le joueur  
  - `int max_hp` — Points de vie maximum  
  - `int attack_value` — Valeur d'attaque initiale  
  - `int defend_value` — Valeur de défense initiale  
  - `Dice dice` — Instance du dé utilisé pour les actions aléatoires  
- **Retourne** : `None`

---

### 👾 print_enemy_appearance(enemy)
**Comment :**  
Affiche un message indiquant l'apparition d'un ennemi dans le jeu.  
**Pourquoi :**  
Pour signaler au joueur le début d'un nouveau combat et créer une ambiance immersive.

- **Paramètres** :  
  - `Enemy enemy` — L'ennemi qui apparaît  
- **Retourne** : `None`

---

### 💀 print_game_over_message()
**Comment :**  
Affiche le message de fin de partie lorsque tous les personnages sont vaincus ou que le joueur abandonne.  
**Pourquoi :**  
Pour conclure l'expérience de jeu en informant le joueur de sa défaite.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 🏆 print_victory_message_final()
**Comment :**  
Affiche un message final de victoire, souvent lors de la défaite du boss final ou la fin de l'aventure.  
**Pourquoi :**  
Pour récompenser le joueur et marquer la fin de la campagne avec un sentiment d'accomplissement.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 🔍 describe_class(class_name)
**Comment :**  
Retourne une description textuelle de la classe de personnage (ses forces, faiblesses, et rôle dans le jeu).  
**Pourquoi :**  
Pour aider le joueur à comprendre les différences entre les classes et à faire un choix éclairé lors de la création de son personnage.

- **Paramètres** :  
  - `str class_name` — Le nom de la classe  
- **Retourne** : `str` — La description associée

---

### ❓ print_class_choice_prompt()
**Comment :**  
Affiche une invite demandant à l'utilisateur de choisir une classe parmi celles disponibles.  
**Pourquoi :**  
Pour guider l'utilisateur lors de la création du personnage et s'assurer qu'il sélectionne une classe valide.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 📚 print_know_classes_prompt()
**Comment :**  
Affiche une invite pour demander si l'utilisateur souhaite en savoir plus sur les classes disponibles, souvent avec l'option "?" pour afficher des détails.  
**Pourquoi :**  
Pour offrir plus d'informations et aider le joueur à comprendre les options avant de faire son choix.

- **Paramètres** : Aucun  
- **Retourne** : `str` — La réponse de l'utilisateur

---

### 📝 print_class_details(classes)
**Comment :**  
Affiche les détails de toutes les classes disponibles, en itérant sur un dictionnaire ou une liste des classes et en présentant leurs caractéristiques.  
**Pourquoi :**  
Pour fournir au joueur une vue d'ensemble complète des classes et l'aider dans sa décision de création de personnage.

- **Paramètres** :  
  - `dict[str, type] classes` — Dictionnaire des classes disponibles  
- **Retourne** : `None`

---

### 🎬 print_battle_intro(player, enemy)
**Comment :**  
Affiche une introduction au combat en présentant le joueur et l'ennemi, souvent avec un effet dramatique.  
**Pourquoi :**  
Pour créer une ambiance immersive et signaler le début d'un affrontement important dans le jeu.

- **Paramètres** :  
  - `Character player` — Le joueur  
  - `Enemy enemy` — L'ennemi  
- **Retourne** : `None`

---

### 📊 print_health_bars(player, enemy)
**Comment :**  
Affiche côte à côte les barres de vie du joueur et de l'ennemi pour visualiser l'état de chacun avant et après les échanges d'attaques.  
**Pourquoi :**  
Pour offrir une représentation visuelle claire de l'évolution de la santé des participants durant le combat.

- **Paramètres** :  
  - `Character player` — Le joueur  
  - `Enemy enemy` — L'ennemi  
- **Retourne** : `None`

---

### ⚠️ print_invalid_action_message()
**Comment :**  
Affiche un message d'erreur indiquant que l'action choisie durant le combat n'est pas valide.  
**Pourquoi :**  
Pour aider le joueur à comprendre qu'il doit choisir parmi les actions proposées et éviter des erreurs d'entrée.

- **Paramètres** : Aucun  
- **Retourne** : `None`

---

### 🎉 print_victory_message(player, enemy)
**Comment :**  
Affiche un message de victoire détaillé lorsque le joueur remporte un combat contre un ennemi.  
**Pourquoi :**  
Pour récompenser le joueur et signaler la progression dans le jeu.

- **Paramètres** :  
  - `Character player` — Le joueur victorieux  
  - `Enemy enemy` — L'ennemi vaincu  
- **Retourne** : `None`

---

### 💔 print_defeat_message(player, enemy)
**Comment :**  
Affiche un message de défaite lorsque le joueur perd le combat contre l'ennemi.  
**Pourquoi :**  
Pour indiquer la fin du combat et marquer la défaite du joueur, souvent en lui proposant de recommencer ou de revoir sa stratégie.

- **Paramètres** :  
  - `Character player` — Le joueur vaincu  
  - `Enemy enemy` — L'ennemi ayant remporté le combat  
- **Retourne** : `None`

---

### 👋 print_welcome_message()
**Comment :**  
Affiche un message de bienvenue au début du jeu, introduisant l'univers et préparant le joueur à l'aventure.  
**Pourquoi :**  
Pour créer une première impression positive et fournir des instructions ou des informations contextuelles dès le lancement du jeu.

- **Paramètres** : Aucun  
- **Retourne** : `None`
