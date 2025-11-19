from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Optional, List
from .base_classes import Vec3, Collidable, Interactable, GameObject, BoundingBox
import math


class Player(Collidable):
    """Player character with movement and interaction capabilities."""

    def __init__(self, position: Vec3 = (0.0, 0.0, 0.0)):
        super().__init__(position)
        self.velocity: Vec3 = (0.0, 0.0, 0.0)
        self.speed: float = 5.0
        self.interaction_range: float = 3.0

    def draw(self) -> None:
        # --- Head (cube) ---
        # head bounds
        hx0, hx1 = -1.0, 1.0
        hy0, hy1 = 0.0, 1.0
        hz0, hz1 = -1.0, 1.0

        # skin color
        glColor3f(1.0, 0.85, 0.7)
        glBegin(GL_QUADS)
        # front (z = hz1)
        glVertex3f(hx0, hy0, hz1)
        glVertex3f(hx1, hy0, hz1)
        glVertex3f(hx1, hy1, hz1)
        glVertex3f(hx0, hy1, hz1)
        # back (z = hz0)
        glVertex3f(hx1, hy0, hz0)
        glVertex3f(hx0, hy0, hz0)
        glVertex3f(hx0, hy1, hz0)
        glVertex3f(hx1, hy1, hz0)
        # left (x = hx0)
        glVertex3f(hx0, hy0, hz0)
        glVertex3f(hx0, hy0, hz1)
        glVertex3f(hx0, hy1, hz1)
        glVertex3f(hx0, hy1, hz0)
        # right (x = hx1)
        glVertex3f(hx1, hy0, hz1)
        glVertex3f(hx1, hy0, hz0)
        glVertex3f(hx1, hy1, hz0)
        glVertex3f(hx1, hy1, hz1)
        # top
        glVertex3f(hx0, hy1, hz1)
        glVertex3f(hx1, hy1, hz1)
        glVertex3f(hx1, hy1, hz0)
        glVertex3f(hx0, hy1, hz0)
        # bottom (neck area)
        glVertex3f(hx0, hy0, hz0)
        glVertex3f(hx1, hy0, hz0)
        glVertex3f(hx1, hy0, hz1)
        glVertex3f(hx0, hy0, hz1)
        glEnd()

        # --- Eyes (on front face, slightly in front to avoid z-fighting) ---
        # white eye plates
        eye_z = hz1 + 0.01
        # left white
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glVertex3f(-0.5, 0.65, eye_z)
        glVertex3f(-0.15, 0.65, eye_z)
        glVertex3f(-0.15, 0.9, eye_z)
        glVertex3f(-0.5, 0.9, eye_z)
        glEnd()
        # right white
        glBegin(GL_QUADS)
        glVertex3f(0.15, 0.65, eye_z)
        glVertex3f(0.5, 0.65, eye_z)
        glVertex3f(0.5, 0.9, eye_z)
        glVertex3f(0.15, 0.9, eye_z)
        glEnd()

        # black pupils (big & cute)
        pupil_z = hz1 + 0.02
        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        # left pupil
        glVertex3f(-0.43, 0.69, pupil_z)
        glVertex3f(-0.22, 0.69, pupil_z)
        glVertex3f(-0.22, 0.86, pupil_z)
        glVertex3f(-0.43, 0.86, pupil_z)
        # right pupil
        glVertex3f(0.22, 0.69, pupil_z)
        glVertex3f(0.43, 0.69, pupil_z)
        glVertex3f(0.43, 0.86, pupil_z)
        glVertex3f(0.22, 0.86, pupil_z)
        glEnd()

        # small mouth
        mouth_z = hz1 + 0.02
        glColor3f(0.6, 0.15, 0.15)
        glBegin(GL_QUADS)
        glVertex3f(-0.25, 0.35, mouth_z)
        glVertex3f(0.25, 0.35, mouth_z)
        glVertex3f(0.25, 0.45, mouth_z)
        glVertex3f(-0.25, 0.45, mouth_z)
        glEnd()

        # --- Body (shirt) ---
        bx0, bx1 = -1.2, 1.2
        by0, by1 = -1.5, 0.0
        bz0, bz1 = -0.6, 0.6
        # shirt color (Steve-ish blue)
        glColor3f(0.2, 0.45, 0.85)
        glBegin(GL_QUADS)
        # front
        glVertex3f(bx0, by0, bz1)
        glVertex3f(bx1, by0, bz1)
        glVertex3f(bx1, by1, bz1)
        glVertex3f(bx0, by1, bz1)
        # back
        glVertex3f(bx1, by0, bz0)
        glVertex3f(bx0, by0, bz0)
        glVertex3f(bx0, by1, bz0)
        glVertex3f(bx1, by1, bz0)
        # left
        glVertex3f(bx0, by0, bz0)
        glVertex3f(bx0, by0, bz1)
        glVertex3f(bx0, by1, bz1)
        glVertex3f(bx0, by1, bz0)
        # right
        glVertex3f(bx1, by0, bz1)
        glVertex3f(bx1, by0, bz0)
        glVertex3f(bx1, by1, bz0)
        glVertex3f(bx1, by1, bz1)
        # top (neck area)
        glVertex3f(bx0, by1, bz1)
        glVertex3f(bx1, by1, bz1)
        glVertex3f(bx1, by1, bz0)
        glVertex3f(bx0, by1, bz0)
        # bottom
        glVertex3f(bx0, by0, bz0)
        glVertex3f(bx1, by0, bz0)
        glVertex3f(bx1, by0, bz1)
        glVertex3f(bx0, by0, bz1)
        glEnd()

        # --- Arms (sleeves) ---
        ax_in, ax_out = -1.2, -1.6
        # left arm
        glColor3f(0.2, 0.45, 0.85)
        glBegin(GL_QUADS)
        # front
        glVertex3f(ax_out, -0.5, bz1)
        glVertex3f(ax_in, -0.5, bz1)
        glVertex3f(ax_in, 0.2, bz1)
        glVertex3f(ax_out, 0.2, bz1)
        # back
        glVertex3f(ax_in, -0.5, bz0)
        glVertex3f(ax_out, -0.5, bz0)
        glVertex3f(ax_out, 0.2, bz0)
        glVertex3f(ax_in, 0.2, bz0)
        # top
        glVertex3f(ax_out, 0.2, bz1)
        glVertex3f(ax_in, 0.2, bz1)
        glVertex3f(ax_in, 0.2, bz0)
        glVertex3f(ax_out, 0.2, bz0)
        # bottom
        glVertex3f(ax_out, -0.5, bz0)
        glVertex3f(ax_in, -0.5, bz0)
        glVertex3f(ax_in, -0.5, bz1)
        glVertex3f(ax_out, -0.5, bz1)
        glEnd()

        # right arm (mirror)
        ax_in_r, ax_out_r = 1.2, 1.6
        glColor3f(0.2, 0.45, 0.85)
        glBegin(GL_QUADS)
        glVertex3f(ax_in_r, -0.5, bz1)
        glVertex3f(ax_out_r, -0.5, bz1)
        glVertex3f(ax_out_r, 0.2, bz1)
        glVertex3f(ax_in_r, 0.2, bz1)

        glVertex3f(ax_out_r, -0.5, bz0)
        glVertex3f(ax_in_r, -0.5, bz0)
        glVertex3f(ax_in_r, 0.2, bz0)
        glVertex3f(ax_out_r, 0.2, bz0)

        glVertex3f(ax_in_r, 0.2, bz1)
        glVertex3f(ax_out_r, 0.2, bz1)
        glVertex3f(ax_out_r, 0.2, bz0)
        glVertex3f(ax_in_r, 0.2, bz0)

        glVertex3f(ax_in_r, -0.5, bz0)
        glVertex3f(ax_out_r, -0.5, bz0)
        glVertex3f(ax_out_r, -0.5, bz1)
        glVertex3f(ax_in_r, -0.5, bz1)
        glEnd()

        # --- Legs (pants) ---
        # left leg
        lx0, lx1 = -0.6, -0.1
        ly0, ly1 = -3.0, -1.5
        lz0, lz1 = -0.5, 0.5
        glColor3f(0.08, 0.2, 0.6)  # dark blue pants
        glBegin(GL_QUADS)
        # front
        glVertex3f(lx0, ly0, lz1)
        glVertex3f(lx1, ly0, lz1)
        glVertex3f(lx1, ly1, lz1)
        glVertex3f(lx0, ly1, lz1)
        # back
        glVertex3f(lx1, ly0, lz0)
        glVertex3f(lx0, ly0, lz0)
        glVertex3f(lx0, ly1, lz0)
        glVertex3f(lx1, ly1, lz0)
        # left
        glVertex3f(lx0, ly0, lz0)
        glVertex3f(lx0, ly0, lz1)
        glVertex3f(lx0, ly1, lz1)
        glVertex3f(lx0, ly1, lz0)
        # right
        glVertex3f(lx1, ly0, lz1)
        glVertex3f(lx1, ly0, lz0)
        glVertex3f(lx1, ly1, lz0)
        glVertex3f(lx1, ly1, lz1)
        # top
        glVertex3f(lx0, ly1, lz1)
        glVertex3f(lx1, ly1, lz1)
        glVertex3f(lx1, ly1, lz0)
        glVertex3f(lx0, ly1, lz0)
        # bottom
        glVertex3f(lx0, ly0, lz0)
        glVertex3f(lx1, ly0, lz0)
        glVertex3f(lx1, ly0, lz1)
        glVertex3f(lx0, ly0, lz1)
        glEnd()

        # right leg
        rx0, rx1 = 0.1, 0.6
        glColor3f(0.08, 0.2, 0.6)
        glBegin(GL_QUADS)
        glVertex3f(rx0, ly0, lz1)
        glVertex3f(rx1, ly0, lz1)
        glVertex3f(rx1, ly1, lz1)
        glVertex3f(rx0, ly1, lz1)

        glVertex3f(rx1, ly0, lz0)
        glVertex3f(rx0, ly0, lz0)
        glVertex3f(rx0, ly1, lz0)
        glVertex3f(rx1, ly1, lz0)

        glVertex3f(rx0, ly0, lz0)
        glVertex3f(rx0, ly0, lz1)
        glVertex3f(rx0, ly1, lz1)
        glVertex3f(rx0, ly1, lz0)

        glVertex3f(rx1, ly0, lz1)
        glVertex3f(rx1, ly0, lz0)
        glVertex3f(rx1, ly1, lz0)
        glVertex3f(rx1, ly1, lz1)

        glVertex3f(rx0, ly1, lz1)
        glVertex3f(rx1, ly1, lz1)
        glVertex3f(rx1, ly1, lz0)
        glVertex3f(rx0, ly1, lz0)

        glVertex3f(rx0, ly0, lz0)
        glVertex3f(rx1, ly0, lz0)
        glVertex3f(rx1, ly0, lz1)
        glVertex3f(rx0, ly0, lz1)
        glEnd()

    def get_collision_box(self) -> BoundingBox:
        """Player's collision box (approximate body bounds)."""
        return BoundingBox(-1.2, 1.2, -3.0, 1.0, -0.6, 0.6)

    def move(self, direction: Vec3, delta_time: float, collidables: List[Collidable]) -> None:
        """
        Move player in given direction, checking for collisions.
        direction: normalized direction vector (x, y, z)
        """
        if direction == (0, 0, 0):
            self.velocity = (0.0, 0.0, 0.0)
            return

        # Calculate new position
        move_delta = (
            direction[0] * self.speed * delta_time,
            direction[1] * self.speed * delta_time,
            direction[2] * self.speed * delta_time,
        )

        new_position = (
            self.position[0] + move_delta[0],
            self.position[1] + move_delta[1],
            self.position[2] + move_delta[2],
        )

        # Check collision at new position
        old_position = self.position
        self.position = new_position

        collision_detected = False
        for obj in collidables:
            if obj is not self and self.collides_with(obj):
                collision_detected = True
                break

        if collision_detected:
            # Revert to old position if collision detected
            self.position = old_position
            self.velocity = (0.0, 0.0, 0.0)
        else:
            self.velocity = move_delta

    def is_moving(self) -> bool:
        """Check if player is currently moving."""
        return self.velocity != (0.0, 0.0, 0.0)

    def find_interactable(self, objects: List[GameObject]) -> Optional[Interactable]:
        """
        Find the nearest interactable object within range.
        Returns the object and its distance, or None if none found.
        """
        nearest: Optional[Interactable] = None
        nearest_distance = float("inf")

        for obj in objects:
            if isinstance(obj, Interactable):
                # Calculate distance
                dx = obj.position[0] - self.position[0]
                dy = obj.position[1] - self.position[1]
                dz = obj.position[2] - self.position[2]
                distance = math.sqrt(dx * dx + dy * dy + dz * dz)

                if distance <= self.interaction_range and distance < nearest_distance:
                    nearest = obj
                    nearest_distance = distance

        return nearest

    def interact_with(self, interactable: Interactable) -> str:
        """Interact with an interactable object, returns dialogue message."""
        return interactable.on_interact(self)
