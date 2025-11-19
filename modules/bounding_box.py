from abc import ABC, abstractmethod
from dataclasses import dataclass
import math

from base_classes import Vec2, Vec3

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
        return (self.min_x <= other.max_x and self.max_x >= other.min_x and
                self.min_y <= other.max_y and self.max_y >= other.min_y and
                self.min_z <= other.max_z and self.max_z >= other.min_z)
    
    def translate(self, position: Vec3) -> "BoundingBox":
        """Return a new bounding box translated by position."""
        return BoundingBox(
            self.min_x + position[0], self.max_x + position[0],
            self.min_y + position[1], self.max_y + position[1],
            self.min_z + position[2], self.max_z + position[2],
        )
