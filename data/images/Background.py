import pygame

s = pygame.image.load('BackgroundPRE.png')
d = pygame.Surface((1440-900,900))
d.set_alpha(128)
s.blit(d,(900,0))

pygame.image.save(s,'Background.png')
