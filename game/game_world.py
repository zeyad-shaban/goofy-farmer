from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Optional, List
from modules.player import Player
from modules.base_classes import GameObject, Collidable
from ui.dialogue_box import DialogueBox
from utils.utils import draw_collision_box
import math


class GameWorld:
    """Manages all game objects and interactions."""

    def __init__(self):
        self.objects: List[GameObject] = []
        self.player: Optional[Player] = None
        self.dialogue_box = DialogueBox()

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

                # Draw in different colors for different objects
                if isinstance(obj, Player):
                    draw_collision_box(obj.get_collision_box(), (0.0, 1.0, 0.0, 0.5))  # Green for player
                else:
                    draw_collision_box(obj.get_collision_box(), (1.0, 0.0, 0.0, 0.5))  # Red for others

                glPopMatrix()
