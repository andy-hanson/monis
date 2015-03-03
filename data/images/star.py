import pygame
import math

useless = pygame.display.set_mode((300,300))

w = 120
h = 120
s = pygame.Surface((w,h)).convert_alpha()

def numToColor(num):
    R = 255
    G = 255
    B = 255
    A = num*255
    return (R,G,B,A)

for x in xrange(0,w):
    for y in xrange(0,h):
        relX = x - w/2
        relY = y - h/2
        dist = math.sqrt(relX**2 + relY**2 + 0.0)/math.sqrt(w**2/4 + h**2/4)
        angle = math.atan2(relY,relX) + math.pi/2
        k = math.pi*2/5
        b = (angle%(k))/(k)
        if b < .5:
            b = 1 - b
        b = (b - .5)*2
        b **= 3
        n = .5
        b = (b*.5) + 1 - n
        b *= (1 - dist)**2

        b **= 2
        
        color = numToColor(b)
        try:
            s.set_at((x,y),color)
        except TypeError:
            print b
            print dist
            print color
            jk

pygame.image.save(s,'Star.TGA')

s2 = pygame.Surface((w,h))
s2.fill((0,0,0))
s2.blit(s,(0,0))

#pygame.image.save(s2,'BigStar.BMP')
