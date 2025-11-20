from OpenGL.GL import *
from OpenGL.GLU import *
from modules.base_classes import BoundingBox
import math
from game.game_world import GameWorld
from modules.player import Player
from modules.crate import Crate
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt

def pls_load_texture(filename):
    """Load an image file and convert it into an OpenGL texture."""
    try:
        # 1. Load the image using Pygame
        surface = pygame.image.load(filename)
        # Flip the image vertically because OpenGL reads images bottom-up
        surface = pygame.transform.flip(surface, False, True)

        # Convert to a string of pixel data (RGBA)
        texture_data = pygame.image.tostring(surface, "RGBA", True)

        width = surface.get_width()
        height = surface.get_height()

        # 2. Generate and bind a texture ID
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Set filtering and wrapping (tiling) parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Upload image data to the GPU
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        return texture_id

    except pygame.error as e:
        print(f"Error loading texture {filename}: {e}")
        return None
