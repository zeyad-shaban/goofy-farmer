from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Optional, List
import math


class DialogueBox:
    """Semi-transparent dialogue box at bottom of screen."""

    def __init__(self):
        self.current_message: str = ""
        self.display_time: float = 0.0
        self.max_display_time: float = 3.0  # seconds

    def show_message(self, message: str) -> None:
        """Display a new message."""
        self.current_message = message
        self.display_time = self.max_display_time

    def update(self, delta_time: float) -> None:
        """Update dialogue display timer."""
        if self.display_time > 0:
            self.display_time -= delta_time

    def draw(self, window_width: int, window_height: int) -> None:
        """Draw the dialogue box."""
        if self.display_time <= 0 or not self.current_message:
            return

        from OpenGL.GL import (
            glMatrixMode,
            glPushMatrix,
            glPopMatrix,
            glLoadIdentity,
            glBegin,
            glEnd,
            glVertex2f,
            glColor4f,
            GL_PROJECTION,
            GL_MODELVIEW,
            GL_QUADS,
            glEnable,
            glDisable,
            GL_BLEND,
            glBlendFunc,
            GL_SRC_ALPHA,
            GL_ONE_MINUS_SRC_ALPHA,
        )
        from OpenGL.GLU import gluOrtho2D

        # Switch to 2D orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, window_width, 0, window_height)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Enable transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Draw semi-transparent box at bottom
        box_height = 80
        padding = 20

        glColor4f(0.0, 0.0, 0.0, 0.7)  # Semi-transparent black
        glBegin(GL_QUADS)
        glVertex2f(padding, padding)
        glVertex2f(window_width - padding, padding)
        glVertex2f(window_width - padding, padding + box_height)
        glVertex2f(padding, padding + box_height)
        glEnd()

        # Note: For text rendering, you'd need to use pygame font or a library like PyOpenGL-accelerate
        # For now, this draws the box. You can add text rendering separately.

        glDisable(GL_BLEND)

        # Restore previous projection
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
