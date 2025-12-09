from enum import Enum
from typing import Optional
from OpenGL.GL import *
from OpenGL.GLU import *
from modules.base_classes import Collidable, Interactable, BoundingBox, Vec3
from modules.items import Item, ItemType
from utils.texture_cache import TextureCache


class BlockState(Enum):
    """States of a dirt block."""
    DIRT = "dirt"  # Normal dirt, texture: assets/dirt.png
    FARMLAND = "farmland"  # Tilled farmland, texture: assets/farmland.png
    PLANTED = "planted"  # Has crop growing, texture: crop texture on top


class DirtBlock(Collidable, Interactable):
    """A dirt block that can be tilled and farmed."""

    def __init__(self, position: Vec3 = (0.0, 0.0, 0.0), size: Vec3 = (1.0, 1.0, 1.0)):
        super().__init__(position, size)
        self.state = BlockState.DIRT
        self.uses_remaining = 3  # Can be used 3 times before returning to dirt
        self.planted_item_type: Optional[ItemType] = None  # What's planted on this block
        self.growth_timer = 0.0  # Time until crop is ready to harvest
        self.growth_duration = 5.0  # 5 seconds to grow

    def get_collision_box(self) -> BoundingBox:
        """Return collision box for this block."""
        return BoundingBox(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)

    def on_interact(self, interactor) -> str:
        """Handle interaction based on block state and what player is holding."""
        from modules.player import Player
        
        if not isinstance(interactor, Player):
            return "Cannot interact"

        # Check if player is holding a hoe (must be selected in hotbar)
        is_holding_hoe = (
            interactor.hotbar.items[interactor.hotbar.selected_slot] is not None
            and interactor.hotbar.items[interactor.hotbar.selected_slot].type == ItemType.HOE
        )

        # State: DIRT -> Can be tilled with hoe
        if self.state == BlockState.DIRT:
            if is_holding_hoe:
                self.state = BlockState.FARMLAND
                return "Tilled the dirt block!"
            else:
                return "This dirt needs a hoe to till"

        # State: FARMLAND -> Can plant seeds
        elif self.state == BlockState.FARMLAND:
            # Check if player is holding seeds
            hotbar_item = interactor.hotbar.items[interactor.hotbar.selected_slot]
            if hotbar_item and hotbar_item.type == ItemType.TOMATO_SEED:
                # Plant the seed
                self.plant_seed(hotbar_item, interactor)
                return "Planted tomato seed!"
            else:
                return "Need tomato seeds to plant"

        # State: PLANTED -> Can wait for growth or harvest
        elif self.state == BlockState.PLANTED:
            if self.growth_timer <= 0.0:
                # Ready to harvest
                return self.harvest(interactor)
            else:
                return f"Growing... {self.growth_timer:.1f}s remaining"

        return "Cannot interact with this block"

    def plant_seed(self, seed_item: Item, player) -> None:
        """Plant a seed on this farmland."""
        self.state = BlockState.PLANTED
        self.planted_item_type = seed_item.type
        self.growth_timer = self.growth_duration
        
        # Remove seed from player's hotbar
        player.hotbar.items[player.hotbar.selected_slot].stack_size -= 1
        if player.hotbar.items[player.hotbar.selected_slot].stack_size <= 0:
            player.hotbar.items[player.hotbar.selected_slot] = None

    def harvest(self, player) -> str:
        """Harvest the crop and give player the produce."""
        if self.planted_item_type == ItemType.TOMATO_SEED:
            # Give tomato + 2 seeds as harvest
            harvest_item = Item(ItemType.TOMATO, 1)
            harvest_seeds = Item(ItemType.TOMATO_SEED, 2)
            
            if player.add_item(harvest_item) and player.add_item(harvest_seeds):
                self.uses_remaining -= 1
                
                # Check if this block has been used 3 times
                if self.uses_remaining <= 0:
                    # Return to dirt
                    self.state = BlockState.DIRT
                    self.planted_item_type = None
                    self.uses_remaining = 3
                    return "Harvested tomato + 2 seeds! Block returned to dirt."
                else:
                    # Return to farmland for replanting
                    self.state = BlockState.FARMLAND
                    self.planted_item_type = None
                    return f"Harvested tomato + 2 seeds! Block ready to replant. ({self.uses_remaining} uses left)"
            else:
                return "Inventory full!"

        return "Cannot harvest this crop"

    def get_interaction_prompt(self) -> str:
        """Return interaction prompt text."""
        if self.state == BlockState.DIRT:
            return "Press E to till (needs hoe)"
        elif self.state == BlockState.FARMLAND:
            return "Press E to plant"
        elif self.state == BlockState.PLANTED:
            return "Press E to check growth"
        return "Press E to interact"

    def update(self, delta_time: float) -> None:
        """Update block state (countdown growth timer)."""
        if self.state == BlockState.PLANTED and self.growth_timer > 0.0:
            self.growth_timer -= delta_time
            if self.growth_timer < 0.0:
                self.growth_timer = 0.0

    def draw(self) -> None:
        """Draw the dirt block with appropriate texture."""
        # Determine texture based on state
        if self.state == BlockState.DIRT:
            texture_path = "assets/dirt.png"
        elif self.state == BlockState.FARMLAND:
            texture_path = "assets/farmland.png"
        elif self.state == BlockState.PLANTED:
            # Use crop texture on top
            if self.planted_item_type:
                texture_path = f"assets/{self.planted_item_type.value}.png"
            else:
                texture_path = "assets/farmland.png"
        else:
            texture_path = "assets/dirt.png"

        texture_id = TextureCache.get_texture(texture_path)

        # Draw cube with texture
        size_x = self.size[0] / 2
        size_y = self.size[1] / 2
        size_z = self.size[2] / 2

        glColor3f(1.0, 1.0, 1.0)

        if texture_id:
            glBindTexture(GL_TEXTURE_2D, texture_id)

            glBegin(GL_QUADS)

            # Front face
            glTexCoord2f(0, 0)
            glVertex3f(-size_x, -size_y, size_z)
            glTexCoord2f(1, 0)
            glVertex3f(size_x, -size_y, size_z)
            glTexCoord2f(1, 1)
            glVertex3f(size_x, size_y, size_z)
            glTexCoord2f(0, 1)
            glVertex3f(-size_x, size_y, size_z)

            # Back face
            glTexCoord2f(1, 0)
            glVertex3f(-size_x, -size_y, -size_z)
            glTexCoord2f(1, 1)
            glVertex3f(-size_x, size_y, -size_z)
            glTexCoord2f(0, 1)
            glVertex3f(size_x, size_y, -size_z)
            glTexCoord2f(0, 0)
            glVertex3f(size_x, -size_y, -size_z)

            # Top face (for planted state, use crop texture)
            if self.state == BlockState.PLANTED and self.planted_item_type:
                glEnd()
                glBindTexture(GL_TEXTURE_2D, 0)
                
                # Draw crop texture on top
                crop_texture_path = f"assets/{self.planted_item_type.value}.png"
                crop_texture_id = TextureCache.get_texture(crop_texture_path)
                if crop_texture_id:
                    glBindTexture(GL_TEXTURE_2D, crop_texture_id)
                
                glBegin(GL_QUADS)
                glTexCoord2f(0, 0)
                glVertex3f(-size_x, size_y, -size_z)
                glTexCoord2f(1, 0)
                glVertex3f(size_x, size_y, -size_z)
                glTexCoord2f(1, 1)
                glVertex3f(size_x, size_y, size_z)
                glTexCoord2f(0, 1)
                glVertex3f(-size_x, size_y, size_z)
                glEnd()
                
                glBindTexture(GL_TEXTURE_2D, 0)
                glBegin(GL_QUADS)
            else:
                # Regular farmland/dirt top
                glTexCoord2f(0, 1)
                glVertex3f(-size_x, size_y, -size_z)
                glTexCoord2f(1, 1)
                glVertex3f(size_x, size_y, -size_z)
                glTexCoord2f(1, 0)
                glVertex3f(size_x, size_y, size_z)
                glTexCoord2f(0, 0)
                glVertex3f(-size_x, size_y, size_z)

            # Bottom face
            glTexCoord2f(1, 1)
            glVertex3f(-size_x, -size_y, -size_z)
            glTexCoord2f(0, 1)
            glVertex3f(size_x, -size_y, -size_z)
            glTexCoord2f(0, 0)
            glVertex3f(size_x, -size_y, size_z)
            glTexCoord2f(1, 0)
            glVertex3f(-size_x, -size_y, size_z)

            # Left face
            glTexCoord2f(1, 0)
            glVertex3f(-size_x, -size_y, -size_z)
            glTexCoord2f(1, 1)
            glVertex3f(-size_x, size_y, -size_z)
            glTexCoord2f(0, 1)
            glVertex3f(-size_x, size_y, size_z)
            glTexCoord2f(0, 0)
            glVertex3f(-size_x, -size_y, size_z)

            # Right face
            glTexCoord2f(0, 0)
            glVertex3f(size_x, -size_y, -size_z)
            glTexCoord2f(1, 0)
            glVertex3f(size_x, -size_y, size_z)
            glTexCoord2f(1, 1)
            glVertex3f(size_x, size_y, size_z)
            glTexCoord2f(0, 1)
            glVertex3f(size_x, size_y, -size_z)

            glEnd()
            glBindTexture(GL_TEXTURE_2D, 0)
        else:
            # Fallback color rendering if texture not available
            color = (0.6, 0.4, 0.2) if self.state == BlockState.DIRT else (0.5, 0.3, 0.1)
            glColor3f(*color)
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
