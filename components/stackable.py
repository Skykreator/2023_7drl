from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
import components.ai
import components.inventory

if TYPE_CHECKING:
    from entity import Actor, Item


class Stackable(BaseComponent):
    parent: Item

    def __init__(
        self,
        stack: int = 0,
        quality: int = 0,
    ):
        self.stack = stack
        self.quality = quality
