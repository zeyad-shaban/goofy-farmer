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
        super().__init__(position)
        self.has_been_opened = False
        self.size = size

    def draw(self) -> None:
        """Draw a simple crate."""
        size = self.size

        glColor3f(0.6, 0.4, 0.2)  # Brown color

        glBegin(GL_QUADS)
        # Front
        glVertex3f(-size, 0, size)
        glVertex3f(size, 0, size)
        glVertex3f(size, size * 2, size)
        glVertex3f(-size, size * 2, size)
        # Back
        glVertex3f(size, 0, -size)
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, size * 2, -size)
        glVertex3f(size, size * 2, -size)
        # Left
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, 0, size)
        glVertex3f(-size, size * 2, size)
        glVertex3f(-size, size * 2, -size)
        # Right
        glVertex3f(size, 0, size)
        glVertex3f(size, 0, -size)
        glVertex3f(size, size * 2, -size)
        glVertex3f(size, size * 2, size)
        # Top
        glVertex3f(-size, size * 2, size)
        glVertex3f(size, size * 2, size)
        glVertex3f(size, size * 2, -size)
        glVertex3f(-size, size * 2, -size)
        # Bottom
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glEnd()

    def get_collision_box(self) -> BoundingBox:
        """Crate collision box."""
        size = self.size
        return BoundingBox(-size, size, 0, size * 2, -size, size)

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
