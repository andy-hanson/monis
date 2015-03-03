import pygame

def viewTGA(name):
    s = pygame.display.set_mode((1000,600))
    image = pygame.image.load(name+'.TGA').convert_alpha()

    b = 0
    bVel = 1

    done = 0
    while not done:
        b += bVel
        if b == 255 or b == 0:
            bVel *= -1
        s.fill((b,b,b))
        s.blit(image,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = 1
    pygame.quit()

viewTGA('0')
