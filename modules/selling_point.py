from modules.base_classes import Collidable, Interactable, BoundingBox, Vec3
from modules.items import Item, ItemType
from OpenGL.GL import *
from OpenGL.GLU import *


class SellingPoint(Collidable, Interactable):
    """A selling point where the player can sell items."""

    def __init__(self, position: Vec3 = (0.0, 0.0, 0.0), size: Vec3 = (1.0, 1.0, 1.0)):
        super().__init__(position, size)

    def get_collision_box(self) -> BoundingBox:
        """Return collision box for this selling point."""
        return BoundingBox(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)

    def on_interact(self, interactor) -> str:
        """Sell the item the player is currently holding."""
        from modules.player import Player
        
        if not isinstance(interactor, Player):
            return "Cannot sell"

        hotbar_item = interactor.hotbar.items[interactor.hotbar.selected_slot]
        
        if hotbar_item is None:
            return "You're not holding anything to sell!"

        price = hotbar_item.get_price() # type: ignore
        
        if price <= 0:
            return f"Can't sell {hotbar_item.get_name()}!"

        interactor.coins += price
        hotbar_item.stack_size -= 1
        
        if hotbar_item.stack_size <= 0:
            interactor.hotbar.items[interactor.hotbar.selected_slot] = None

        return f"Sold {hotbar_item.get_name()} for ${price}!"

    def get_interaction_prompt(self) -> str:
        """Return interaction prompt text."""
        return "Press E to sell held item"

    def draw(self) -> None:
        """Draw the selling point as a pedestal."""
        size_x = self.size[0] / 2
        size_y = self.size[1] / 2
        size_z = self.size[2] / 2

        # Main pedestal - yellow/gold color
        glColor3f(1.0, 0.85, 0.0)
        glBegin(GL_QUADS)

        # Front
        glVertex3f(-size_x, -size_y, size_z)
        glVertex3f(size_x, -size_y, size_z)
        glVertex3f(size_x, size_y, size_z)
        glVertex3f(-size_x, size_y, size_z)

        # Back
        glVertex3f(-size_x, -size_y, -size_z)
        glVertex3f(-size_x, size_y, -size_z)
        glVertex3f(size_x, size_y, -size_z)
        glVertex3f(size_x, -size_y, -size_z)

        # Top
        glVertex3f(-size_x, size_y, -size_z)
        glVertex3f(size_x, size_y, -size_z)
        glVertex3f(size_x, size_y, size_z)
        glVertex3f(-size_x, size_y, size_z)

        # Bottom
        glVertex3f(-size_x, -size_y, -size_z)
        glVertex3f(size_x, -size_y, -size_z)
        glVertex3f(size_x, -size_y, size_z)
        glVertex3f(-size_x, -size_y, size_z)

        # Left
        glVertex3f(-size_x, -size_y, -size_z)
        glVertex3f(-size_x, size_y, -size_z)
        glVertex3f(-size_x, size_y, size_z)
        glVertex3f(-size_x, -size_y, size_z)

        # Right
        glVertex3f(size_x, -size_y, -size_z)
        glVertex3f(size_x, -size_y, size_z)
        glVertex3f(size_x, size_y, size_z)
        glVertex3f(size_x, size_y, -size_z)

        glEnd()

        # Top accent - brighter gold
        glColor3f(1.0, 1.0, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(-size_x * 0.8, size_y + 0.1, -size_z * 0.8)
        glVertex3f(size_x * 0.8, size_y + 0.1, -size_z * 0.8)
        glVertex3f(size_x * 0.8, size_y + 0.1, size_z * 0.8)
        glVertex3f(-size_x * 0.8, size_y + 0.1, size_z * 0.8)
        glEnd()
