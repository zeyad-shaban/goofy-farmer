from game.game_world import GameWorld
from modules import Table, Chest, Hoe, Crate, Player, Item, ItemType, DirtBlock, SellingPoint
import math
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluOrtho2D
from utils.load_texture import pls_load_texture
from utils.texture_cache import TextureCache
from OpenGL.GL import glBegin, glEnd, glVertex3f, glColor3f, GL_QUADS, glTexCoord2f


camera_zoom_z = 10.0
MIN_ZOOM_Z = 3.0
MAX_ZOOM_Z = 20.0

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


def draw_coins_ui(window_width: int, window_height: int, coins: float):
    """Draw coins display in top-right corner."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    coin_size = 30
    padding = 10
    pos_x = window_width - coin_size - padding
    pos_y = window_height - coin_size - padding

    # Draw coin texture
    coin_texture_id = TextureCache.get_texture("assets/coin.png")
    if coin_texture_id:
        glBindTexture(GL_TEXTURE_2D, coin_texture_id)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(pos_x, pos_y)
        glTexCoord2f(1, 0)
        glVertex2f(pos_x + coin_size, pos_y)
        glTexCoord2f(1, 1)
        glVertex2f(pos_x + coin_size, pos_y + coin_size)
        glTexCoord2f(0, 1)
        glVertex2f(pos_x, pos_y + coin_size)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

    # Draw coin amount text
    font = pygame.font.Font(None, 24)
    text_surface = font.render(f"${coins:.1f}", True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    text_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, text_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    text_x = pos_x - text_surface.get_width() - 10
    text_y = pos_y + (coin_size - text_surface.get_height()) / 2

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(text_x, text_y)
    glTexCoord2f(1, 0)
    glVertex2f(text_x + text_surface.get_width(), text_y)
    glTexCoord2f(1, 1)
    glVertex2f(text_x + text_surface.get_width(), text_y + text_surface.get_height())
    glTexCoord2f(0, 1)
    glVertex2f(text_x, text_y + text_surface.get_height())
    glEnd()

    glDeleteTextures([text_id])
    glBindTexture(GL_TEXTURE_2D, 0)

    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


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

# Give player starting items (debug only)
if debug_mode:
    player.hotbar.items[0] = Item(ItemType.HOE, 1)
    player.inventory.add_item(Item(ItemType.TOMATO_SEED, 2))
    player.inventory.add_item(Item(ItemType.TOMATO, 1))

world.add_object(Crate(position=(5, 0, 0), size=(0.5, 0.5, 0.5)))
world.add_object(Crate(position=(-5, 0, 0), size=(0.5, 0.5, 0.5)))
world.add_object(Crate(position=(0, 0, 5), size=(0.5, 0.5, 0.5)))
world.add_object(Crate(position=(3, 0, -3), size=(0.5, 0.5, 0.5)))
world.add_object(Table(position=(8, 0, 0), size=(0.7, 0.7, 0.7)))
world.add_object(Hoe(position=(8, 0.8, 0), size=(0.7, 0.7, 0.7)))

# Add dirt blocks for farming
world.add_object(DirtBlock(position=(-3, 0, 3), size=(1.0, 1.0, 1.0)))
world.add_object(DirtBlock(position=(-2, 0, 3), size=(1.0, 1.0, 1.0)))
world.add_object(DirtBlock(position=(-1, 0, 3), size=(1.0, 1.0, 1.0)))

# Add selling point
world.add_object(SellingPoint(position=(0, 0, -5), size=(1.5, 1.5, 1.5)))

chest = Chest(position=(10, 0, 0))
world.add_object(chest)
chest.inventory.add_item(Item(ItemType.TOMATO_SEED, 5))
chest.inventory.add_item(Item(ItemType.BURGER, 3))

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
                if world.opened_chest:
                    world.close_chest()
                    world.player.inventory.is_open = False
                else:
                    if world.player.inventory.is_open:
                        world.inventory.is_open = False
                    else:
                        running = False

            elif event.key == pygame.K_e:
                # Check if clicking on chest
                if world.player:
                    interactable = world.player.find_interactable(world.objects)
                    if isinstance(interactable, Chest):
                        if world.opened_chest == interactable:
                            world.close_chest()
                        else:
                            world.open_chest(interactable)
                    else:
                        world.handle_player_interaction()

            elif event.key == pygame.K_TAB:
                # Close chest if open, otherwise toggle inventory
                if world.opened_chest:
                    world.close_chest()
                    world.player.inventory.is_open = False
                else:
                    world.player.inventory.is_open = not world.player.inventory.is_open

            # Hotbar Selection (1-5)
            elif event.key == pygame.K_1:
                world.player.hotbar.select_slot(0)
            elif event.key == pygame.K_2:
                world.player.hotbar.select_slot(1)
            elif event.key == pygame.K_3:
                world.player.hotbar.select_slot(2)
            elif event.key == pygame.K_4:
                world.player.hotbar.select_slot(3)
            elif event.key == pygame.K_5:
                world.player.hotbar.select_slot(4)

        # Hotbar Scroll
        elif event.type == pygame.MOUSEWHEEL and not (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
            world.player.hotbar.scroll(-event.y)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if world.opened_chest:
                world.handle_inventory_click(event.pos[0], event.pos[1], *display)
            elif world.player.inventory.is_open:
                world.handle_inventory_click(event.pos[0], event.pos[1], *display)

            else:
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
    world.player.hotbar.draw(*display)
    draw_coins_ui(*display, world.player.coins)

    # paleyr inventory
    if world.player.inventory.is_open and not world.opened_chest:
        world.player.inventory.draw(*display, "Inventory", 100)

    # both inventories
    if world.opened_chest:
        world.opened_chest.inventory.draw(*display, "Chest", display[1] // 2)

        if world.player:
            world.player.inventory.draw(*display, "Inventory", 100)

    pygame.display.flip()

pygame.quit()
