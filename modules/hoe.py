from OpenGL.GL import *
from .base_classes import GameObject, Collidable, Interactable
from typing import TYPE_CHECKING
from .player import Player


class Hoe(GameObject, Interactable):
    def __init__(self, position=(0, 0, 0), size=(1, 1, 1)):
        super().__init__(position, size)

    def draw(self):
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
        return "You picked up the hoe!"

    def get_interaction_prompt(self) -> str:
        return "Pick up hoe"