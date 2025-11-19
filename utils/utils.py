from OpenGL.GL import *
from OpenGL.GLU import *
from modules.base_classes import BoundingBox
import math

def draw_collision_box(bbox: BoundingBox, color: tuple = (1.0, 0.0, 0.0, 0.3)):
    """
    Draw a wireframe box representing a collision box for debugging.
    
    Args:
        bbox: BoundingBox to draw
        color: RGBA color tuple (default: semi-transparent red)
    """
    from OpenGL.GL import glBegin, glEnd, glVertex3f, glColor4f, glEnable, glDisable, GL_BLEND, GL_LINES, glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
    
    # Enable transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glColor4f(*color)
    
    # Draw wireframe box
    glBegin(GL_LINES)
    
    # Bottom face
    glVertex3f(bbox.min_x, bbox.min_y, bbox.min_z)
    glVertex3f(bbox.max_x, bbox.min_y, bbox.min_z)
    
    glVertex3f(bbox.max_x, bbox.min_y, bbox.min_z)
    glVertex3f(bbox.max_x, bbox.min_y, bbox.max_z)
    
    glVertex3f(bbox.max_x, bbox.min_y, bbox.max_z)
    glVertex3f(bbox.min_x, bbox.min_y, bbox.max_z)
    
    glVertex3f(bbox.min_x, bbox.min_y, bbox.max_z)
    glVertex3f(bbox.min_x, bbox.min_y, bbox.min_z)
    
    # Top face
    glVertex3f(bbox.min_x, bbox.max_y, bbox.min_z)
    glVertex3f(bbox.max_x, bbox.max_y, bbox.min_z)
    
    glVertex3f(bbox.max_x, bbox.max_y, bbox.min_z)
    glVertex3f(bbox.max_x, bbox.max_y, bbox.max_z)
    
    glVertex3f(bbox.max_x, bbox.max_y, bbox.max_z)
    glVertex3f(bbox.min_x, bbox.max_y, bbox.max_z)
    
    glVertex3f(bbox.min_x, bbox.max_y, bbox.max_z)
    glVertex3f(bbox.min_x, bbox.max_y, bbox.min_z)
    
    # Vertical edges
    glVertex3f(bbox.min_x, bbox.min_y, bbox.min_z)
    glVertex3f(bbox.min_x, bbox.max_y, bbox.min_z)
    
    glVertex3f(bbox.max_x, bbox.min_y, bbox.min_z)
    glVertex3f(bbox.max_x, bbox.max_y, bbox.min_z)
    
    glVertex3f(bbox.max_x, bbox.min_y, bbox.max_z)
    glVertex3f(bbox.max_x, bbox.max_y, bbox.max_z)
    
    glVertex3f(bbox.min_x, bbox.min_y, bbox.max_z)
    glVertex3f(bbox.min_x, bbox.max_y, bbox.max_z)
    
    glEnd()
    
    glDisable(GL_BLEND)
