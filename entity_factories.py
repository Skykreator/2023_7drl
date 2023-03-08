from components import consumable, equippable, part
from components.ai import HostileEnemy, Neutral
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.body import Body
from components.loot_table import LootTable
import color
from entity import Actor, Item

human_heart = Item(char="q", color=color.red, name="Human Heart", part=part.Human_Heart())

human_brain = Item(char="m", color=color.red, name="Human Brain", part=part.Human_Brain())

human_leg = Item(char="L", color=color.red, name="Human Leg", part=part.Human_Leg())

human_eye = Item(char="o", color=color.red, name="Human Eye", part=part.Human_Eye())

human_tongue = Item(char="U", color=color.red, name="Human Tongue", part=part.Human_Tongue())

human_torso = Item(char="H", color=color.red, name="Human Torso", part=part.Human_Torso())

human_arm = Item(char="\\", color=color.red, name="Human Arm", part=part.Human_Arm())

human_ear = Item(char="G", color=color.red, name="Human Ear", part=part.Human_Ear())

librarian_heart = Item(char="q", color=color.red, name="Librarian Heart", part=part.Librarian_Heart())

librarian_brain = Item(char="m", color=color.red, name="Librarian Brain", part=part.Librarian_Brain())

librarian_leg = Item(char="L", color=color.red, name="Librarian Leg", part=part.Librarian_Leg())

librarian_eye = Item(char="o", color=color.red, name="Librarian Eye", part=part.Librarian_Eye())

librarian_tongue = Item(char="U", color=color.red, name="Librarian Tongue", part=part.Librarian_Tongue())

librarian_torso = Item(char="H", color=color.red, name="Librarian Torso", part=part.Librarian_Torso())

librarian_arm = Item(char="\\", color=color.red, name="Librarian Arm", part=part.Librarian_Arm())

librarian_ear = Item(char="G", color=color.red, name="Librarian Ear", part=part.Librarian_Ear())

dwarf_heart = Item(char="q", color=color.red, name="Dwarf Heart", part=part.Dwarf_Heart())

dwarf_brain = Item(char="m", color=color.red, name="Dwarf Brain", part=part.Dwarf_Brain())

dwarf_leg = Item(char="L", color=color.red, name="Dwarf Leg", part=part.Dwarf_Leg())

dwarf_eye = Item(char="o", color=color.red, name="Dwarf Eye", part=part.Dwarf_Eye())

dwarf_tongue = Item(char="U", color=color.red, name="Dwarf Tongue", part=part.Dwarf_Tongue())

dwarf_torso = Item(char="H", color=color.red, name="Dwarf Torso", part=part.Dwarf_Torso())

dwarf_arm = Item(char="\\", color=color.red, name="Dwarf Arm", part=part.Dwarf_Arm())

dwarf_ear = Item(char="G", color=color.red, name="Dwarf Ear", part=part.Dwarf_Ear())

max_arm = Item(char="\\", color=color.red, name="Max's Arm", part=part.Max_Arm())

max_leg = Item(char="G", color=color.red, name="Max's Leg", part=part.Max_Leg())

base_loot = LootTable(inventory_chance=0.1, inventory_rolls=3,body_chance=0.8,body_rolls=1)

# H:20 M:10 P:10 D:10 SP:10 SD:10
player = Actor(
    char="@",
    color=color.white,
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=0, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    body = Body(parts=[human_leg, human_leg,human_arm, human_arm, human_eye, human_eye, human_tongue, human_torso, human_ear, human_ear, human_heart, human_brain]),
    loot_table=base_loot,
)

# H:16 M:16 P:6 D:6 SP:13 SD:13
librarian = Actor(
    char="A",
    color=color.dark_blue,
    name="Librarian",
    ai_cls=Neutral,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=0, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10),
    level=Level(xp_given=35),
    body = Body(parts=[librarian_leg, librarian_leg, librarian_arm, librarian_arm, librarian_eye, librarian_tongue, librarian_torso, librarian_ear, librarian_ear, librarian_heart, librarian_brain]),
    loot_table=base_loot,
)

# H:16 M:16 P:6 D:6 SP:13 SD:13
mad_librarian = Actor(
    char="A",
    color=color.blue,
    name="Mad Librarian",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=0, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10),
    level=Level(xp_given=35),
    body = Body(parts=[librarian_leg, librarian_leg, librarian_arm, librarian_arm, librarian_eye, librarian_tongue, librarian_torso, librarian_ear, librarian_ear, librarian_heart, librarian_brain]),
    loot_table=base_loot,
)

# H:25 M:14 P:14 D:14 SP:0 SD:3
dwarf = Actor(
    char="n",
    color=color.dark_grey,
    name="Dwarf",
    ai_cls=Neutral,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=0, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10),
    level=Level(xp_given=100),
    body = Body(parts=[dwarf_leg, dwarf_leg, dwarf_arm, dwarf_arm, dwarf_eye, dwarf_eye, dwarf_tongue, dwarf_torso, dwarf_ear, dwarf_ear,dwarf_heart, dwarf_brain]),
    loot_table=base_loot,
)

# H:25 M:14 P:14 D:14 SP:0 SD:3
mad_dwarf = Actor(
    char="n",
    color=color.light_grey,
    name="Mad Dwarf",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=0, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10),
    level=Level(xp_given=100),
    body = Body(parts=[dwarf_leg, dwarf_leg, dwarf_arm, dwarf_arm, dwarf_eye, dwarf_eye, dwarf_tongue, dwarf_torso, dwarf_ear, dwarf_ear,dwarf_heart, dwarf_brain]),
    loot_table=base_loot,
)

# H:31 M:14 P:20 D:20 SP:0 SD:3
max = Actor(
    char="n",
    color=color.orange,
    name="Max",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=-9, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10),
    level=Level(xp_given=100),
    body = Body(parts=[max_leg, max_leg, max_arm, max_arm, dwarf_eye, dwarf_eye, dwarf_tongue, dwarf_torso, dwarf_ear, dwarf_ear,dwarf_heart, dwarf_brain]),
    loot_table=base_loot,
)

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3, mental_strength=1, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    body = Body(parts=[human_heart, human_brain, human_leg, human_leg, human_eye, human_eye, human_tongue, human_torso, human_ear, human_ear, human_arm, human_arm]),
    loot_table=base_loot,
)
troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4, mental_strength=1, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    body = Body(parts=[human_heart, human_brain, human_leg, human_leg, human_eye, human_eye, human_tongue, human_torso, human_ear, human_ear, human_arm, human_arm]),
    loot_table=base_loot,
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

dagger = Item(char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger())

sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail())
