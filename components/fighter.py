from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from render_order import RenderOrder
import random
import color

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, mental_strength: int, spiritual_defense: int, spiritual_power: int, base_defense: int, base_power: int):
        self._hp = hp
        self._max_hp = hp
        self._mental_strength = mental_strength
        self.base_spiritual_defense = spiritual_defense
        self.base_spiritual_power = spiritual_power
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def hp(self) -> int:
        return self._hp + self.health_bonus
    
    @property
    def max_hp(self) -> int:
        return self._max_hp + self.max_health_bonus
    
    @max_hp.setter
    def max_hp(self, value: int) -> None:
        self._max_hp = value

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = min(self._max_hp, max(0, value))
        body_health = value - self._hp
        self.parent.body.set_health(body_health)
        if self.hp == 0 and self.parent.ai:
            self.die()

    @property
    def mental_strength(self) -> int:
        return self._mental_strength + self.mental_bonus

    @mental_strength.setter
    def mental_strength(self, value: int) -> None:
        self._mental_strength = max(0, value)
        if self._mental_strength == 0 and self.parent.ai:
            self.die()

    @property
    def spiritual_defense(self) -> int:
        return self.base_spiritual_defense + self.spiritual_defense_bonus
    
    @property
    def spiritual_power(self) -> int:
        return self.base_spiritual_power + self.spiritual_power_bonus

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def health_bonus(self) -> int:
        bonus = 0
        if self.parent.body:
            bonus += self.parent.body.health_bonus
        return bonus
    
    @property
    def max_health_bonus(self) -> int:
        bonus = 0
        if self.parent.body:
            bonus += self.parent.body.max_health_bonus
        return bonus

    @property
    def mental_bonus(self) -> int:
        bonus = 0
        if self.parent.body:
            bonus += self.parent.body.mental_strength_bonus
        return bonus

    @property
    def spiritual_defense_bonus(self) -> int:
        bonus = 0
        if self.parent.equipment:
            bonus += self.parent.equipment.spiritual_defense_bonus
        if self.parent.body:
            bonus += self.parent.body.spiritual_defense_bonus
        return bonus
    
    @property
    def spiritual_power_bonus(self) -> int:
        bonus = 0
        if self.parent.equipment:
            bonus += self.parent.equipment.spiritual_power_bonus
        if self.parent.body:
            bonus += self.parent.body.spiritual_power_bonus
        return bonus

    @property
    def defense_bonus(self) -> int:
        bonus = 0
        if self.parent.equipment:
            bonus += self.parent.equipment.defense_bonus
        if self.parent.body:
            bonus += self.parent.body.defense_bonus
        return bonus

    @property
    def power_bonus(self) -> int:
        bonus = 0
        if self.parent.equipment:
            bonus += self.parent.equipment.power_bonus
        if self.parent.body:
            bonus += self.parent.body.power_bonus
        return bonus

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        if self.parent.loot_table:
            if self.parent.inventory:
                for _ in range(self.parent.loot_table.inventory_rolls):
                    if len(self.parent.inventory.items) > 0:
                        if random.random() < self.parent.loot_table.inventory_chance:
                            self.parent.inventory.drop(self.parent.inventory.items[random.randint(0, len(self.parent.inventory.items))])
            if self.parent.body:
                for _ in range(self.parent.loot_table.body_rolls):
                    if len(self.parent.body.parts) > 0:
                        if random.random() < self.parent.loot_table.body_chance:
                            self.parent.body.drop(self.parent.body.parts[random.randint(0, len(self.parent.body.parts))])
                        

        self.engine.message_log.add_message(death_message, death_message_color)

        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def mental_strength_change(self, amount: float) -> int:

        amount_changed = (int) (self.mental_strength * amount)

        self.hp = self.hp + amount_changed

        return amount_changed
