from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Optional, List
from .base_classes import Vec3, Collidable, Interactable, BoundingBox
from .player import Player
from OpenGL.GL import glBegin, glEnd, glVertex3f, glColor3f, GL_QUADS
import math


class Crate(Collidable, Interactable):
    """A crate that can be collided with and interacted with."""

    def __init__(self, position: Vec3 = (0.0, 0.0, 0.0), size=0.8):
        super().__init__(position, size)
        self.has_been_opened = False

    def draw(self) -> None:
        """Draw a simple crate."""
        local_size = 1

        glColor3f(0.6, 0.4, 0.2)  # Brown color

        glBegin(GL_QUADS)
        # Front
        glVertex3f(-local_size, 0, local_size)
        glVertex3f(local_size, 0, local_size)
        glVertex3f(local_size, local_size * 2, local_size)
        glVertex3f(-local_size, local_size * 2, local_size)
        # Back
        glVertex3f(local_size, 0, -local_size)
        glVertex3f(-local_size, 0, -local_size)
        glVertex3f(-local_size, local_size * 2, -local_size)
        glVertex3f(local_size, local_size * 2, -local_size)
        # Left
        glVertex3f(-local_size, 0, -local_size)
        glVertex3f(-local_size, 0, local_size)
        glVertex3f(-local_size, local_size * 2, local_size)
        glVertex3f(-local_size, local_size * 2, -local_size)
        # Right
        glVertex3f(local_size, 0, local_size)
        glVertex3f(local_size, 0, -local_size)
        glVertex3f(local_size, local_size * 2, -local_size)
        glVertex3f(local_size, local_size * 2, local_size)
        # Top
        glVertex3f(-local_size, local_size * 2, local_size)
        glVertex3f(local_size, local_size * 2, local_size)
        glVertex3f(local_size, local_size * 2, -local_size)
        glVertex3f(-local_size, local_size * 2, -local_size)
        # Bottom
        glVertex3f(-local_size, 0, -local_size)
        glVertex3f(local_size, 0, -local_size)
        glVertex3f(local_size, 0, local_size)
        glVertex3f(-local_size, 0, local_size)
        glEnd()

    def get_collision_box(self) -> BoundingBox:
        """Crate collision box."""
        local_size = 1
        return BoundingBox(-local_size, local_size, 0, local_size * 2, -local_size, local_size)

    def on_interact(self, interactor: Player) -> str:
        """Handle interaction with the crate."""
        print("interacted with lol")
        if not self.has_been_opened:
            self.has_been_opened = True
            return "You opened the crate! It's empty..."
        else:
            return "Hey stop! This crate is already opened."

    def get_interaction_prompt(self) -> str:
        return "Press E to open crate"
