import pygame
import random

w = 900
h = 900

useless = pygame.display.set_mode((300,300))

s = pygame.Surface((w,h))
star = pygame.image.load('star.TGA').convert_alpha()

numStars = 2048
for k in xrange(0,numStars):
    x = random.randint(0,w)
    y = random.randint(0,h)
    size = random.randint(1,32)

    s.blit(pygame.transform.smoothscale(star,(size,size)),(x-size/2,y-size/2))

pygame.image.save(s,'Background.bmp')
