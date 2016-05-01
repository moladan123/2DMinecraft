import pygame
import sys
import random
from pygame.locals import *

BLACK = (0, 0, 0)
BROWN = (153, 76, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

TILESIZE = 16
MAPWIDTH = 30
MAPHEIGHT = 30

pygame.init()
screen = pygame.display.set_mode((TILESIZE * MAPWIDTH, TILESIZE * MAPHEIGHT + 50))
pygame.display.set_caption("Minecraft")

# ID for each block type
DIRT = 0
GRASS = 1
WATER = 2
COAL = 3
DIAMOND = 4

resources = [DIRT, GRASS, WATER, COAL, DIAMOND]

textures = {
    DIRT: pygame.image.load("dirt.png"),
    GRASS: pygame.image.load("grass.png"),
    WATER: pygame.image.load("water.png"),
    COAL: pygame.image.load("coal.png"),
    DIAMOND: pygame.image.load("diamond.png")
}

player = pygame.image.load("player.png")
player.set_colorkey(WHITE)
player.convert_alpha()  # Makes player background transparent
playerPos = [0, 0]
inventory_cursor = pygame.image.load("cursor.png")
inventory_cursor.set_alpha(50)
inventory_anticursor = pygame.image.load("anticursor.png")
inventory_position = [0, TILESIZE * MAPHEIGHT + 16]

font = pygame.font.Font(pygame.font.get_default_font(), 18)

inventory = {
    DIRT: 0,
    GRASS: 0,
    COAL: 0,
    WATER: 0,
    DIAMOND: 0
}


def spawn_block(tile_map, block_value, max_vein, seed_chance, spread_chance):  # Generates a single type of block
    rand = random.randint(1, 10000)
    if tile_map[row][column] == DIRT or (tile_map[row][column] == GRASS and rand < 5000):
            for i in range(max_vein):
                try:
                    if 1 <= rand <= seed_chance:
                        tile_map[row][column] = block_value
                    if tile_map[row - 1][column] == block_value or tile_map[row][column - 1] == block_value or tile_map[row + 1][column] == block_value or tile_map[row][column + 1] == block_value:
                        if 1 <= rand <= spread_chance:
                            tile_map[row][column] = block_value

                except IndexError:
                    pass
    return tile_map

tilemap = [[DIRT for i in range(MAPHEIGHT)] for j in range(MAPWIDTH)]
for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
        rand = random.randint(1, 10000)
        for i in range(random.randint(3, 4)): # The weird ordering is so that everything spawns evenly
            tilemap = spawn_block(tilemap, DIAMOND, 1, 5, 200)
            tilemap = spawn_block(tilemap, WATER, 1, 15, 3200)
            tilemap = spawn_block(tilemap, COAL, 1, 40, 1500)
            tilemap = spawn_block(tilemap, GRASS, 5, 100, 10000)


player = player.convert_alpha()
window_states = {True:"exploring", False: "crafting"}
inventory_open = False

while 1:
    if not inventory_open:
        for row in range(MAPHEIGHT):  # Display map
            for column in range(MAPWIDTH):
                screen.blit(textures[tilemap[row][column]], (column * TILESIZE, row * TILESIZE))

        # Display player
        screen.blit(player, (playerPos[0] * TILESIZE, playerPos[1] * TILESIZE))

        # Display cursor
        screen.blit(inventory_cursor, (inventory_position[0] * 80 + 8, inventory_position[1]))

        Position = 10
        for item in resources:
            screen.blit(textures[item], (Position, MAPHEIGHT * TILESIZE + 20))
            Position += 30
            text = font.render(str(inventory[item]), True, WHITE, BLACK)
            screen.blit(text, (Position, MAPHEIGHT * TILESIZE + 20))
            Position += 50

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT and playerPos[0] + 1 < MAPWIDTH:
                    playerPos[0] += 1
                if event.key == K_LEFT and playerPos[0] > 0:
                    playerPos[0] -= 1
                if event.key == K_DOWN and playerPos[1] + 1 < MAPWIDTH:
                    playerPos[1] += 1
                if event.key == K_UP and playerPos[1] > 0:
                    playerPos[1] -= 1
                if event.key == K_SPACE:
                    current_block = tilemap[playerPos[1]][playerPos[0]]
                    if current_block != DIRT:
                        inventory[current_block] += 1
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                        print inventory
                if event.key == K_z and inventory_position[0] > 0:
                    screen.blit(inventory_anticursor, (inventory_position[0] * 80 + 8, inventory_position[1]))
                    inventory_position[0] -= 1
                if event.key == K_c and inventory_position[0] + 1 < len(resources):
                    screen.blit(inventory_anticursor, (inventory_position[0] * 80 + 8, inventory_position[1]))
                    inventory_position[0] += 1
                if event.key == K_x and inventory[inventory_position[0]] > 0:
                    current_block = tilemap[playerPos[1]][playerPos[0]]
                    inventory[current_block] += 1
                    tilemap[playerPos[1]][playerPos[0]] = inventory_position[0]
                    inventory[inventory_position[0]] -= 1
                if event.key == K_e:
                    inventory_open = True


    if inventory_open:
        inventory_open = False


    pygame.display.update()