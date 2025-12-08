from modules.items import Item, ItemType
from typing import List, Optional
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class Inventory:
    def __init__(self, rows: int = 4, cols: int = 9):
        self.rows = rows
        self.cols = cols
        self.slot_size = 40
        self.padding = 5
        self.is_open = False
        self.items: List[List[Optional[Item]]] = [[None for _ in range(cols)] for _ in range(rows)]
        self.selected_slot = (0, 0)

        self.color_selected = (1.0, 1.0, 0.0, 0.8)
        self.color_default = (0.2, 0.2, 0.2, 0.5)
        self.border_color = (1.0, 1.0, 1.0, 1.0)

    # todo modify this to stack if possible
    def add_item(self, item: Item) -> bool:
        """Add item to first available slot."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.items[row][col] is None:
                    self.items[row][col] = item
                    return True
                elif self.items[row][col].type == item.type:
                    # Stack with existing item
                    if self.items[row][col].stack_size < self.items[row][col].max_stack:
                        self.items[row][col].stack_size += item.stack_size
                        return True
        return False
    
    def remove_item(self, row: int, col: int) -> Optional[Item]:
        """Remove item from slot."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            item = self.items[row][col]
            self.items[row][col] = None
            return item
        return None

    def get_item(self, row: int, col: int) -> Optional[Item]:
        """Get item from slot without removing."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.items[row][col]
        return None

    def transfer_item(self, from_row: int, from_col: int, other_inventory: "Inventory", to_row: int, to_col: int) -> bool:
        """Transfer item between inventories."""
        item = self.remove_item(from_row, from_col)
        if item:
            if other_inventory.items[to_row][to_col] is None:
                other_inventory.items[to_row][to_col] = item
                return True
            elif other_inventory.items[to_row][to_col].type == item.type:
                # Stack items
                space = other_inventory.items[to_row][to_col].max_stack - other_inventory.items[to_row][to_col].stack_size
                if space >= item.stack_size:
                    other_inventory.items[to_row][to_col].stack_size += item.stack_size
                    return True
                else:
                    # Partial stack
                    other_inventory.items[to_row][to_col].stack_size += space
                    item.stack_size -= space
                    self.items[from_row][from_col] = item  # Put back remaining
                    return True
            else:
                # Swap items
                swap_item = other_inventory.remove_item(to_row, to_col)
                other_inventory.items[to_row][to_col] = item
                self.items[from_row][from_col] = swap_item
                return True
        return False

    def draw(self, window_width: int, window_height: int, title: str = "Inventory", offset_y: int = 0):
        """Draw the inventory grid with optional title and vertical offset."""
        # Setup 2D projection (same as hotbar)
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

        # Center the inventory
        total_width = (self.slot_size * self.cols) + (self.padding * (self.cols - 1))
        total_height = (self.slot_size * self.rows) + (self.padding * (self.rows - 1))
        start_x = (window_width - total_width) / 2
        start_y = offset_y

        # Draw title if provided
        if title:
            # Simple title rendering (you might want to use pygame font later)
            glColor3f(1.0, 1.0, 1.0)
            title_y = start_y + total_height + 20
            # For now, just draw a line as title placeholder
            glBegin(GL_LINES)
            glVertex2f(start_x, title_y)
            glVertex2f(start_x + total_width, title_y)
            glEnd()

        # Draw slots
        for row in range(self.rows):
            for col in range(self.cols):
                x = start_x + (col * (self.slot_size + self.padding))
                y = start_y + (row * (self.slot_size + self.padding))

                # Color based on selection
                if (row, col) == self.selected_slot:
                    glColor4f(*self.color_selected)
                else:
                    glColor4f(*self.color_default)

                # Draw slot
                glBegin(GL_QUADS)
                glVertex2f(x, y)
                glVertex2f(x + self.slot_size, y)
                glVertex2f(x + self.slot_size, y + self.slot_size)
                glVertex2f(x, y + self.slot_size)
                glEnd()

                # Draw item if present
                item = self.items[row][col]
                if item:
                    glColor3f(*item.get_color())
                    item_margin = 5
                    glBegin(GL_QUADS)
                    glVertex2f(x + item_margin, y + item_margin)
                    glVertex2f(x + self.slot_size - item_margin, y + item_margin)
                    glVertex2f(x + self.slot_size - item_margin, y + self.slot_size - item_margin)
                    glVertex2f(x + item_margin, y + self.slot_size - item_margin)
                    glEnd()

                # Draw border
                glColor4f(*self.border_color)
                glLineWidth(2.0)
                glBegin(GL_LINE_LOOP)
                glVertex2f(x, y)
                glVertex2f(x + self.slot_size, y)
                glVertex2f(x + self.slot_size, y + self.slot_size)
                glVertex2f(x, y + self.slot_size)
                glEnd()

        # Restore state
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
