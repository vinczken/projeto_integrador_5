# Example file showing a basic pygame "game loop"
import pygame
from render.controller import Controller

# pygame setup
pygame.init()

info = pygame.display.Info()

factor = 0.8

width = info.current_w * factor 
height = info.current_h * factor

size = width, height

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True
dt = 0

mouse_pos = pygame.mouse.get_pos()
mouse_img = pygame.image.load("assets/imgs/mouse.png")

size_img_mouse = mouse_img.get_size()

with open("assets/map/startmap.txt", "r") as file:
    mapa_inicial = file.read()

tabu_claro = pygame.image.load("assets/imgs/tabu_claro.png")
tabu_escuro = pygame.image.load("assets/imgs/tabu_escuro.png")

tabu_pos = pygame.Vector2(0, 0)

controller = Controller(screen)

while running:

    for event in pygame.event.get():  # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT: running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            controller.handle_click(event.pos)
                        
    
    # poll for events
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = [mouse_pos[0] - size_img_mouse[0] / 2, mouse_pos[1] - size_img_mouse[1] / 2]

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((38, 11, 1))

    controller.draw()
    
    # RENDER YOUR GAME HERE
    screen.blit(mouse_img, mouse_pos)


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit() 