import pygame
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

        # Initialize pygame font
        pygame.font.init()
        self.font = pygame.font.Font(None, 32)  # Default font, size 32
        self.text_color = (255, 255, 255)  # White text

    def show_message(self, message: str) -> None:
        """Display a new message."""
        self.current_message = message
        self.display_time = self.max_display_time

    def update(self, delta_time: float) -> None:
        """Update dialogue display timer."""
        if self.display_time > 0:
            self.display_time -= delta_time

    def draw(self, window_width: int, window_height: int) -> None:
        """Draw the dialogue box with text."""
        if self.display_time <= 0 or not self.current_message:
            return

        # Switch to 2D orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, window_width, 0, window_height)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Disable depth test for UI rendering
        glDisable(GL_DEPTH_TEST)

        # Enable transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Draw semi-transparent box at bottom
        box_height = 100
        padding = 20

        glColor4f(0.0, 0.0, 0.0, 0.7)  # Semi-transparent black
        glBegin(GL_QUADS)
        glVertex2f(padding, padding)
        glVertex2f(window_width - padding, padding)
        glVertex2f(window_width - padding, padding + box_height)
        glVertex2f(padding, padding + box_height)
        glEnd()

        # Render text using pygame
        text_surface = self.font.render(self.current_message, True, self.text_color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        text_width, text_height = text_surface.get_size()

        # Calculate text position (centered in the box)
        text_x = padding + 15
        text_y = padding + (box_height - text_height) // 2

        # Draw text as texture
        glRasterPos2f(text_x, text_y)
        glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glDisable(GL_BLEND)

        # Re-enable depth test
        glEnable(GL_DEPTH_TEST)

        # Restore previous projection
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
