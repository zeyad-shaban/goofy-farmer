from enum import Enum
from typing import Optional, Tuple


class ItemType(Enum):
    TOMATO_SEED = "tomato_seed"
    TOMATO = "tomato"
    BURGER = "burger"
    HOE = "hoe"
    COW = "cow"


class Item:
    def __init__(self, item_type: ItemType, stack_size: int = 1):
        self.type = item_type
        self.stack_size = stack_size
        self.max_stack = 64

    def get_color(self) -> Tuple[float, float, float]:
        """Return color for rendering in inventory slots (fallback if no texture)."""
        colors = {
            ItemType.TOMATO_SEED: (0.8, 0.2, 0.2),  # Red
            ItemType.TOMATO: (0.9, 0.3, 0.2),  # Dark red
            ItemType.BURGER: (0.8, 0.6, 0.2),  # Yellow-brown
            ItemType.HOE: (0, 0, 0),  # Black
            ItemType.COW: (0.6, 0.4, 0.2),  # Brown
        }
        return colors.get(self.type, (0.5, 0.5, 0.5))

    def get_name(self) -> str:
        """Return display name."""
        names = {
            ItemType.TOMATO_SEED: "Tomato Seed",
            ItemType.TOMATO: "Tomato",
            ItemType.BURGER: "Burger",
            ItemType.HOE: "Hoe",
            ItemType.COW: "Cow",
        }
        return names.get(self.type, "Unknown")

    def get_texture_path(self) -> Optional[str]:
        """Return path to texture image for this item."""
        texture_paths = {
            ItemType.TOMATO_SEED: "assets/tomato_seed.png",
            ItemType.TOMATO: "assets/tomato.png",
            ItemType.BURGER: "assets/burger.png",
            ItemType.HOE: "assets/hoe.png",
            ItemType.COW: "assets/cow.png",
        }
        return texture_paths.get(self.type, None)

    def get_price(self) -> float:
        """Return the selling price of this item."""
        prices = {
            ItemType.TOMATO_SEED: 0.5,
            ItemType.TOMATO: 5.0,
            ItemType.BURGER: 3.0,
            ItemType.HOE: 0.0,  # Can't sell tools
            ItemType.COW: 100.0,
        }
        return prices.get(self.type, 0.0)
