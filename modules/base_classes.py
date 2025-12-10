from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING
from dataclasses import dataclass
from .items import Item  


if TYPE_CHECKING:
    from .player import Player

Vec3 = Tuple[float, float, float]
Vec2 = Tuple[float, float]


@dataclass
class BoundingBox:
    """Axis-aligned bounding box for collision detection."""

    min_x: float
    max_x: float
    min_y: float
    max_y: float
    min_z: float
    max_z: float

    def intersects(self, other: "BoundingBox") -> bool:
        """Check if this box intersects with another."""
        return self.min_x <= other.max_x and self.max_x >= other.min_x and self.min_y <= other.max_y and self.max_y >= other.min_y and self.min_z <= other.max_z and self.max_z >= other.min_z

    def translate(self, position: Vec3) -> "BoundingBox":
        """Return a new bounding box translated by position."""
        return BoundingBox(
            self.min_x + position[0],
            self.max_x + position[0],
            self.min_y + position[1],
            self.max_y + position[1],
            self.min_z + position[2],
            self.max_z + position[2],
        )


class GameObject(ABC):
    """Base class for all game objects."""

    def __init__(self, position: Vec3 = (0.0, 0.0, 0.0), size: Vec3 = (1, 1, 1)):
        self.position: Vec3 = position
        self.size: Vec3 = size

    @abstractmethod
    def draw(self) -> None:
        """Render this object."""
        pass

    def update(self, delta_time: float) -> None:
        """Update object state. Override if needed."""
        pass


class Collidable(GameObject):
    """Base class for objects that can collide."""

    @abstractmethod
    def get_collision_box(self) -> BoundingBox:
        """Return the collision box in local coordinates."""
        pass

    def get_world_collision_box(self) -> BoundingBox:
        """Return the collision box in world coordinates with scaling applied."""
        local_box = self.get_collision_box()
        scaled_box = BoundingBox(
            local_box.min_x * self.size[0],
            local_box.max_x * self.size[0],
            local_box.min_y * self.size[1],
            local_box.max_y * self.size[1],
            local_box.min_z * self.size[2],
            local_box.max_z * self.size[2],
        )
        return scaled_box.translate(self.position)

    def collides_with(self, other: "Collidable") -> bool:
        """Check if this object collides with another collidable object."""
        return self.get_world_collision_box().intersects(other.get_world_collision_box())


class Interactable(ABC):
    """Interface for objects that can be interacted with."""

    @abstractmethod
    def on_interact(self, interactor: "Player") -> str:
        """
        Called when player interacts with this object.
        Returns a message to display in dialogue.
        """
        pass

    @abstractmethod
    def get_interaction_prompt(self) -> str:
        """Return the prompt text (e.g., 'Press E to interact')."""
        pass


class Pickable(ABC):
    """Interface for objects that can be picked up by the player."""

    @abstractmethod
    def get_item_type(self) -> "ItemType": # type: ignore
        """Return the item type when picked up."""
        pass

    @staticmethod
    def try_pickup_item(pickable_obj: "Pickable", interactor: "Player") -> str:
        """Shared pickup logic for all pickable items."""
        item = Item(pickable_obj.get_item_type(), 1)  
        if interactor.add_item(item):  
            return f"Picked up {pickable_obj.get_item_type().value}!"  
        
        return "No space in inventory!"

