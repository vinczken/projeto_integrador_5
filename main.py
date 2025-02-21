# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()

size = width, height = 1280, 720

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True
dt = 0

mouse_pos = pygame.mouse.get_pos()
mouse_img = pygame.image.load("assets/imgs/mouse.png")


while running:

    for event in pygame.event.get():  # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT: running = False
    
    # poll for events
    mouse_pos = pygame.mouse.get_pos()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    screen.blit(mouse_img, mouse_pos)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit() 