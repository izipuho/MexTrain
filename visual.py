#!/usr/bin/env python3
import pygame
import math
import sys

def tileBackground(screen: pygame.display, image: pygame.Surface) -> None:
    screenWidth, screenHeight = screen.get_size()
    imageWidth, imageHeight = image.get_size()

    # Calculate how many tiles we need to draw in x axis and y axis
    tilesX = math.ceil(screenWidth / imageWidth)
    tilesY = math.ceil(screenHeight / imageHeight)

    # Loop over both and blit accordingly
    for x in range(tilesX):
        for y in range(tilesY):
            screen.blit(image, (x * imageWidth - 10, y * imageHeight))


pygame.init()
scr_res = (1280, 720)
display_screen = pygame.display.set_mode(scr_res, flags=pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("MexTrain")
running = True

bg = pygame.image.load('img/background/cloth2.png', 'Background')

# Tile image
tile = pygame.image.load('img/tile.png', 'Empty tile')
tile = pygame.transform.scale(tile, (100, 100))


class Button:
    def __init__(self):
        pass


# white color
color = (255, 255, 255)
# light shade of the button
color_light = (170, 170, 170)
# dark shade of the button
color_dark = (100, 100, 100)
# sizes
width = display_screen.get_width()
height = display_screen.get_height()
# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)
# rendering a text written in
# this font
text = smallfont.render('quit', True, color)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                pygame.quit()

    # disp_color = pygame.Color(0, 204, 0)
    # display_screen.fill(disp_color)
    tileBackground(display_screen, bg)
    # display_screen.blit(tile, (10, 10))
    mouse = pygame.mouse.get_pos()
    if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
        pygame.draw.rect(display_screen, color_light, [width / 2, height / 2, 140, 40])

    else:
        pygame.draw.rect(display_screen, color_dark, [width / 2, height / 2, 140, 40])

    # superimposing the text onto our button
    display_screen.blit(text, (width / 2 + 50, height / 2))

    pygame.display.flip()
    clock.tick(60)
# Update your screen when required
# pygame.display.update()
# quit the pygame initialization and module
pygame.quit()
# End the program
# quit()