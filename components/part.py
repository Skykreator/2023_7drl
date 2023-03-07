from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from part_types import PartType
from forms import Form
from ability import Ability

if TYPE_CHECKING:
    from entity import Item


class Part(BaseComponent):
    parent: Item

    def __init__(
        self,
        part_type: PartType,
        form: Form,
        #ability: Ability,
        health_bonus: int = 0,
        mental_bonus: int = 0,
        spiritual_defense_bonus: int = 0,
        spiritual_power_bonus: int = 0,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        
    ):
        self.part_type = PartType
        self.form = Form
        #self.ability = Ability
        self.health_bonus = health_bonus
        self.current_health = health_bonus
        self.mental_bonus = mental_bonus
        self.spiritual_defense_bonus = spiritual_defense_bonus
        self.spiritual_power_bonus = spiritual_power_bonus
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus

# would be pretty cool if there were two seperate hemispheres...
class Human_Brain(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.BRAIN, form=Form.FLESH, health_bonus = 1, mental_bonus=10, spiritual_power_bonus=4, spiritual_defense_bonus=5)


class Human_Arm(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.ARM, form=Form.FLESH, health_bonus = 2, power_bonus=2, defense_bonus=1)


class Human_Leg(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.LEG, form=Form.FLESH, health_bonus = 3, power_bonus=2, defense_bonus=2)


class Human_Eye(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.EYE, form=Form.FLESH, spiritual_defense_bonus=1, spiritual_power_bonus=1)


class Human_Ear(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.EAR, form=Form.FLESH, spiritual_defense_bonus=1, spiritual_power_bonus=1)


class Human_Tongue(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.TONGUE, form=Form.FLESH, spiritual_power_bonus=1)


class Human_Heart(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.HEART, form=Form.FLESH, health_bonus = 3, power_bonus=2, spiritual_defense_bonus=1, spiritual_power_bonus=1)


class Human_Torso(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.TORSO, form=Form.FLESH, health_bonus = 6, defense_bonus=4)

###############################################

class Librarian_Brain(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.BRAIN, form=Form.FLESH, health_bonus = 1, mental_bonus=10, spiritual_power_bonus=6, spiritual_defense_bonus=5)


class Librarian_Arm(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.ARM, form=Form.FLESH, health_bonus = 2, power_bonus=1, defense_bonus=1)


class Librarian_Leg(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.LEG, form=Form.FLESH, health_bonus = 2, power_bonus=1, defense_bonus=1)


class Librarian_Eye(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.EYE, form=Form.FLESH, mental_bonus = 3, spiritual_defense_bonus=2, spiritual_power_bonus=2)


class Librarian_Ear(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.EAR, form=Form.FLESH, spiritual_defense_bonus=1, spiritual_power_bonus=1)


class Librarian_Tongue(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.TONGUE, form=Form.FLESH, spiritual_defense_bonus=2, spiritual_power_bonus=2)


class Librarian_Heart(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.HEART, form=Form.FLESH, health_bonus = 2, mental_bonus = 3, power_bonus=2, spiritual_defense_bonus=1, spiritual_power_bonus=6)


class Librarian_Torso(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.TORSO, form=Form.FLESH, health_bonus = 5, defense_bonus=2)

#######################

class Dwarf_Brain(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.BRAIN, form=Form.FLESH, health_bonus = 1, mental_bonus=10, spiritual_defense_bonus=2)


class Dwarf_Arm(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.ARM, form=Form.FLESH, health_bonus = 3, power_bonus=1, defense_bonus=1)


class Dwarf_Leg(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.LEG, form=Form.FLESH, health_bonus = 4, power_bonus=1, defense_bonus=1)


class Dwarf_Eye(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.EYE, form=Form.FLESH)


class Dwarf_Ear(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.EAR, form=Form.FLESH)


class Dwarf_Tongue(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.TONGUE, form=Form.FLESH)


class Dwarf_Heart(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.HEART, form=Form.FLESH, health_bonus = 5, mental_bonus = 4, power_bonus=2, spiritual_defense_bonus=1)


class Dwarf_Torso(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.TORSO, form=Form.FLESH, health_bonus = 5, defense_bonus=2)

class Max_Arm(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.ARM, form=Form.FLESH, health_bonus = 4, power_bonus=2, defense_bonus=2)


class Max_Leg(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.LEG, form=Form.FLESH, health_bonus = 5, power_bonus=2, defense_bonus=2)

#######################

class Phantom_Heart(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.HEART, form=Form.SPIRIT, defense_bonus=999, power_bonus=2, spiritual_defense_bonus=1, spiritual_power_bonus=1)

class Phantom_Brain(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.BRAIN, form=Form.SPIRIT, mental_bonus=15, spiritual_power_bonus=8, spiritual_defense_bonus=8)


class Phantom_Arm(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.ARM, form=Form.SPIRIT, mental_bonus=2, spiritual_power_bonus=2, spiritual_defense_bonus=1)


class Phantom_Leg(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.LEG, form=Form.SPIRIT, mental_bonus=3, spiritual_power_bonus=2, spiritual_defense_bonus=2)


class Phantom_Eye(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.EYE, form=Form.SPIRIT, spiritual_defense_bonus=3, spiritual_power_bonus=3)


class Phantom_Ear(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.EAR, form=Form.SPIRIT, spiritual_defense_bonus=2, spiritual_power_bonus=2)


class Phantom_Tongue(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.TONGUE, form=Form.SPIRIT, spiritual_defense_bonus=2, spiritual_power_bonus=2)


class Phantom_Torso(Part):
    def __init__(self) -> None:
        super().__init__(part_type=PartType.TORSO, form=Form.SPIRIT, mental_bonus= 8, spiritual_defense_bonus=6)