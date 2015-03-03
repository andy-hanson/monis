import pygame

def darkToAlpha(imageName,bT,op):
    img = pygame.image.load(imageName)
    #bT = brightness Threshhold
    useless = pygame.display.set_mode((300,300))
    s = pygame.Surface((img.get_width(),img.get_height())).convert_alpha()
    for x in xrange(0,img.get_width()):
        for y in xrange(0,img.get_height()):
            col = img.get_at((x,y))
            if 1:#((x-img.get_width()/2)**2 + (y-img.get_height()/2)**2)**.5 > 22: #MEGA ONLY
                bright = sum(col) - 255 #Will have a final alpha value of 255
                if bright > bT:
                    a = 255
                else:
                    a = (bright + 0.0)/bT * 255
                s.set_at((x,y),(col[0],col[1],col[2],a))
            else:
                s.set_at((x,y),(col[0],col[1],col[2],255))
    pygame.image.save(s,str(op) + '.TGA')
    
    pygame.quit()

for x in xrange(1,8):
    darkToAlpha(str(x) + '.png',160,x)
darkToAlpha('0.png',80,0)

def convertBack(imageName):
    img = pygame.image.load(imageName + '.TGA')
    s = pygame.Surface((img.get_width(),img.get_height()))
    for x in xrange(0,img.get_width()):
        for y in xrange(0,img.get_height()):
            c = img.get_at((x,y))
            s.set_at((x,y),(c[0],c[1],c[2]))
    pygame.image.save(s,imageName + '.png')

'''for x in xrange(0,8):
    convertBack(str(x))'''
