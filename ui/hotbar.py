import pygame
from typing import List, Optional
from modules.items import Item, ItemType
from OpenGL.GL import *
from OpenGL.GLU import *
from utils.texture_cache import TextureCache


class Hotbar:
    def __init__(self):
        self.slot_count = 5
        self.selected_slot = 0  # 0 to 4
        self.items: List[List[Optional[Item]]] = [None] * self.slot_count  # type: ignore

        # Visual settings
        self.slot_size = 50
        self.padding = 10
        self.color_selected = (1.0, 1.0, 0.0, 0.8)  # Yellow, semi-transparent
        self.color_default = (0.2, 0.2, 0.2, 0.5)  # Dark Gray, semi-transparent
        self.border_color = (1.0, 1.0, 1.0, 1.0)  # White border

    def select_slot(self, index: int):
        """Change the selected slot (0-indexed)."""
        if 0 <= index < self.slot_count:
            self.selected_slot = index

    def scroll(self, direction: int):
        """Scroll selection: +1 for right, -1 for left."""
        self.selected_slot = (self.selected_slot + direction) % self.slot_count

    def add_item(self, item) -> bool:
        """Add item to first available hotbar slot."""
        for i in range(self.slot_count):
            if self.items[i] is None:
                self.items[i] = item
                return True
            elif self.items[i].type == item.type:
                # Stack with existing item
                if self.items[i].stack_size < self.items[i].max_stack:
                    self.items[i].stack_size += item.stack_size
                    return True
        return False

    def draw(self, window_width: int, window_height: int):
        """Draw the hotbar with items."""
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

        slot_size = 50
        padding = 5
        total_width = (slot_size * len(self.items)) + (padding * (len(self.items) - 1))
        start_x = (window_width - total_width) / 2
        start_y = 20

        for i, item in enumerate(self.items):
            slot_x = start_x + (i * (slot_size + padding))
            slot_y = start_y

            # Draw slot background
            if i == self.selected_slot:
                glColor4f(1.0, 1.0, 0.0, 0.8)  # Yellow for selected
            else:
                glColor4f(0.3, 0.3, 0.3, 0.5)  # Gray for unselected

            glBegin(GL_QUADS)
            glVertex2f(slot_x, slot_y)
            glVertex2f(slot_x + slot_size, slot_y)
            glVertex2f(slot_x + slot_size, slot_y + slot_size)
            glVertex2f(slot_x, slot_y + slot_size)
            glEnd()

            # Draw item if present
            if item:
                # Try to load and draw texture
                texture_path = item.get_texture_path()
                texture_id = TextureCache.get_texture(texture_path) if texture_path else None
                
                if texture_id:
                    # Draw textured quad
                    glBindTexture(GL_TEXTURE_2D, texture_id)
                    glColor3f(1.0, 1.0, 1.0)
                    margin = 5
                    glBegin(GL_QUADS)
                    glTexCoord2f(0, 0)
                    glVertex2f(slot_x + margin, slot_y + margin)
                    glTexCoord2f(1, 0)
                    glVertex2f(slot_x + slot_size - margin, slot_y + margin)
                    glTexCoord2f(1, 1)
                    glVertex2f(slot_x + slot_size - margin, slot_y + slot_size - margin)
                    glTexCoord2f(0, 1)
                    glVertex2f(slot_x + margin, slot_y + slot_size - margin)
                    glEnd()
                    glBindTexture(GL_TEXTURE_2D, 0)
                else:
                    # Fallback to color if texture not found
                    color = item.get_color()
                    glColor3f(*color)
                    glBegin(GL_QUADS)
                    margin = 5
                    glVertex2f(slot_x + margin, slot_y + margin)
                    glVertex2f(slot_x + slot_size - margin, slot_y + margin)
                    glVertex2f(slot_x + slot_size - margin, slot_y + slot_size - margin)
                    glVertex2f(slot_x + margin, slot_y + slot_size - margin)
                    glEnd()

                # Draw stack count if > 1
                if item.stack_size > 1:
                    glColor3f(1.0, 1.0, 1.0)
                    glBegin(GL_QUADS)
                    glVertex2f(slot_x + slot_size - 20, slot_y)
                    glVertex2f(slot_x + slot_size, slot_y)
                    glVertex2f(slot_x + slot_size, slot_y + 20)
                    glVertex2f(slot_x + slot_size - 20, slot_y + 20)
                    glEnd()

            # Draw border
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glLineWidth(2.0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(slot_x, slot_y)
            glVertex2f(slot_x + slot_size, slot_y)
            glVertex2f(slot_x + slot_size, slot_y + slot_size)
            glVertex2f(slot_x, slot_y + slot_size)
            glEnd()

        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
