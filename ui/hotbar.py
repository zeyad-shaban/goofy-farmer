import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Hotbar:
    def __init__(self):
        self.slot_count = 5
        self.selected_slot = 0  # 0 to 4
        self.items = [None] * self.slot_count  # Placeholder for item data
        
        # Visual settings
        self.slot_size = 50
        self.padding = 10
        self.color_selected = (1.0, 1.0, 0.0, 0.8)  # Yellow, semi-transparent
        self.color_default = (0.2, 0.2, 0.2, 0.5)   # Dark Gray, semi-transparent
        self.border_color = (1.0, 1.0, 1.0, 1.0)    # White border

    def select_slot(self, index: int):
        """Change the selected slot (0-indexed)."""
        if 0 <= index < self.slot_count:
            self.selected_slot = index

    def scroll(self, direction: int):
        """Scroll selection: +1 for right, -1 for left."""
        self.selected_slot = (self.selected_slot + direction) % self.slot_count

    def draw(self, window_width: int, window_height: int):
        """Draw the hotbar overlay."""
        # --- Setup 2D Orthographic Projection (Same as DialogueBox) ---
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, window_width, 0, window_height)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # --- Calculate Positioning ---
        # Center the hotbar at the bottom
        total_width = (self.slot_size * self.slot_count) + (self.padding * (self.slot_count - 1))
        start_x = (window_width - total_width) / 2
        start_y = 20  # Distance from bottom

        # --- Draw Slots ---
        for i in range(self.slot_count):
            x = start_x + (i * (self.slot_size + self.padding))
            y = start_y

            # Determine color based on selection
            if i == self.selected_slot:
                glColor4f(*self.color_selected)
            else:
                glColor4f(*self.color_default)

            # Draw Slot Background (Fill)
            glBegin(GL_QUADS)
            glVertex2f(x, y)
            glVertex2f(x + self.slot_size, y)
            glVertex2f(x + self.slot_size, y + self.slot_size)
            glVertex2f(x, y + self.slot_size)
            glEnd()

            # Draw Slot Border (Line)
            glColor4f(*self.border_color)
            glLineWidth(2.0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(x, y)
            glVertex2f(x + self.slot_size, y)
            glVertex2f(x + self.slot_size, y + self.slot_size)
            glVertex2f(x, y + self.slot_size)
            glEnd()

        # --- Restore OpenGL State ---
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)