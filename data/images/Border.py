import pygame

w = 50
h = 900
s = pygame.Surface((w,h))

yChange = 40
maxYMargin = 40
minX = 10
maxX = 40

pygame.init()

def numToColor(num):
    if num < 1.0/3:   
        R = 0
        G = 0
        B = num*3*255
    else:
        R = 255*(num-1.0/3)*3/2
        G = 255*(num-1.0/3)*3/2
        B = 255
    return (R,G,B)

for x in xrange(0,w):
    for y in xrange(0,h):
        if x < minX:
            yMargin = 0
        elif x > maxX:
            yMargin = maxYMargin
        else:
            yMargin = maxYMargin*(x - minX + 0.0)/(maxX - minX)
        dist = (y + yMargin) % yChange
        if dist < yChange/2:
            dist = yChange - dist
        dist /= 2
        color = numToColor((dist + 0.0)/yChange)
        
        s.set_at((x,y),color)

s2 = pygame.display.set_mode((w,h)).convert_alpha()
s2.fill((0,0,0,0))
k = 10
for m in xrange(0,k):
    pygame.draw.rect(s2,(0,0,0,255*(1 - (m + 1.0)/k)),pygame.Rect(m,m,w-m*2,h-m*2),1)
s.blit(s2,(0,0))

pygame.image.save(s,'border.bmp')
pygame.quit()
