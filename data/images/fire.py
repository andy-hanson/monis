import pygame
import math

useless = pygame.display.set_mode((300,300))

shot = pygame.image.load('Shot.TGA').convert_alpha()

s = pygame.Surface((150,150)).convert_alpha()
s.fill((0,0,0,0))

numShots = 9
r = 45
ang = -math.pi/2
while ang < math.pi*2 - math.pi/2:
    i = pygame.transform.rotate(shot,-ang*180/math.pi + 180)
    centerX = s.get_width()/2.0 + r*math.cos(ang)
    centerY = s.get_height()/2.0 + r*math.sin(ang)
    s.blit(i,(centerX-i.get_width()/2,centerY-i.get_height()/2))

    ang += math.pi*2/numShots

s = pygame.transform.smoothscale(s,(75,75))
pygame.image.save(s,'fire.TGA')
pygame.quit()
