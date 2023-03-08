from __future__ import annotations

from typing import TYPE_CHECKING, List

from components.base_component import BaseComponent
from components.part import Part
import copy

if TYPE_CHECKING:
    from entity import Actor,Item

# collection of parts, has no attributes besides its parts
class Body(BaseComponent):
    parent: Actor

    def __init__(self, parts: List[Item] = None, max_parts: int = 12):
        self.parts: List[Part] = []
        for part in parts:
            self.parts.append(copy.deepcopy(part.part))
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

        if self.parent.inventory:
            if part.parent in self.parent.inventory.items:
                self.parent.inventory.items.remove(part.parent)

        if add_message:
            self.equip_message(part.parent.name)

    def unequip(self, part: Part, add_message: bool) -> None:
        self.parts.remove(part)
        if add_message:
            self.unequip_message(part.parent.name)

    def toggle_equip(self, part: Part, add_message: bool = True) -> None:
        if part in self.parts:
            self.unequip(part, add_message)
        else:
            self.equip(part, add_message)
    
    def set_health(self, value: int) -> None:
        change = value - self.health_bonus
        for part in self.parts:
            #positive try to get to max, negative try to get to 0
            if change == 0:
                return
            part_change = 0
            if change < 0:
                part_change = max(-part.current_health, change)
            else:
                part_change = min(part.health_bonus - part.current_health, change) 
            part.current_health += part_change
            change -= part_change
            if (part.health_bonus > 0):
                self.engine.message_log.add_message(f"{part.parent.name} max: {part.health_bonus}, current: {part.current_health}.")
    
    def drop(self, part: Part) -> None:
        self.parts.remove(part)
        part.parent.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"{self.parent.name} dropped a {part.parent.name}.")
