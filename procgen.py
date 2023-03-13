from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterator, List, Tuple
import random

import tcod
import copy
import numpy as np

from game_map import GameMap
import entity_factories
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


max_items_by_floor = [
    (1, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.health_potion, 35)],
    2: [(entity_factories.confusion_scroll, 10)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.sword, 5)],
    6: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.orc, 50)],
    0: [(entity_factories.dwarf, 15)],
    0: [(entity_factories.librarian, 80)],
    2: [(entity_factories.mad_librarian, 40)],
    2: [(entity_factories.librarian, 40)],
    3: [(entity_factories.dwarf, 0)],
    1: [(entity_factories.mad_dwarf, 15)],
    1: [(entity_factories.max, 3)],
    3: [(entity_factories.troll, 15)],
    5: [(entity_factories.troll, 30)],
    7: [(entity_factories.troll, 60)],
}


def get_max_value_for_floor(max_value_by_floor: List[Tuple[int, int]], floor: int) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value


def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(entities, weights=entity_weighted_chance_values, k=number_of_entities)

    return chosen_entities


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1


def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int) -> None:
    number_of_monsters = random.randint(0, get_max_value_for_floor(max_monsters_by_floor, floor_number))
    number_of_items = random.randint(0, get_max_value_for_floor(max_items_by_floor, floor_number))

    monsters: List[Entity] = get_entities_at_random(enemy_chances, number_of_monsters, floor_number)
    items: List[Entity] = get_entities_at_random(item_chances, number_of_items, floor_number)

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_box_dungeon(max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    for _ in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, engine.game_world.current_floor)

        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon


def generate_bsp_dungeon(
    room_min_size: int,
    room_max_ratio: float,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    bsp = tcod.bsp.BSP(0,0, width=map_width-1, height=map_height-1)
    bsp.split_recursive(depth=6, min_width=room_min_size, min_height=room_min_size, max_horizontal_ratio=room_max_ratio, max_vertical_ratio=room_max_ratio)

    rooms: List[RectangularRoom] = []

    for node in bsp.pre_order():
        if node.children:
            node1, node2 = node.children
            for x, y in tunnel_between((node1.x+(node1.width >> 1) + random.randint(-2,2), node1.y+(node1.height >> 1)), (node2.x+(node2.width >> 1), node2.y+(node2.height >> 1)+ random.randint(-2,2))):
                dungeon.tiles[x, y] = tile_types.floor
        else:
            rooms.append(RectangularRoom(node.x, node.y, node.width, node.height))

    for i, room in enumerate(rooms):
        dungeon.tiles[room.inner] = tile_types.floor

        if i == 0:
            player.place(*room.center, dungeon)
        elif i + 1 == len(rooms):
            dungeon.tiles[room.center] = tile_types.down_stairs
            dungeon.downstairs_location = room.center
            
        place_entities(room, dungeon, engine.game_world.current_floor)

    return dungeon

def generate_cave_dungeon(
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    random_array = np.random.rand(map_width,map_height)

    for i in range(1, map_width-1):
        for j in range(1, map_height-1):
            if random_array[i,j] < 0.45: 
                dungeon.tiles[i,j] = tile_types.floor

    for _ in range(0, 6):
        new_tiles = np.full((map_width, map_height), fill_value=tile_types.wall, order="F")
        for i in range(1, map_width-1):
            for j in range(1, map_height-1):
                sum = 0
                if dungeon.tiles[i+1,j] == tile_types.wall:
                    sum += 1
                if dungeon.tiles[i+1,j+1] == tile_types.wall:
                    sum += 1
                if dungeon.tiles[i+1,j-1] == tile_types.wall:
                    sum += 1
                if dungeon.tiles[i,j+1] == tile_types.wall:
                    sum += 1
                if dungeon.tiles[i,j-1] == tile_types.wall:
                    sum += 1
                if dungeon.tiles[i-1,j] == tile_types.wall:
                    sum += 1
                if dungeon.tiles[i-1,j+1] == tile_types.wall:
                    sum += 1
                if dungeon.tiles[i-1,j-1] == tile_types.wall:
                    sum += 1
                if sum == 8 or sum > 4:
                    new_tiles[i,j] = tile_types.wall
                else:
                    new_tiles[i,j] = tile_types.floor
        dungeon.tiles = copy.deepcopy(new_tiles)

    for i in range(0, map_width):
        dungeon.tiles[i,0] = tile_types.wall
        dungeon.tiles[i,map_height-1] = tile_types.wall
    for j in range(0, map_height):
        dungeon.tiles[0,j] = tile_types.wall
        dungeon.tiles[map_width-1,j] = tile_types.wall
    
    x = map_width >> 1
    y = map_height >> 1
    while dungeon.tiles[x, y] == tile_types.wall:
        x -= 1
        if x == 1:
            y -= 1
            x = map_width >> 1
            if y == 1:
                y = map_height - 1
    player.place(x,y, dungeon)
    
    exit_x = map_width - 5
    exit_y = map_height - 5
    while dungeon.tiles[exit_x, exit_y] == tile_types.wall:
        exit_x -= 1
        exit_y -= 1
    
    for i in range(10):
        dungeon.tiles[exit_x - i, exit_y-i] = tile_types.floor
        dungeon.tiles[exit_x - i + 1, exit_y-i] = tile_types.floor
        dungeon.tiles[exit_x - i, exit_y-i + 1] = tile_types.floor

    dungeon.tiles[exit_x, exit_y] = tile_types.down_stairs
    dungeon.downstairs_location = exit_x, exit_y

    floor_num = engine.game_world.current_floor

    monsters: List[Entity] = get_entities_at_random(enemy_chances, 100, floor_num)
    items: List[Entity] = get_entities_at_random(item_chances, 100, floor_num)

    monster_num = get_max_value_for_floor(max_monsters_by_floor, floor_num)
    entity_num = get_max_value_for_floor(max_items_by_floor, floor_num) + monster_num

    for i in range(1, map_width-1):
        for j in range(1, map_height-1):
            if dungeon.tiles[i,j] == tile_types.floor and not (i == x and j == y):
                if random.randint(0, 1000) < 40:
                    if random.randint(0, entity_num) < monster_num:
                        entity = monsters[random.randint(0, 99)]
                    else:
                        entity = items[random.randint(0, 99)]
                    entity.spawn(dungeon, i, j)

    return dungeon