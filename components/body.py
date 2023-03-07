from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from components.base_component import BaseComponent
from components.part import Part
from components.fighter import Fighter
from part_types import PartType

if TYPE_CHECKING:
    from entity import Actor,Item

# collection of parts, has no attributes besides its parts
class Body(BaseComponent):
    parent: Actor

    def __init__(self, parts: List[Item] = None, max_parts: int = 12):
        self.parts = []
        for part in parts:
            self.parts.append(part.part)
        self.max_parts = max_parts


    @property
    def defense_bonus(self) -> int:
        bonus = 0
        for part in self.parts:
            bonus += part.defense_bonus

        return bonus

    @property
    def power_bonus(self) -> int:
        bonus = 0
        for part in self.parts:
            bonus += part.power_bonus

        return bonus
    
    @property
    def health_bonus(self) -> int:
        bonus = 0
        for part in self.parts:
            bonus += part.current_health

        return bonus
    
    @property
    def max_health_bonus(self) -> int:
        bonus = 0
        for part in self.parts:
            bonus += part.health_bonus

        return bonus

    @property
    def mental_strength_bonus(self) -> int:
        bonus = 0
        for part in self.parts:
            bonus += part.mental_bonus

        return bonus

    @property
    def spiritual_defense_bonus(self) -> int:
        bonus = 0
        for part in self.parts:
            bonus += part.spiritual_defense_bonus

        return bonus
    
    @property
    def spiritual_power_bonus(self) -> int:
        bonus = 0
        for part in self.parts:
            bonus += part.spiritual_power_bonus

        return bonus

    def part_equipped(self, part: Part) -> bool:
        return part in self.parts

    def unequip_message(self, part_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(f"You remove the {part_name}.")

    def equip_message(self, part_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(f"You equip the {part_name}.")

    def full_message(self) -> None:
        self.parent.gamemap.engine.message_log.add_message(f"You cannot fit more to your body.")


    def equip(self, part: Part, add_message: bool) -> None:
        if len(self.parts) >= self.max_parts:
            self.full_message
            return
            
        self.parts.append(part)
        self.parent.fighter.max_hp += part.health_bonus
        self.parent.fighter.hp += part.current_health

        if add_message:
            self.equip_message(part.parent.name)

    def unequip(self, part: Part, add_message: bool) -> None:
        self.parts.remove(part)
        self.parent.fighter.max_hp -= part.health_bonus
        part.current_health = self.parent.fighter.hp - self.parent.fighter.max_hp
        self.parent.fighter.hp(self.parent.fighter.hp)
        if add_message:
            self.unequip_message(part.parent.name)

    def toggle_equip(self, part: Part, add_message: bool = True) -> None:
        if part in self.parts:
            self.unequip(part, add_message)
        else:
            self.equip(part, add_message)
