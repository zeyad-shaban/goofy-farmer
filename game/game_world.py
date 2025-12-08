from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Optional, List
from modules.player import Player
from modules.base_classes import GameObject, Collidable
from ui.dialogue_box import DialogueBox
from utils.utils import draw_collision_box
from ui.hotbar import Hotbar
from ui.inventory import Inventory
from modules.chest import Chest
import math


class GameWorld:
    """Manages all game objects and interactions."""

    def __init__(self):
        self.objects: List[GameObject] = []
        self.player: [Player] = None
        self.dialogue_box = DialogueBox()
        self.hotbar = Hotbar()
        self.inventory = Inventory()
        self.opened_chest: Optional[Chest] = None

    def add_object(self, obj: GameObject) -> None:
        """Add an object to the world."""
        self.objects.append(obj)
        if isinstance(obj, Player):
            self.player = obj

    def get_collidables(self) -> List[Collidable]:
        """Get all collidable objects."""
        return [obj for obj in self.objects if isinstance(obj, Collidable)]

    def update(self, delta_time: float) -> None:
        """Update all objects."""
        for obj in self.objects:
            obj.update(delta_time)
        self.dialogue_box.update(delta_time)

    def draw(self, window_width: int, window_height: int) -> None:
        """Draw all objects."""
        for obj in self.objects:
            from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslatef

            glPushMatrix()
            glTranslatef(*obj.position)
            obj.draw()
            glPopMatrix()
            self.hotbar.draw(window_width, window_height)

        self.dialogue_box.draw(window_width, window_height)

    def handle_player_interaction(self) -> None:
        """Handle player trying to interact with nearby objects."""
        if not self.player:
            return

        interactable = self.player.find_interactable(self.objects)
        if interactable:
            message = self.player.interact_with(interactable)
            self.dialogue_box.show_message(message)

    def draw_collisions(self):
        for obj in self.objects:
            if isinstance(obj, Collidable):
                glPushMatrix()
                glTranslatef(*obj.position)
                glScalef(*obj.size)

                # Draw in different colors for different objects
                if isinstance(obj, Player):
                    draw_collision_box(obj.get_collision_box(), (0.0, 1.0, 0.0, 0.5))  # Green for player
                else:
                    draw_collision_box(obj.get_collision_box(), (1.0, 0.0, 0.0, 0.5))  # Red for others

                glPopMatrix()

    # chest handling
    def open_chest(self, chest: Chest):
        """Open a chest inventory UI."""
        self.opened_chest = chest
        chest.is_open = True

    def close_chest(self):
        """Close the currently open chest."""
        if self.opened_chest:
            self.opened_chest.is_open = False
            self.opened_chest = None

    def handle_inventory_click(self, mouse_x: int, mouse_y: int, window_width: int, window_height: int):
        """Handle mouse clicks on inventory slots."""
        if not self.opened_chest or not self.player:
            return

        for row in range(self.opened_chest.inventory.rows):
            for col in range(self.opened_chest.inventory.cols):
                item = self.opened_chest.inventory.get_item(row, col)
                if item:
                    if self.player.inventory.add_item(item):
                        self.opened_chest.inventory.remove_item(row, col)
                    return
