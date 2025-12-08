from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Optional, List, Tuple
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
        self.player: list[Player] = None
        self.dialogue_box = DialogueBox()
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
        
        # Check chest inventory click (top half)  
        chest_clicked = self._get_clicked_slot(  
            mouse_x, mouse_y, window_width, window_height,  
            self.opened_chest.inventory, window_height // 2  
        )  
        
        if chest_clicked:  
            row, col = chest_clicked  
            item = self.opened_chest.inventory.get_item(row, col)  
            if item and self.player.inventory.add_item(item):  
                self.opened_chest.inventory.remove_item(row, col)  
            return  
        
        # Check player inventory click (bottom half)  
        player_clicked = self._get_clicked_slot(  
            mouse_x, mouse_y, window_width, window_height,  
            self.player.inventory, 100  
        )  
        
        if player_clicked:  
            row, col = player_clicked  
            # Transfer from player to chest  
            item = self.player.inventory.get_item(row, col)  
            if item and self.opened_chest.inventory.add_item(item):  
                self.player.inventory.remove_item(row, col)  
    
    def _get_clicked_slot(self, mouse_x: int, mouse_y: int, window_width: int, window_height: int,   
                        inventory: 'Inventory', offset_y: int) -> Optional[Tuple[int, int]]:  
        """Get which slot was clicked based on mouse coordinates."""  
        # Convert to openGL coords for Y (TL -> BL)
        mouse_y_gl = window_height - mouse_y  
        
        # Calculate inventory position  
        total_width = (inventory.slot_size * inventory.cols) + (inventory.padding * (inventory.cols - 1))  
        start_x = (window_width - total_width) / 2  
        start_y = offset_y  
        
        # Check if click is within inventory bounds  
        if (mouse_x < start_x or mouse_x > start_x + total_width or  
            mouse_y_gl < start_y or mouse_y_gl > start_y +   
            (inventory.slot_size * inventory.rows) + (inventory.padding * (inventory.rows - 1))):  
            return None  
        
        # Calculate which slot was clicked  
        for row in range(inventory.rows):  
            for col in range(inventory.cols):  
                slot_x = start_x + (col * (inventory.slot_size + inventory.padding))  
                slot_y = start_y + (row * (inventory.slot_size + inventory.padding))  
                
                if (slot_x <= mouse_x <= slot_x + inventory.slot_size and  
                    slot_y <= mouse_y_gl <= slot_y + inventory.slot_size):  
                    return (row, col)  
        
        return None
