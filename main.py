from game.game_world import GameWorld
from modules.player import Player
from modules.crate import Crate
import math
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from utils.load_texture import pls_load_texture


camera_zoom_z = 10.0   # Starting camera distance
MIN_ZOOM_Z = 3.0       # Closest zoom allowed
MAX_ZOOM_Z = 20.0      # Furthest zoom allowed

debug_mode = True



def draw_ground():
    """Draw ground plane with grass texture."""
    from OpenGL.GL import glBegin, glEnd, glVertex3f, glColor3f, GL_QUADS, glTexCoord2f

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

world.add_object(Crate(position=(5, 0, 0)))
world.add_object(Crate(position=(-5, 0, 0)))
world.add_object(Crate(position=(0, 0, 5)))
world.add_object(Crate(position=(3, 0, -3)))


#main

clock = pygame.time.Clock()
running = True

while running:
    delta_time = clock.tick(60) / 1000.0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_e:
                world.handle_player_interaction()

        # Mouse scroll zoom
        elif event.type == pygame.MOUSEBUTTONDOWN:
            zoom_step = 1.0
            if event.button == 4:
                camera_zoom_z -= zoom_step
            elif event.button == 5:
                camera_zoom_z += zoom_step

            camera_zoom_z = max(MIN_ZOOM_Z, min(MAX_ZOOM_Z, camera_zoom_z))

    # Movement keys
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
    gluLookAt(
        player.position[0], 5, player.position[2] + camera_zoom_z,  # camera position
        player.position[0], player.position[1], player.position[2],  # target (player)
        0, 1, 0                                                     # up vector
    )


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
            obj.draw()
            glPopMatrix()

    # Debug collisions
    if debug_mode:
        world.draw_collisions()

    # UI
    world.dialogue_box.draw(*display)

    pygame.display.flip()

pygame.quit()
