import pygame
import math

pygame.init()

w = 75
h = 75

#15/23

s = pygame.Surface((w,h))
for x in xrange(0,w):
    for y in xrange(0,h):
        relX = w/2 - x
        relY = h/2 - y
        rad = math.sqrt(relX**2 + relY**2)
        if 25 < math.sqrt(relX**2 + relY**2) <= 38:
            b = 1 - (rad - 25 + 0.0)/(38 - 25)
            color = (int(b*155+100),0,0)
        elif math.sqrt(relX**2 + relY**2) <= 25:
            color = (255,255,255)
        else:
            color = (0,0,0)
        s.set_at((x,y),color)

fontColor = (0,0,0)
font = pygame.font.Font('CRYSRG__.TTF', 59)
text = font.render('B',1,fontColor)
textpos = text.get_rect(centerx=38+2,centery=38+1)
s.blit(text,textpos)


pygame.image.save(s,'Mega.bmp')
