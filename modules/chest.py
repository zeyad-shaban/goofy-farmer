from OpenGL.GL import *  
from .base_classes import GameObject, Interactable, Collidable  
from .items import Item, ItemType  
from ui.inventory import Inventory  
from typing import TYPE_CHECKING  
  
if TYPE_CHECKING:  
    from .player import Player  
  
class Chest(Interactable, Collidable):  
    def __init__(self, position=(0, 0, 0), size=(1.0, 1.0, 1.0)):  
        super().__init__(position, size)  
        self.inventory = Inventory(rows=3, cols=5)  # Chest has 3x9 inventory  
        self.is_open = False  
      
    def draw(self):  
        # Draw chest box  
        glColor3f(0.5, 0.3, 0.1)  # Brown wood color  
        glBegin(GL_QUADS)  
          
        width, height, depth = 0.8, 0.8, 0.8  
          
        # Front face  
        glVertex3f(-width, 0, -depth)  
        glVertex3f(width, 0, -depth)  
        glVertex3f(width, height, -depth)  
        glVertex3f(-width, height, -depth)  
          
        # Back face  
        glVertex3f(width, 0, depth)  
        glVertex3f(-width, 0, depth)  
        glVertex3f(-width, height, depth)  
        glVertex3f(width, height, depth)  
          
        # Top face (lid)  
        if self.is_open:  
            # Open lid at 45 degrees  
            glVertex3f(-width, height, -depth)  
            glVertex3f(width, height, -depth)  
            glVertex3f(width, height + width, 0)  
            glVertex3f(-width, height + width, 0)  
        else:  
            # Closed lid  
            glVertex3f(-width, height, -depth)  
            glVertex3f(width, height, -depth)  
            glVertex3f(width, height, depth)  
            glVertex3f(-width, height, depth)  
          
        # Bottom face  
        glVertex3f(-width, 0, depth)  
        glVertex3f(width, 0, depth)  
        glVertex3f(width, 0, -depth)  
        glVertex3f(-width, 0, -depth)  
          
        # Left face  
        glVertex3f(-width, 0, -depth)  
        glVertex3f(-width, 0, depth)  
        glVertex3f(-width, height, depth)  
        glVertex3f(-width, height, -depth)  
          
        # Right face  
        glVertex3f(width, 0, -depth)  
        glVertex3f(width, 0, depth)  
        glVertex3f(width, height, depth)  
        glVertex3f(width, height, -depth)  
          
        glEnd()  
      
    def get_collision_box(self):  
        """Chest collision box."""  
        from .base_classes import BoundingBox  
        return BoundingBox(-0.4, 0.4, 0, 0.8, -0.4, 0.4)  
      
    def on_interact(self, interactor: "Player") -> str:  
        self.is_open = not self.is_open  
        if self.is_open:  
            return "Opened chest"  
        else:  
            return "Closed chest"  
      
    def get_interaction_prompt(self) -> str:  
        return "Press E to open chest"