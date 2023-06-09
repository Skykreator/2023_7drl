from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional, Tuple, Union
import os

import tcod

from actions import Action, BumpAction, PickupAction, WaitAction
import actions
import color
import exceptions
from forms import Form
from part_types import PartType

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item


MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}

CONFIRM_KEYS = {
    tcod.event.K_RETURN,
    tcod.event.K_KP_ENTER,
}

ActionOrHandler = Union[Action, "BaseEventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, console: tcod.Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()


class PopupMessage(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler: BaseEventHandler, text: str):
        self.parent = parent_handler
        self.text = text

    def on_render(self, console: tcod.Console) -> None:
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(console)
        console.tiles_rgb["fg"] //= 8
        console.tiles_rgb["bg"] //= 8

        console.print(
            console.width // 2,
            console.height // 2,
            self.text,
            fg=color.white,
            bg=color.black,
            alignment=tcod.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        """Any key returns to the parent handler."""
        return self.parent


class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle events for input handlers with an engine."""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # A valid action was performed.
            if not self.engine.player.is_alive:
                # The player was killed sometime during or after the action.
                return GameOverEventHandler(self.engine)
            elif self.engine.player.level.requires_level_up:
                return LevelUpEventHandler(self.engine)
            return MainGameEventHandler(self.engine)  # Return to the main handler.
        return self

    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.handle_enemy_turns()

        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)


class AskUserEventHandler(EventHandler):
    """Handles user input for actions which require special input."""

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """By default any key exits this input handler."""
        if event.sym in {  # Ignore modifier keys.
            tcod.event.K_LSHIFT,
            tcod.event.K_RSHIFT,
            tcod.event.K_LCTRL,
            tcod.event.K_RCTRL,
            tcod.event.K_LALT,
            tcod.event.K_RALT,
            tcod.event.K_LGUI,
            tcod.event.K_RGUI,
            tcod.event.K_MODE,
        }:
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """By default any mouse click exits this input handler."""
        return self.on_exit()

    def on_exit(self) -> Optional[ActionOrHandler]:
        """Called when the user is trying to exit or cancel an action.

        By default this returns to the main event handler.
        """
        return MainGameEventHandler(self.engine)


class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "Character Information"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        widest_name = 0

        for part in self.engine.player.body.parts:
            widest_name = max(widest_name, len(part.parent.name))

        width = max(len(self.TITLE), widest_name + 6)+ 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=13 + len(self.engine.player.body.parts),
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(x=x + 1, y=y + 1, string=f"Level: {self.engine.player.level.current_level}")
        console.print(x=x + 1, y=y + 2, string=f"XP: {self.engine.player.level.current_xp}")
        console.print(
            x=x + 1,
            y=y + 3,
            string=f"XP for next Level: {self.engine.player.level.experience_to_next_level}",
        )

        console.print(x=x + 1, y=y + 4, string=f"Health: {self.engine.player.fighter.hp} / {self.engine.player.fighter.max_hp}")
        console.print(x=x + 1, y=y + 5, string=f"Mental Strength: {self.engine.player.fighter.mental_strength}")
        console.print(x=x + 1, y=y + 6, string=f"Power: {self.engine.player.fighter.power}")
        console.print(x=x + 1, y=y + 7, string=f"Defense: {self.engine.player.fighter.defense}")
        console.print(x=x + 1, y=y + 8, string=f"Spiritual Power: {self.engine.player.fighter.spiritual_power}")
        console.print(x=x + 1, y=y + 9, string=f"Spiritual Defense: {self.engine.player.fighter.spiritual_defense}")

        console.print(x=x + 1, y=y + 11, string=f"Body: ")
        for i, part in enumerate(self.engine.player.body.parts):
            console.print(x=x + 1, y=y + 12 + i, string=f"{part.parent.name}: {part.current_health} / {part.health_bonus}")


class LevelUpEventHandler(AskUserEventHandler):
    TITLE = "Level Up"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        console.draw_frame(
            x=x,
            y=0,
            width=35,
            height=8,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(x=x + 1, y=1, string="Congratulations! You level up!")
        console.print(x=x + 1, y=2, string="Select an attribute to increase.")

        console.print(
            x=x + 1,
            y=4,
            string=f"a) Constitution (+20 HP, from {self.engine.player.fighter.max_hp})",
        )
        console.print(
            x=x + 1,
            y=5,
            string=f"b) Strength (+1 attack, from {self.engine.player.fighter.power})",
        )
        console.print(
            x=x + 1,
            y=6,
            string=f"c) Agility (+1 defense, from {self.engine.player.fighter.defense})",
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <= index <= 2:
            if index == 0:
                player.level.increase_max_hp()
            elif index == 1:
                player.level.increase_power()
            else:
                player.level.increase_defense()
        else:
            self.engine.message_log.add_message("Invalid entry.", color.invalid)

            return None

        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """
        Don't allow the player to click to exit the menu, like normal.
        """
        return None


class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.

    What happens then depends on the subclass.
    """

    TITLE = "Inventory"

    selected_ind = -1

    def on_render(self, console: tcod.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console)
        number_of_items_in_inventory = len(self.engine.player.inventory.items)

        height = number_of_items_in_inventory + 2

        if height <= 3:
            height = 3

        x = 0
        y = 0

        longest_item = 0
        for item in self.engine.player.inventory.items:
            longest_item = max(longest_item, len(item.name))

        width = max(len(self.TITLE), longest_item + 8) + 4 # make dynamic

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )
        console.print(x + 1, y, f" {self.TITLE} ", fg=(0, 0, 0), bg=(255, 255, 255))

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a") + i)

                is_equipped = self.engine.player.equipment.item_is_equipped(item)

                item_string = f"({item_key}) {item.name}"

                if is_equipped:
                    item_string = f"{item_string} (E)"
                
                if item.stack:
                    item_string = f"{item_string} x{item.stack.stack}"

                console.print(x + 1, y + i + 1, item_string)
        else:
            console.print(x + 1, y + 1, "(Empty)")

        if self.selected_ind >= 0:
            item = self.engine.player.inventory.items[self.selected_ind]
            console.draw_frame(
            x=width + 2,
            y=y + self.selected_ind + 1,
            width=max(len(item.name), 11) + 4, # 11 is len("(u) unequip")
            height=5, # place holder
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
            )
            console.print(width + 3, y + self.selected_ind + 1, f" {item.name} ", fg=(0, 0, 0), bg=(255, 255, 255))

            index = self.selected_ind + 2
            if item.consumable:
                console.print(width + 4, y + index, "(c) consume")
                index += 1
            console.print(width + 4, y + index, "(d) drop")
            index += 1
            if (item.equippable and not self.engine.player.equipment.item_is_equipped(item)) or (item.part and not item.part in self.engine.player.body.parts):
                console.print(width + 4, y + index, "(e) equip")
                index += 1
            console.print(width + 4, y + index, "(l) look")
            index += 1
            if (item.equippable and self.engine.player.equipment.item_is_equipped(item)) or (item.part and item.part in self.engine.player.body.parts):
                console.print(width + 4, y + index, "(u) unequip")
                index += 1


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if self.selected_ind < 0 and 0 <= index <= 26:
            if index < len(player.inventory.items):
                self.selected_ind = index
            else:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
            return None
        else:
            item = self.engine.player.inventory.items[self.selected_ind]
            if index == 3: # d for drop
                return actions.DropItem(self.engine.player, item)
            if index == 11: # l for look
                return PopupMessage(self, item.description)
            if item.equippable:
                if self.engine.player.equipment.item_is_equipped(item):
                    if index == 20: # u for unequip
                        return actions.EquipAction(self.engine.player, item)
                else:
                    if index == 4: # e for equip
                        return actions.EquipAction(self.engine.player, item)
            if item.part:
                if item.part in self.engine.player.body.parts:
                    if index == 20: # u for unequip
                        return actions.AttachAction(self.engine.player, item.part)
                else:
                    if index == 4: # e for equip
                        return actions.AttachAction(self.engine.player, item.part)
            if item.consumable and index == 2: # c for consume
                return item.consumable.get_action(self.engine.player)
            self.selected_ind = -1
        return super().ev_keydown(event)


class BodyEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.

    What happens then depends on the subclass.
    """

    TITLE = "Body"

    selected_ind = -1

    menu_parts = []

    def on_render(self, console: tcod.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console)

        x = 0
        y = 0

        self.menu_parts = []
        longest_part = 0
        for item in self.engine.player.inventory.items:
            if item.part:
                self.menu_parts.append(item.part)
                longest_part = max(longest_part, len(item.name))

        for part in self.engine.player.body.parts:
            self.menu_parts.append(part)
            longest_part = max(longest_part, len(part.parent.name))

        height = len(self.menu_parts) + 2

        if height <= 3:
            height = 3

        width = max(len(self.TITLE), longest_part + 8) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )
        console.print(x + 1, y, f" {self.TITLE} ", fg=(0, 0, 0), bg=(255, 255, 255))

        if len(self.menu_parts) > 0:
            for i, part in enumerate(self.menu_parts):
                part_key = chr(ord("a") + i)

                part_string = f"({part_key}) {part.parent.name}"

                if part in self.engine.player.body.parts:
                    part_string = part_string + " (E)"

                console.print(x + 1, y + i + 1, part_string)
        else:
            console.print(x + 1, y + 1, "(Empty)")

        if self.selected_ind >= 0:
            part = self.menu_parts[self.selected_ind]
            console.draw_frame(
            x=width + 2,
            y=y + self.selected_ind + 1,
            width=max(len(part.parent.name), 11) + 4, # 11 is len("(u) unequip")
            height=5, # place holder
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
            )
            console.print(width + 3, y + self.selected_ind + 1, f" {part.parent.name} ", fg=(0, 0, 0), bg=(255, 255, 255))

            index = self.selected_ind + 2
            console.print(width + 4, y + index, "(d) drop")
            index += 1
            if not part in self.engine.player.body.parts:
                console.print(width + 4, y + index, "(e) equip")
                index += 1
            console.print(width + 4, y + index, "(l) look")
            index += 1
            if  part in self.engine.player.body.parts:
                console.print(width + 4, y + index, "(u) unequip")
                index += 1


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        index = key - tcod.event.K_a

        if self.selected_ind < 0 and 0 <= index <= 26:
            if index < len(self.menu_parts):
                self.selected_ind = index
            else:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
            return None 
        else:
            part = self.menu_parts[self.selected_ind]
            if index == 3: # d for drop
                return actions.DropItem(self.engine.player, part)
            if index == 11: # l for look
                return PopupMessage(self, part.parent.description)
            if part in self.engine.player.body.parts:
                if index == 20: # u for unequip
                    return actions.AttachAction(self.engine.player, part)
            else:
                if index == 4: # e for equip
                    return actions.AttachAction(self.engine.player, part)
            self.selected_ind = -1
        return super().ev_keydown(event)
    

class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""

    def __init__(self, engine: Engine):
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = player.x, player.y

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)
        x, y = self.engine.mouse_location
        console.tiles_rgb["bg"][x, y] = color.white
        console.tiles_rgb["fg"][x, y] = color.black

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """Check for key movement or confirmation keys."""
        key = event.sym
        if key in MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                modifier *= 5
            if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
                modifier *= 10
            if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
                modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = x, y
            return None
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """Left click confirms a selection."""
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        """Called when an index is selected."""
        raise NotImplementedError()


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
        """Return to main handler."""
        for item in self.engine.game_map.items:
            if x == item.x and y == item.y:
                return PopupMessage(self, item.description)
        if self.engine.game_map.get_actor_at_location(x,y):
            return PopupMessage(self, self.engine.game_map.get_actor_at_location(x,y).description)
        return MainGameEventHandler(self.engine)


class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]):
        super().__init__(engine)

        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Tuple[int, int]], Optional[Action]],
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a rectangle around the targeted area, so the player can see the affected tiles.
        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius ** 2,
            height=self.radius ** 2,
            fg=color.red,
            clear=False,
        )

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))

class RitualHandler(AskUserEventHandler):
    
    TITLE = "Select Limb to Sacrifice"

    flesh_parts = []
    offering_inds = []

    selected_ind = -1
    can_ritual = False

    part_to_qual = {PartType.ARM : 20,
                    PartType.BRAIN : 40,
                    PartType.EAR : 15,
                    PartType.EYE : 15,
                    PartType.HEART : 50,
                    PartType.LEG : 20,
                    PartType.TONGUE : 15,
                    PartType.TORSO : 30,}

    def on_render(self, console: tcod.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console)

        x = 0
        y = 0

        ritual_equip = False
        ritual_offering = False
        ritual_limb = False

        offering_quality = 0
        self.flesh_parts = []
        self.offering_inds = []
        for i, item in enumerate(self.engine.player.inventory.items):
            if item.equippable and item.equippable.sacrificial:
                ritual_equip = True
            if item.stack and item.stack.quality > 0:
                self.offering_inds.append(i)
                offering_quality += item.stack.stack * item.stack.quality
        longest_part = 0

        for part in self.engine.player.body.parts:
            longest_part = max(longest_part, len(part.parent.name))
            if part.form == Form.FLESH:
                ritual_limb = True
                if offering_quality >= self.part_to_qual[part.part_type]:
                    ritual_offering = True
                    self.flesh_parts.append(part)

        self.can_ritual = True
        if not (ritual_equip and ritual_limb and ritual_offering):
            message = "Missing: "
            if not ritual_equip:
                message = message + "an implement "
            if not ritual_limb:
                message = message + "living flesh "
            if not ritual_offering:
                message = message + "an offering "
            console.draw_frame(
                x=x,
                y=y,
                width=len(message) + 4,
                height=3,
                clear=True,
                fg=(255, 255, 255),
                bg=(0, 0, 0),
            )
            console.print(x + 1, y + 1, f" {message} ")
            self.can_ritual = False
            return

        height = len(self.flesh_parts) + 2

        if height <= 3:
            height = 3

        width = max(len(self.TITLE), longest_part + 8) + 4
        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )
        console.print(x + 1, y, f" {self.TITLE} ")
        for i, part in enumerate(self.flesh_parts):
                part_key = chr(ord("a") + i)

                part_string = f"({part_key}) {part.parent.name}"

                console.print(x + 1, y + i + 1, part_string)

        if self.selected_ind >= 0:
            part = self.flesh_parts[self.selected_ind]
            console.draw_frame(
            x=width + 2,
            y=y + self.selected_ind + 1,
            width=max(len(part.parent.name), 11) + 4, # 11 is len("(c) confirm")
            height=3, 
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
            )
            console.print(width + 3, y + self.selected_ind + 1, f" {part.parent.name} ", fg=(0, 0, 0), bg=(255, 255, 255))

            index = self.selected_ind + 2
            console.print(width + 4, y + index, "(c) confirm")


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        index = key - tcod.event.K_a
        if not self.can_ritual:
            return MainGameEventHandler(self.engine)

        if self.selected_ind < 0 and 0 <= index <= 26:
            if index < len(self.flesh_parts):
                self.selected_ind = index
            else:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
            return None 
        else:
            part = self.flesh_parts[self.selected_ind]
            self.selected_ind = -1
            if index == 2: # c for confirm
                actions.SacrificePart(self.engine.player, part, self.offering_inds).perform()
                return MainGameEventHandler(self.engine)
        return super().ev_keydown(event)

class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        action: Optional[Action] = None

        key = event.sym
        modifier = event.mod

        player = self.engine.player

        if key == tcod.event.K_PERIOD and modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            return actions.TakeStairsAction(player)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.K_ESCAPE:
            raise SystemExit()
        elif key == tcod.event.K_v:
            return HistoryViewer(self.engine)

        elif key == tcod.event.K_g:
            action = PickupAction(player)

        elif key == tcod.event.K_i:
            return InventoryEventHandler(self.engine)
        elif key == tcod.event.K_p:
            return BodyEventHandler(self.engine)
        elif key == tcod.event.K_c:
            return CharacterScreenEventHandler(self.engine)
        elif key == tcod.event.K_SLASH:
            return LookHandler(self.engine)
        elif key == tcod.event.K_r:
            return RitualHandler(self.engine)

        # No valid key was pressed
        return action


class GameOverEventHandler(EventHandler):
    def on_quit(self) -> None:
        """Handle exiting out of a finished game."""
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")  # Deletes the active save file.
        raise exceptions.QuitWithoutSaving()  # Avoid saving a finished game.

    def ev_quit(self, event: tcod.event.Quit) -> None:
        self.on_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_ESCAPE:
            self.on_quit()


CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}


class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(0, 0, log_console.width, 1, "┤Message history├", alignment=tcod.CENTER)

        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]:
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym == tcod.event.K_HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.K_END:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:  # Any other key moves back to the main game state.
            return MainGameEventHandler(self.engine)
        return None
