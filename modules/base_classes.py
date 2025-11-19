from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
from dataclasses import dataclass
import math

Vec3 = Tuple[float, float, float]
Vec2 = Tuple[float, float]


class GameObject(ABC):
    """Base class for all game objects."""
    
    def __init__(self, position: Vec3 = (0.0, 0.0, 0.0)):
        self.position: Vec3 = position
    
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
        """Return the collision box in world coordinates."""
        return self.get_collision_box().translate(self.position)
    
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