from OpenGL.GL import *
from .base_classes import GameObject, Collidable, Interactable, Pickable
from typing import TYPE_CHECKING
from .player import Player
from .items import Item, ItemType


class Hoe(GameObject, Interactable, Pickable):
    def __init__(self, position=(0, 0, 0), size=(1, 1, 1)):
        super().__init__(position, size)
        self.picked_up = False

    def draw(self):
        if self.picked_up:
            return

        # Brown wooden handle
        glColor3f(0.55, 0.27, 0.07)  # Brown color
        glBegin(GL_QUADS)
        # Handle sides (simplified as a rectangular prism)
        handle_length = 2.0
        handle_width = 0.1
        handle_height = 0.1

        # Front face
        glVertex3f(-handle_width, 0, 0)
        glVertex3f(handle_width, 0, 0)
        glVertex3f(handle_width, handle_height, 0)
        glVertex3f(-handle_width, handle_height, 0)

        # Back face
        glVertex3f(handle_width, 0, -handle_length)
        glVertex3f(-handle_width, 0, -handle_length)
        glVertex3f(-handle_width, handle_height, -handle_length)
        glVertex3f(handle_width, handle_height, -handle_length)

        # Top face
        glVertex3f(-handle_width, handle_height, 0)
        glVertex3f(handle_width, handle_height, 0)
        glVertex3f(handle_width, handle_height, -handle_length)
        glVertex3f(-handle_width, handle_height, -handle_length)

        # Bottom face
        glVertex3f(-handle_width, 0, 0)
        glVertex3f(handle_width, 0, 0)
        glVertex3f(handle_width, 0, -handle_length)
        glVertex3f(-handle_width, 0, -handle_length)

        # Left face
        glVertex3f(-handle_width, 0, 0)
        glVertex3f(-handle_width, 0, -handle_length)
        glVertex3f(-handle_width, handle_height, -handle_length)
        glVertex3f(-handle_width, handle_height, 0)

        # Right face
        glVertex3f(handle_width, 0, 0)
        glVertex3f(handle_width, 0, -handle_length)
        glVertex3f(handle_width, handle_height, -handle_length)
        glVertex3f(handle_width, handle_height, 0)
        glEnd()

        # Black metal blade
        glColor3f(0.1, 0.1, 0.1)  # Dark gray/black
        glBegin(GL_QUADS)
        blade_width = 0.4
        blade_height = 0.05
        blade_length = 0.3

        # Blade (attached to end of handle)
        glVertex3f(-blade_width, 0, -handle_length - blade_length)
        glVertex3f(blade_width, 0, -handle_length - blade_length)
        glVertex3f(blade_width, blade_height, -handle_length)
        glVertex3f(-blade_width, blade_height, -handle_length)
        glEnd()

    def on_interact(self, interactor: "Player") -> str:
        return self.on_pickup(interactor)

    def get_interaction_prompt(self) -> str:
        return "Pick up hoe"

    def get_item_type(self) -> ItemType:
        return ItemType.HOE

    def on_pickup(self, interactor: "Player") -> str:
        """Pick up the hoe."""
        result = Pickable.try_pickup_item(self, interactor)
        if "Picked up" in result:
            self.picked_up = True
        return result