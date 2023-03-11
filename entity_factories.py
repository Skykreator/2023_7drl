from components import consumable, equippable, part
from components.ai import HostileEnemy, Neutral
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.body import Body
from components.loot_table import LootTable
from components.stackable import Stackable
import color
from entity import Actor, Item

human_heart = Item(char="q", color=color.red, name="Human Heart", part=part.Human_Heart(), description=
    """
    It beats.
    """,)

human_brain = Item(char="m", color=color.red, name="Human Brain", part=part.Human_Brain(), description=
    """
    No heavier than a couple books.
    """,)

human_leg = Item(char="L", color=color.red, name="Human Leg", part=part.Human_Leg(), description=
    """
    Thick, tapering down then flaring out again.
    """,)

human_eye = Item(char="o", color=color.red, name="Human Eye", part=part.Human_Eye(), description=
    """
    It stares.
    """,)

human_tongue = Item(char="U", color=color.red, name="Human Tongue", part=part.Human_Tongue(), description=
    """
    Dexterous.
    """,)

human_torso = Item(char="H", color=color.red, name="Human Torso", part=part.Human_Torso(), description=
    """
    Broad and strong, it was not designed for a library.
    """,)

human_arm = Item(char="\\", color=color.red, name="Human Arm", part=part.Human_Arm(), description=
    """
    It twitches.
    """,)

human_ear = Item(char="G", color=color.red, name="Human Ear", part=part.Human_Ear(), description=
    """
    It listens.
    """,)

librarian_heart = Item(char="q", color=color.red, name="Librarian Heart", part=part.Librarian_Heart(), description=
    """
    It ripples.
    """,)

librarian_brain = Item(char="m", color=color.red, name="Librarian Brain", part=part.Librarian_Brain(), description=
    """
    No heavier than a couple books.
    """)

librarian_leg = Item(char="L", color=color.red, name="Librarian Leg", part=part.Librarian_Leg(), description=
    """
    Short and awkward, an afterthought.
    """,)

librarian_eye = Item(char="o", color=color.red, name="Librarian Eye", part=part.Librarian_Eye(), description=
    """
    The fist-sized eye stares.
    """,)

librarian_tongue = Item(char="U", color=color.red, name="Librarian Tongue", part=part.Librarian_Tongue(), description=
    """
    Long and flexible, it can pronounce every word in every book.
    """,)

librarian_torso = Item(char="H", color=color.red, name="Librarian Torso", part=part.Librarian_Torso(), description=
    """
    Shaped to the furniture.
    """,)

librarian_arm = Item(char="\\", color=color.red, name="Librarian Arm", part=part.Librarian_Arm(), description=
    """
    Strong enough.
    """,)

librarian_ear = Item(char="G", color=color.red, name="Librarian Ear", part=part.Librarian_Ear(), description=
    """
    It listens.
    """,)

dwarf_heart = Item(char="q", color=color.red, name="Dwarf Heart", part=part.Dwarf_Heart(), description=
    """
    It throbs.
    """)

dwarf_brain = Item(char="m", color=color.red, name="Dwarf Brain", part=part.Dwarf_Brain(), description=
    """
    No heavier than a couple books.
    """)

dwarf_leg = Item(char="L", color=color.red, name="Dwarf Leg", part=part.Dwarf_Leg(), description=
    """
    Stout and powerful.
    """,)

dwarf_eye = Item(char="o", color=color.red, name="Dwarf Eye", part=part.Dwarf_Eye(), description=
    """
    It stays focused, even in the dark.
    """,)

dwarf_tongue = Item(char="U", color=color.red, name="Dwarf Tongue", part=part.Dwarf_Tongue(), description=
    """
    Bulky, warping speech.
    """,)

dwarf_torso = Item(char="H", color=color.red, name="Dwarf Torso", part=part.Dwarf_Torso(), description=
    """
    Overfortified for its size.
    """,)

dwarf_arm = Item(char="\\", color=color.red, name="Dwarf Arm", part=part.Dwarf_Arm(),  description=
    """
    It could bear the weight of a man.
    """,)

dwarf_ear = Item(char="G", color=color.red, name="Dwarf Ear", part=part.Dwarf_Ear(),  description=
    """
    Knobbly.
    """,)

max_arm = Item(char="\\", color=color.red, name="Max's Arm", part=part.Max_Arm(), description=
    """
    Strong with a strong orange hue and a strong orange scent.
    """,)

max_leg = Item(char="G", color=color.red, name="Max's Leg", part=part.Max_Leg(), description=
    """
    Strong with a strong orange hue and a strong orange scent.
    """,)

phantom_heart = Item(char="q", color=color.red, name="Phantom Heart", part=part.Phantom_Heart(), description=
    """
    It pulses.
    """,)

phantom_brain = Item(char="m", color=color.red, name="Phantom Brain", part=part.Phantom_Brain(), description=
    """
    Almost transparent.
    """,)

phantom_leg = Item(char="L", color=color.red, name="Phantom Leg", part=part.Phantom_Leg(), description=
    """
    Visible out of the corner of your eye.
    """,)

phantom_eye = Item(char="o", color=color.red, name="Phantom Eye", part=part.Phantom_Eye(), description=
    """
    It stares at something deeper inside.
    """,)

phantom_tongue = Item(char="U", color=color.red, name="Phantom Tongue", part=part.Phantom_Tongue(), description=
    """
    Fluent in forgotten tongues.
    """,)

phantom_torso = Item(char="H", color=color.red, name="Phantom Torso", part=part.Phantom_Torso(), description=
    """
    Sturdy, yet ephemeral.
    """,)

phantom_arm = Item(char="\\", color=color.red, name="Phantom Arm", part=part.Phantom_Arm(), description=
    """
    It decieves the conscious mind.
    """,)

