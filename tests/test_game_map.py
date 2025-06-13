"""
Tests for the game map system.
"""

import pytest
from src.yendoria.game_map.game_map import GameMap
from src.yendoria.game_map.tile import floor, wall
from src.yendoria.game_map.room import RectangularRoom, tunnel_between


class TestGameMap:
    """Test cases for the GameMap class."""
    
    def test_game_map_creation(self):
        """Test basic game map creation."""
        game_map = GameMap(20, 15)
        
        assert game_map.width == 20
        assert game_map.height == 15
        assert game_map.tiles.shape == (20, 15)
        assert len(game_map.rooms) == 0
        
    def test_bounds_checking(self):
        """Test map bounds checking."""
        game_map = GameMap(10, 10)
        
        assert game_map.in_bounds(0, 0) is True
        assert game_map.in_bounds(9, 9) is True
        assert game_map.in_bounds(-1, 0) is False
        assert game_map.in_bounds(0, -1) is False
        assert game_map.in_bounds(10, 0) is False
        assert game_map.in_bounds(0, 10) is False
        
    def test_walkability(self):
        """Test walkability checking."""
        game_map = GameMap(10, 10)
        
        # Initially all walls (not walkable)
        assert game_map.is_walkable(5, 5) is False
        
        # Set a floor tile
        game_map.tiles[5, 5] = floor
        assert game_map.is_walkable(5, 5) is True
        
        # Out of bounds should not be walkable
        assert game_map.is_walkable(-1, 5) is False
        assert game_map.is_walkable(15, 5) is False
        
    def test_dungeon_generation(self):
        """Test dungeon generation."""
        game_map = GameMap(80, 43)
        player_x, player_y = game_map.generate_dungeon()
        
        # Should have generated rooms
        assert len(game_map.rooms) > 0
        
        # Player position should be valid
        assert game_map.in_bounds(player_x, player_y)
        assert game_map.is_walkable(player_x, player_y)
        
        # Should have some floor tiles
        floor_count = 0
        for x in range(game_map.width):
            for y in range(game_map.height):
                if game_map.tiles[x, y] == floor:
                    floor_count += 1
                    
        assert floor_count > 0


class TestRectangularRoom:
    """Test cases for the RectangularRoom class."""
    
    def test_room_creation(self):
        """Test room creation and properties."""
        room = RectangularRoom(5, 10, 8, 6)
        
        assert room.x1 == 5
        assert room.y1 == 10
        assert room.x2 == 13  # 5 + 8
        assert room.y2 == 16  # 10 + 6
        
    def test_room_center(self):
        """Test room center calculation."""
        room = RectangularRoom(10, 20, 10, 8)
        center_x, center_y = room.center
        
        assert center_x == 15  # (10 + 20) / 2
        assert center_y == 24  # (20 + 28) / 2
        
    def test_room_inner_area(self):
        """Test room inner area calculation."""
        room = RectangularRoom(5, 5, 6, 4)
        inner_x, inner_y = room.inner
        
        assert inner_x == slice(6, 11)  # x1+1 to x2
        assert inner_y == slice(6, 9)   # y1+1 to y2
        
    def test_room_intersection(self):
        """Test room intersection detection."""
        room1 = RectangularRoom(5, 5, 10, 10)
        room2 = RectangularRoom(10, 10, 10, 10)  # Overlapping
        room3 = RectangularRoom(20, 20, 5, 5)    # Non-overlapping
        
        assert room1.intersects(room2) is True
        assert room1.intersects(room3) is False
        assert room2.intersects(room3) is False


class TestTileSystem:
    """Test cases for the tile system."""
    
    def test_floor_tile_properties(self):
        """Test floor tile properties."""
        assert floor.walkable is True
        assert floor.transparent is True
        assert floor.dark is not None
        assert floor.light is not None
        
    def test_wall_tile_properties(self):
        """Test wall tile properties."""
        assert wall.walkable is False
        assert wall.transparent is False
        assert wall.dark is not None
        assert wall.light is not None
