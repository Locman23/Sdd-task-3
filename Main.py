# **Setup Python**
import pygame
from pygame import *
import sys
from Main_modules import *

# **Setup pygame/window**
mainClock = pygame.time.Clock()

pygame.init()  # initiates pygame
pygame.display.set_caption('Main')  # sets window name
WINDOW_SIZE = [600, 400]  # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiates screen
display = pygame.Surface((300, 200))
icon = pygame.image.load('Images/ICON.png')
pygame.display.set_icon(icon)
game_map = loadmap('map1')
grass_img = pygame.image.load('Images/grassdirt.png')
dirt_img = pygame.image.load('Images/dirt.png')
moving_right = False
moving_left = False
vertical_momentum = 0

player_img = pygame.image.load('Images/player.png').convert()
player_img.set_colorkey((255, 255, 255))

background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [130, 90, 100, 400]],
                      [0.5, [120, 10, 70, 400]]]

player_rect = pygame.Rect(100, 100, 5, 13)
air_time = 0
float_scroll = [0, 0]

# Loop
while True:  # game loop
    display.fill((153, 217, 234))
    tile_rects = []
    y = 0

    float_scroll[0] += (player_rect.x - float_scroll[0] - 152) / 20
    float_scroll[1] += (player_rect.y - float_scroll[1] - 106) / 20
    scroll = float_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))

    # Parallax scrolling effect
    Paralax_scrolling(background_objects, scroll, display)

    # Tile map system
    Tile_map(game_map, scroll, dirt_img, grass_img, tile_rects, display)

    # Player movement Speed
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    display.blit(player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    
    # Jump only once thingy
    if collisions['bottom']:
        air_time = 0
        vertical_momentum = 0
    else:
        air_time += 1



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
