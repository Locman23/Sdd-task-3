# **Setup Python**
import sys

import pygame

# **Setup pygame/window**
mainClock = pygame.time.Clock()
from pygame.locals import *  # import pygame modules

pygame.init()  # initiates pygame
pygame.display.set_caption('Main')  # sets window name
WINDOW_SIZE = [600, 400]  # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiates screen
display = pygame.Surface((300, 200))
icon = pygame.image.load('ICON.png')
pygame.display.set_icon(icon)

moving_right = False
moving_left = False
vertical_momentum = 0

# player_location = [50, 50]
# player_y_momentum = 0
# player_rect = pygame.Rect(player_location[0], player_location[1], player_img.get_width(), player_img.get_height())

game_map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '2', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2', '0', '0', '0', ],
            ['1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '2', '2', '2', ],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]
grass_img = pygame.image.load('grassdirt.png')
dirt_img = pygame.image.load('dirt.png')

player_img = pygame.image.load('player.png').convert()
player_img.set_colorkey((255, 255, 255))

player_rect = pygame.Rect(100, 100, 5, 13)
air_time = 0


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


# Loop
while True:  # game loop
    display.fill((153, 217, 234))
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img, (x * 16, y * 16))
            if tile == '2':
                display.blit(grass_img, (x * 16, y * 16))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        air_time = 0
        vertical_momentum = 0
    else:
        air_time += 1
    display.blit(player_img, (player_rect.x, player_rect.y))

    # inputs
    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # check for window quit
            pygame.quit()  # stop pygame
            sys.exit()  # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_time < 6:
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    # Update
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()  # Update display
    mainClock.tick(60)  # Maintain 60 fps
