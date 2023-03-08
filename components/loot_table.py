from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class LootTable(BaseComponent):
    parent: Actor

    def __init__(
            self,
            inventory_chance: float = 0,
            inventory_rolls: int = 0,
            body_chance: float = 0,
            body_rolls: int = 0,
    ):
        self.inventory_chance = inventory_chance
        self.inventory_rolls = inventory_rolls
        self.body_chance = body_chance
        self.body_rolls = body_rolls
