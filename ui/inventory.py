import pygame  
from OpenGL.GL import *  
from OpenGL.GLU import *  
  
class Inventory:  
    def __init__(self):  
        self.rows = 4  
        self.cols = 9  
        self.slot_size = 40  
        self.padding = 5  
        self.is_open = False  
        self.items = [[None for _ in range(self.cols)] for _ in range(self.rows)]  
          
        # Visual settings (same as hotbar)  
        self.color_selected = (1.0, 1.0, 0.0, 0.8)  
        self.color_default = (0.2, 0.2, 0.2, 0.5)  
        self.border_color = (1.0, 1.0, 1.0, 1.0)  
        self.selected_slot = (0, 0)  # (row, col)  
      
    def toggle(self):  
        """Open/close inventory."""  
        self.is_open = not self.is_open  
      
    def draw(self, window_width: int, window_height: int):  
        """Draw the inventory grid if open."""  
        if not self.is_open:  
            return  
          
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
        start_y = (window_height - total_height) / 2  
          
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
        glMatrixMode(GL_MODELVIEW)