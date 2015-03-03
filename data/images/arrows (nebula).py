import pygame
import math
import random

def numToColor(num):
    num = random.random()*num
    num **= 1.0/3
    if num < 1.0/3:
        num *= 3
        R  = 255*num
        G = 0
        B = 0
    elif num < 2.0/3:
        num = (num - 1.0/3)*3
        R = 255
        G = 255*num
        B = 0
    else:
        num = (num - 2.0/3)*3
        R = 255
        G = 255
        B = 255*num
    A = 255*num
    return (R,G,B,A)
        

pygame.init()


def gradient(inputName):
    outline = pygame.image.load(inputName)
    w = outline.get_rect().width
    h = outline.get_rect().height


    progress = pygame.display.set_mode((222,1))
    #pygame.display.set_icon(pygame.image.load('Result.bmp'))

    s = pygame.Surface((w,h)).convert_alpha()
    white = (255,255,255)
    black = (0,0,0)

    array = []
    for x in xrange(0,w):
        thisColumn = []
        for y in xrange(0,h):
            if outline.get_at((x,y)) == (255,255,255,255):
                thisColumn.append(1)
            else:
                thisColumn.append(0)
        array.append(thisColumn)

    dists = []
    for x in xrange(0,w):
        l = []
        for y in xrange(0,h):
            l.append(0)
        dists.append(l)
        
    maxMinDist = 0 #The maximum value for all minDists found.

    #Method: Expand in squares looking for white. Once you've found white, you'll have to still go out, because you're looking for the closest in a circular range.
    #When doing a point just next to another, you can use just under the same square 'radius' value as before.

    percentInt = 0
    
    #Find maxMinDist
    for x in xrange(0,w):
        lastR = 1
        for y in xrange(0,h):
            if array[x][y] == 1:
                pass
            else:
                minDist = None
                firstR = None
                r = lastR - 1
                if r < 1:
                    r = 1
                while not firstR or r < firstR*math.sqrt(2) + 1:
                    points = []
                    for x2 in xrange(x-r,x+r):
                        points.append([x2,y-r])
                        points.append([x2,y+r])
                    for y2 in xrange(y-r,y+r):
                        points.append([x-r,y2])
                        points.append([x+r,y2])
                    i = 0
                    while i < len(points):
                        if points[i][0] < 0 or points[i][0] >= w or points[i][1] < 0 or points[i][1] >= h:
                            points.remove(points[i])
                            i -= 1
                        i += 1
                    for point in points:
                        x2 = point[0]
                        y2 = point[1]
                        if array[x2][y2] == 1:
                            if minDist:
                                if minDist <= math.sqrt((x2 - x)**2 + (y2 - y)**2):
                                    pass #It's further away than last time.
                                else:
                                    minDist = math.sqrt((x2 - x)**2 + (y2 - y)**2)
                            else:
                                minDist = math.sqrt((x2 - x)**2 + (y2 - y)**2)
                                lastR = r
                                if not firstR:
                                    firstR = r
                    r += 1
                dists[x][y] = minDist
                maxMinDist = max(minDist,maxMinDist)
                
            percent = (x + (y + 0.0)/h)/w
            k = str(int(percent*10000%100)) #The decimal part of the percent, the Ks in XX.KK%
            if len(k) == 1:
                k = '0' + str(int(percent*10000%100))
            percentString = str(int(percent*100)) + '.' + k
            pygame.display.set_caption('Progress - ' + percentString + '%')

    #Using maxMinDist, fill in with gradient.
    for x in xrange(0,w):
        for y in xrange(0,h):
            if array[x][y] == 1:
                color = (0,0,0,0)
            else:
                minDist = dists[x][y]
                b = minDist/maxMinDist
                
                color = numToColor(b)
            s.set_at((x,y),color)

    return s

def smooth(surface,rad):
    s2 = pygame.Surface((w + 2*rad, h + 2*rad + 2)).convert_alpha()
    s2.fill((0,0,0,0))
    s2.blit(surface,(rad,rad))
    s3 = pygame.Surface((w + 2*rad, h + 2*rad + 2)).convert_alpha()
    s3.fill((0,0,0,0))
    for x in xrange(rad,w+rad):
        for y in xrange(rad,h+rad):
            rTotal = 0
            gTotal = 0
            bTotal = 0
            aTotal = 0
            numPoints = 0
            for x2 in xrange(x - rad, x + rad):
                for y2 in xrange(y - rad, y + rad):
                    if math.sqrt((x - x2)**2 + (y - y2)**2) <= rad:
                        col = s2.get_at((x2,y2))
                        rTotal += col[0]
                        gTotal += col[1]
                        bTotal += col[2]
                        aTotal += col[3]
                        numPoints += 1
            rTotal /= numPoints
            gTotal /= numPoints
            bTotal /= numPoints
            aTotal /= numPoints
            s3.set_at((x,y),(rTotal,gTotal,bTotal,aTotal))
        progressPercent = (x - rad + 0.0)/(w - rad)
        pygame.display.set_caption(str(int(progressPercent*100)))
    return s3

def brighten(surface):
    maxA = 0
    for x in xrange(surface.get_width()):
        for y in xrange(surface.get_height()):
            maxA = max(maxA,surface.get_at((x,y))[3])
    factor = 255.0/maxA
    for x in xrange(surface.get_width()):
        for y in xrange(surface.get_height()):
            p = surface.get_at((x,y))
            surface.set_at((x,y),(p[0],p[1],p[2],p[3]*factor))
    return surface


s = gradient('Arrow Outline.bmp')
w = s.get_width()
h = s.get_height()
rad = 8
s = smooth(s,rad)
s = brighten(s)

#All arrow directions
s2 = pygame.Surface((150,150)).convert_alpha()
s2.fill((0,0,0,0))
s2.blit(s,(-(s.get_width()-150)/2,-(s.get_height()-150)/2))
pygame.image.save(s,'arrow1.TGA')
pygame.image.save(pygame.transform.smoothscale(s2,(75,75)),'H.TGA')
s2 = pygame.transform.rotate(s2,90)
pygame.image.save(pygame.transform.smoothscale(s2,(75,75)),'V.TGA')
s2 = pygame.transform.rotate(s2,45)
s3 = pygame.Surface((150,150)).convert_alpha()
s3.fill((0,0,0,0))
s3.blit(s2,(-(s2.get_width()-150)/2,-(s2.get_height()-150)/2))
s3 = pygame.transform.smoothscale(s3,(75,75))
pygame.image.save(s3,'ULtoDR.TGA')
s3 = pygame.transform.flip(s3,1,0)
pygame.image.save(s3,'DLtoUR.TGA')


pygame.quit()
