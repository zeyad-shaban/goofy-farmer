from OpenGL.GL import *
from .base_classes import GameObject
from modules.base_classes import BoundingBox, Collidable


class Table(Collidable):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position)
        self.top_width = 2.0
        self.top_depth = 1.0
        self.top_height = 0.1
        self.table_height = 1.0

    def draw(self):
        # Table top
        glColor3f(0.6, 0.4, 0.2)  # Wood color
        glBegin(GL_QUADS)
        top_width = self.top_width
        top_depth = self.top_depth
        top_height = self.top_height
        table_height = self.table_height

        # Table top
        glVertex3f(-top_width, table_height, -top_depth)
        glVertex3f(top_width, table_height, -top_depth)
        glVertex3f(top_width, table_height, top_depth)
        glVertex3f(-top_width, table_height, top_depth)
        glEnd()

        # Table legs (4 legs)
        leg_width = 0.1
        glBegin(GL_QUADS)

        # Front left leg
        glVertex3f(-top_width + 0.1, 0, -top_depth + 0.1)
        glVertex3f(-top_width + 0.1 + leg_width, 0, -top_depth + 0.1)
        glVertex3f(-top_width + 0.1 + leg_width, table_height, -top_depth + 0.1)
        glVertex3f(-top_width + 0.1, table_height, -top_depth + 0.1)

        # Front right leg
        glVertex3f(top_width - 0.1 - leg_width, 0, -top_depth + 0.1)
        glVertex3f(top_width - 0.1, 0, -top_depth + 0.1)
        glVertex3f(top_width - 0.1, table_height, -top_depth + 0.1)
        glVertex3f(top_width - 0.1 - leg_width, table_height, -top_depth + 0.1)

        # Back left leg
        glVertex3f(-top_width + 0.1, 0, top_depth - 0.1 - leg_width)
        glVertex3f(-top_width + 0.1 + leg_width, 0, top_depth - 0.1 - leg_width)
        glVertex3f(-top_width + 0.1 + leg_width, table_height, top_depth - 0.1 - leg_width)
        glVertex3f(-top_width + 0.1, table_height, top_depth - 0.1 - leg_width)

        # Back right leg
        glVertex3f(top_width - 0.1 - leg_width, 0, top_depth - 0.1 - leg_width)
        glVertex3f(top_width - 0.1, 0, top_depth - 0.1 - leg_width)
        glVertex3f(top_width - 0.1, table_height, top_depth - 0.1 - leg_width)
        glVertex3f(top_width - 0.1 - leg_width, table_height, top_depth - 0.1 - leg_width)
        glEnd()

    def get_collision_box(self) -> BoundingBox:
        # fmt: off
        return BoundingBox(
            -self.top_width, self.top_width,
            0, self.table_height + self.top_height,
            -self.top_depth, self.top_depth,
        )
        # fmt: on
