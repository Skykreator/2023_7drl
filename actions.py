from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, List

import color
import exceptions
from part_types import PartType
import copy

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item, Part


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if item.stack:
                    for inv_item in inventory.items:
                        if inv_item.stack and inv_item.name == item.name:
                            inv_item.stack.stack += item.stack.stack
                            return
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    def __init__(self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)

class AttachAction(Action):
    def __init__(self, entity: Actor, part: Part):
        super().__init__(entity)

        self.part = part

    def perform(self) -> None:
        self.entity.body.toggle_equip(self.part)


class WaitAction(Action):
    def perform(self) -> None:
        pass


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message("You descend the staircase.", color.descend)
        else:
            raise exceptions.Impossible("There are no stairs here.")


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = int((self.entity.fighter.power - target.fighter.defense) * 0.2)

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage}.", attack_color)
            target.fighter.hp -= damage
            import components.ai
            if isinstance(target.ai, components.ai.Neutral):
                target.ai = components.ai.FleeingNeutral(target, self.entity, target.ai, 10)
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

class SacrificePart(Action):
    def __init__(self, entity: Actor, part: Part, offering_inds: List[int]):
        super().__init__(entity)
        self.part = part
        self.offerings: List[Item] = []
        for ind in offering_inds:
            self.offerings.append(self.entity.inventory.items[ind])
    
    def perform(self) -> None:
        radius = 3 + self.part.current_health
        max_quality = 50 # const
        sum_quality = 0
        for offering in self.offerings:
            if sum_quality < max_quality:
                ideal_amount = int((max_quality-sum_quality) / offering.stack.quality)
                actual = min(ideal_amount, offering.stack.stack)
                sum_quality += actual * offering.stack.quality
                offering.stack.stack -= actual
                if offering.stack.stack == 0:
                    self.entity.inventory.items.remove(offering)
        import entity_factories
        if self.part.part_type == PartType.ARM:
            self.entity.body.parts.append(copy.deepcopy(entity_factories.phantom_arm).part)
        elif self.part.part_type == PartType.BRAIN:
            self.entity.body.parts.append(copy.deepcopy(entity_factories.phantom_brain).part)
        elif self.part.part_type == PartType.EAR:
            self.entity.body.parts.append(copy.deepcopy(entity_factories.phantom_ear).part)
        elif self.part.part_type == PartType.EYE:
            self.entity.body.parts.append(copy.deepcopy(entity_factories.phantom_eye).part)
        elif self.part.part_type == PartType.HEART:
            self.entity.body.parts.append(copy.deepcopy(entity_factories.phantom_heart).part)
        elif self.part.part_type == PartType.LEG:
            self.entity.body.parts.append(copy.deepcopy(entity_factories.phantom_leg).part)
        elif self.part.part_type == PartType.TONGUE:
            self.entity.body.parts.append(copy.deepcopy(entity_factories.phantom_tongue).part)
        elif self.part.part_type == PartType.TORSO:
            self.entity.body.parts.append(copy.deepcopy(entity_factories.phantom_torso).part)
        self.entity.body.parts.remove(self.part)

        damage = 10 + sum_quality
        self.engine.message_log.add_message(f"The flesh explodes in a burst of energy", color.spiritual)
        damaged_actors: List[Actor] = []
        for actor in self.engine.game_map.actors:
            if actor.distance(self.entity.x, self.entity.y) <= radius and not actor == self.entity:
                damaged_actors.append(actor)
        for actor in damaged_actors:
            self.engine.message_log.add_message(
                f"The {actor.name} is engulfed the explosion, taking {damage} damage!"
            )
            actor.fighter.take_damage(damage)

