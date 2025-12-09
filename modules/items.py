from enum import Enum
from typing import Optional, Tuple


class ItemType(Enum):
    TOMATO_SEED = "tomato_seed"
    BURGER = "burger"
    HOE = "hoe"


class Item:
    def __init__(self, item_type: ItemType, stack_size: int = 1):
        self.type = item_type
        self.stack_size = stack_size
        self.max_stack = 64

    def get_color(self) -> Tuple[float, float, float]:
        """Return color for rendering in inventory slots (fallback if no texture)."""
        colors = {
            ItemType.TOMATO_SEED: (0.8, 0.2, 0.2),  # Red
            ItemType.BURGER: (0.8, 0.6, 0.2),  # Yellow-brown
            ItemType.HOE: (0, 0, 0), # Black
        }
        return colors.get(self.type, (0.5, 0.5, 0.5))

    def get_name(self) -> str:
        """Return display name."""
        names = {
            ItemType.TOMATO_SEED: "Tomato Seed",
            ItemType.BURGER: "Burger",
            ItemType.HOE: "Hoe",
        }
        return names.get(self.type, "Unknown")

    def get_texture_path(self) -> Optional[str]:
        """Return path to texture image for this item."""
        texture_paths = {
            ItemType.TOMATO_SEED: "assets/tomato_seed.png",
            ItemType.BURGER: "assets/burger.png",
            ItemType.HOE: "assets/hoe.png",
        }
        return texture_paths.get(self.type, None)
