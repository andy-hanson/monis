import pygame

def crop(imageName,string=None,stretchHeight=None,newName = None):
    s = pygame.image.load(imageName + '.bmp')

    #Make it symetrical (for the blocks)
    right = s.subsurface(pygame.Rect(s.get_width()/2,0,s.get_width()/2,s.get_height()-1)).copy()
    s.blit(pygame.transform.flip(right,1,0),(0,0))
    
    c = s.get_at((0,0))

    y1 = -1
    done = 0

    while not done:
        y1 += 1
        for x in xrange(0,s.get_width()):
            if s.get_at((x,y1)) != c:
                done = 1

    x1 = -1
    done = 0

    while not done:
        x1 += 1
        for y in xrange(0,s.get_height()):
            if s.get_at((x1,y)) != c:
                done = 1

    y2 = 0
    done = 0

    while not done:
        y2 += 1
        for x in xrange(0,s.get_width()):
            if s.get_at((x,s.get_height() - y2)) != c:
                done = 1

    x2 = 0
    done = 0

    while not done:
        x2 += 1
        for y in xrange(0,s.get_height()):
            if s.get_at((s.get_width() - x2,y)) != c:
                done = 1

    s2 = pygame.Surface((s.get_width() - x1 - x2,s.get_height() - y1 - y2))
    s2.blit(s,(-x1,-y1))
    if stretchHeight:
        s2 = pygame.transform.smoothscale(s2,(int(stretchHeight),int(stretchHeight)))
    
    if newName:
        pygame.image.save(s2,newName + '.bmp')
    else:
        pygame.image.save(s2,imageName + '.png')

crop('0','notFactor',75)
