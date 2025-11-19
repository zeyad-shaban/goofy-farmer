from game.game_world import GameWorld
from modules.player import Player
from modules.crate import Crate
import math
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt


def draw_ground():
    """Draw the ground plane."""
    from OpenGL.GL import glBegin, glEnd, glVertex3f, glColor3f, GL_QUADS

    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-50, -0.01, -50)
    glVertex3f(50, -0.01, -50)
    glVertex3f(50, -0.01, 50)
    glVertex3f(-50, -0.01, 50)
    glEnd()


# Initialize Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Game with Interactions")

# Setup OpenGL projection
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, display[0] / display[1], 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(0, 5, 10, 0, 0, 0, 0, 1, 0)  # Camera position  # Look at point  # Up direction
glEnable(GL_DEPTH_TEST)

# Create game world
world = GameWorld()

# Add player
player = Player(position=(0, 0, 0))
world.add_object(player)

# Add some crates
world.add_object(Crate(position=(5, 0, 0)))
world.add_object(Crate(position=(-5, 0, 0)))
world.add_object(Crate(position=(0, 0, 5)))
world.add_object(Crate(position=(3, 0, -3)))

# Game loop variables
clock = pygame.time.Clock()
running = True

while running:
    delta_time = clock.tick(60) / 1000.0  # Convert to seconds

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_e:
                # Player interaction
                world.handle_player_interaction()

    # Handle continuous key input (movement)
    keys = pygame.key.get_pressed()
    direction = [0.0, 0.0, 0.0]

    if keys[pygame.K_w]:
        direction[2] -= 1  # Move forward (negative Z)
    if keys[pygame.K_s]:
        direction[2] += 1  # Move backward (positive Z)
    if keys[pygame.K_a]:
        direction[0] -= 1  # Move left (negative X)
    if keys[pygame.K_d]:
        direction[0] += 1  # Move right (positive X)

    # Normalize direction if moving diagonally
    if direction != [0, 0, 0]:
        length = math.sqrt(direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2)
        direction = [d / length for d in direction]

    # Move player
    player.move(tuple(direction), delta_time, world.get_collidables())  # type: ignore

    # Update world
    world.update(delta_time)

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw ground
    draw_ground()

    # Draw player (scaled down)
    glPushMatrix()
    glTranslatef(*player.position)
    glTranslatef(0, 1, 0)  # Offset so player stands on ground
    glScalef(0.2, 0.2, 0.2)
    player.draw()
    glPopMatrix()

    # Draw other objects
    for obj in world.objects:
        if obj is not player:
            glPushMatrix()
            glTranslatef(*obj.position)
            obj.draw()
            glPopMatrix()

    # Draw UI (dialogue box)
    world.dialogue_box.draw(*display)

    # Swap buffers
    pygame.display.flip()

pygame.quit()
