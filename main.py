from game.game_world import GameWorld
from modules.player import Player
from modules.crate import Crate
from modules.hoe import Hoe
from modules.table import Table
import math
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from utils.load_texture import pls_load_texture
from OpenGL.GL import glBegin, glEnd, glVertex3f, glColor3f, GL_QUADS, glTexCoord2f


camera_zoom_z = 10.0  # Starting camera distance
MIN_ZOOM_Z = 3.0  # Closest zoom allowed
MAX_ZOOM_Z = 20.0  # Furthest zoom allowed

debug_mode = True


def draw_ground():
    """Draw ground plane with grass texture."""
    glBindTexture(GL_TEXTURE_2D, grass_texture_id)
    glColor3f(1.0, 1.0, 1.0)

    size = 50.0
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0)
    glVertex3f(-size, -0.01, size)

    glTexCoord2f(0, 5)
    glVertex3f(-size, -0.01, -size)

    glTexCoord2f(5, 5)
    glVertex3f(size, -0.01, -size)

    glTexCoord2f(5, 0)
    glVertex3f(size, -0.01, size)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)


pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Game with Interactions + Zoom")

# OpenGL setup
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, display[0] / display[1], 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)

# Load texture
grass_texture_id = pls_load_texture("assets/grass_background.webp")

world = GameWorld()

player = Player(position=(0, 0, 0))
world.add_object(player)

world.add_object(Crate(position=(5, 0, 0), size=(0.5, 0.5, 0.5)))
world.add_object(Crate(position=(-5, 0, 0), size=(0.5, 0.5, 0.5)))
world.add_object(Crate(position=(0, 0, 5), size=(0.5, 0.5, 0.5)))
world.add_object(Crate(position=(3, 0, -3), size=(0.5, 0.5, 0.5)))
world.add_object(Table(position=(8, 0, 0), size=(0.7, 0.7, 0.7)))
world.add_object(Hoe(position=(8, 0.8, 0), size=(0.7, 0.7, 0.7)))

# main
clock = pygame.time.Clock()
running = True

while running:
    delta_time = clock.tick(60) / 1000.0

    # --- SINGLE EVENT LOOP START ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Game Controls
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_e:
                world.handle_player_interaction()
            elif event.key == pygame.K_TAB:
                world.inventory.toggle()

            # Hotbar Selection (1-5)
            elif event.key == pygame.K_1:
                world.hotbar.select_slot(0)
            elif event.key == pygame.K_2:
                world.hotbar.select_slot(1)
            elif event.key == pygame.K_3:
                world.hotbar.select_slot(2)
            elif event.key == pygame.K_4:
                world.hotbar.select_slot(3)
            elif event.key == pygame.K_5:
                world.hotbar.select_slot(4)

        # Hotbar Scroll
        elif event.type == pygame.MOUSEWHEEL and not (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
            world.hotbar.scroll(-event.y)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                zoom_step = 1.0
                if event.button == 4:  # Scroll Up
                    camera_zoom_z -= zoom_step
                elif event.button == 5:  # Scroll Down
                    camera_zoom_z += zoom_step

            camera_zoom_z = max(MIN_ZOOM_Z, min(MAX_ZOOM_Z, camera_zoom_z))

    keys = pygame.key.get_pressed()
    direction = [0.0, 0.0, 0.0]

    if keys[pygame.K_w]:
        direction[2] -= 1
    if keys[pygame.K_s]:
        direction[2] += 1
    if keys[pygame.K_a]:
        direction[0] -= 1
    if keys[pygame.K_d]:
        direction[0] += 1

    if direction != [0, 0, 0]:
        length = math.sqrt(direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2)
        direction = [d / length for d in direction]

    player.move(tuple(direction), delta_time, world.get_collidables())

    # Update world
    world.update(delta_time)

    # Camera to follow player
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # fmt: off
    gluLookAt(
        player.position[0], player.position[1] + 8, player.position[2] + camera_zoom_z,
        player.position[0], player.position[1] + 1, player.position[2],
        0, 1, 0,
    )
    # fmt: on


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_ground()

    # Draw player
    glPushMatrix()
    glTranslatef(*player.position)
    glTranslatef(0, 1, 0)
    glScalef(0.2, 0.2, 0.2)
    player.draw()
    glPopMatrix()

    # Draw objects
    for obj in world.objects:
        if obj is not player:
            glPushMatrix()
            glTranslatef(*obj.position)
            glScalef(*obj.size)
            obj.draw()
            glPopMatrix()

    # Debug collisions
    if debug_mode:
        world.draw_collisions()

    # UI
    world.dialogue_box.draw(*display)
    world.hotbar.draw(*display)
    world.inventory.draw(*display)

    pygame.display.flip()

pygame.quit()