phantom_ear = Item(char="G", color=color.red, name="Phantom Ear", part=part.Phantom_Ear(), description=
    """
    Not limited to physical vibrations.
    """,)

base_loot = LootTable(inventory_chance=0.1, inventory_rolls=3,body_chance=0.8,body_rolls=1)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Tome of Confusion",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
    description=
    """
    The pages of gibberish are decipherable only by the unconscious mind.
    """,
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Tome of Fire",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
    description=
    """
    The librarians were the first to wield fire as tool and weapon.
    """,
)
health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
    description=
    """
    The opaque fluid churns within the vial
    """,
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Tome of Lightning",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    description=
    """
    bababadalgharaghtakamminarronnkonnbronntonnerronntuonnthunntrovarrhounawnskawntoohoohoordenenthurnuk!
    """,
)

dagger = Item(char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger(), description=
    """
    The blade is better suited to combat than ritual.
    """,)

sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword(), description=
    """
    The blade is forged from the ores in the foundations of the library.
    """,)

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Hide",
    equippable=equippable.LeatherArmor(),
    description=
    """
    The hide of an unknown creature.
    """,
)

chain_mail = Item(char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail(), description=
    """
    Time has dulled its links, but none are broken.
    """,)

sacrificial_dagger = Item(char="/", color=color.spiritual, name="Sacrificial Dagger", equippable=equippable.SacrificialDagger(), description=
    """
    The bare obsidian is without blemish.
    """,)

ornate_shell = Item(char="c", color=color.spiritual, name="Ornate Shell", stack=Stackable(5,5), description=
    """
    Too small and too big.
    """,)

glass_shard = Item(char="w", color=color.spiritual, name="Glass Shard", stack=Stackable(5,3), description=
    """
    Its reflections don't match your surroundings.
    """,)

torn_scrap = Item(char="=", color=color.spiritual, name="Torn Scrap", stack=Stackable(5,1), description=
    """
    Covered in smudged glyphs, undecipherable.
    """,)

orange = Item(char="o", color=color.orange, name="Orange",stack=Stackable(1,8), description=
    """
    ... delicious
    so sweet
    and so cold
    """,
    consumable=consumable.HealingConsumable(3)
    )

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
    description=
    """
    JTP
    """,
)

# H:16 M:16 P:6 D:6 SP:13 SD:13
librarian = Actor(
    char="A",
    color=color.blue,
    name="Librarian",
    ai_cls=Neutral,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=0, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10, items=[torn_scrap]),
    level=Level(xp_given=35),
    body = Body(parts=[librarian_leg, librarian_leg, librarian_arm, librarian_arm, librarian_eye, librarian_tongue, librarian_torso, librarian_ear, librarian_ear, librarian_heart, librarian_brain]),
    loot_table=base_loot,
    description=
    """
    The librarian's cyclopean eye stares back at you.
    """,    
)

# H:16 M:16 P:6 D:6 SP:13 SD:13
mad_librarian = Actor(
    char="A",
    color=color.light_blue,
    name="Mad Librarian",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=0, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10, items=[torn_scrap]),
    level=Level(xp_given=35),
    body = Body(parts=[librarian_leg, librarian_leg, librarian_arm, librarian_arm, librarian_eye, librarian_tongue, librarian_torso, librarian_ear, librarian_ear, librarian_heart, librarian_brain]),
    loot_table=base_loot,
    description=
    """
    The librarian grips the shredded remains of some ancient tome.
    """,
)

# H:25 M:14 P:14 D:14 SP:0 SD:3
dwarf = Actor(
    char="n",
    color=color.dark_green,
    name="Dwarf",
    ai_cls=Neutral,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=0, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10, items=[glass_shard]),
    level=Level(xp_given=100),
    body = Body(parts=[dwarf_leg, dwarf_leg, dwarf_arm, dwarf_arm, dwarf_eye, dwarf_eye, dwarf_tongue, dwarf_torso, dwarf_ear, dwarf_ear,dwarf_heart, dwarf_brain]),
    loot_table=base_loot,
    description=
    """
    The dwarf rushes along, paying you no heed.
    """,
)

# H:25 M:14 P:14 D:14 SP:0 SD:3
mad_dwarf = Actor(
    char="n",
    color=color.green,
    name="Mad Dwarf",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=0, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10, items=[glass_shard]),
    level=Level(xp_given=100),
    body = Body(parts=[dwarf_leg, dwarf_leg, dwarf_arm, dwarf_arm, dwarf_eye, dwarf_eye, dwarf_tongue, dwarf_torso, dwarf_ear, dwarf_ear,dwarf_heart, dwarf_brain]),
    loot_table=base_loot,
    description=
    """
    The dwarf's eyes dart around manically, then focus on you.
    """,
)

# H:31 M:14 P:20 D:20 SP:0 SD:3
max = Actor(
    char="n",
    color=color.orange,
    name="Max",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=0, base_defense=0, base_power=0, mental_strength=-9, spiritual_defense=0, spiritual_power=0),
    inventory=Inventory(capacity=10, items=[glass_shard,orange]),
    level=Level(xp_given=100),
    body = Body(parts=[max_leg, max_leg, max_arm, max_arm, dwarf_eye, dwarf_eye, dwarf_tongue, dwarf_torso, dwarf_ear, dwarf_ear,dwarf_heart, dwarf_brain]),
    loot_table=base_loot,
    description=
    """
    This dwarf has a bandolier of oranges across their chest. 
    His limbs have grown strong from the oranges.
    """,
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
    description=
    """
    It looks like something out of one of the infinite tomes that cover each wall.
    """,
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
    description=
    """
    It looks like something out of one of the infinite tomes that cover each wall.
    """,
)