import pygame

import helpers

class ExplosionGraphics:
	def __init__(self):
		self.explosionLastTime = 20
		self.explosionPoints = [] #X,Y,Time,minRad,maxRad
		self.explosionImage = helpers.loadTGA('Explosion')[0]
		self.xScroll = 0
		self.yScroll = 0
	def compute(self):
		i = 0
		while i < len(self.explosionPoints):
			self.explosionPoints[i][0] += self.xScroll
			self.explosionPoints[i][1] += self.yScroll
			self.explosionPoints[i][2] -= 1
			if self.explosionPoints[i][2] == 0:
				self.explosionPoints.remove(self.explosionPoints[i])
				i -= 1
			i += 1

	def draw(self,surface):
		for p in self.explosionPoints:
			minRad = p[3]
			maxRad = p[4]
			thisRad = minRad + (maxRad-minRad)*(self.explosionLastTime - p[2])/self.explosionLastTime
			scaledImage = pygame.transform.smoothscale(self.explosionImage,helpers.roundPoint(thisRad*2,thisRad*2))

			minX = p[0] - thisRad
			minY = p[1] - thisRad
			#If: Can't take a subsurface if it doesn't intersect at all!
			if minX < surface.get_width() and minY < surface.get_height() and minX + thisRad*2 > 0 and minY + thisRad*2 > 0:
				if minX < 0:
					width = thisRad*2 + minX
					minX = 0
				else:
					width = thisRad*2
				if minY < 0:
					height = thisRad*2 + minY
					minY = 0
				else:
					height = thisRad*2
				if minX + width >= surface.get_width():
					width = surface.get_width() - minX
				if minY + height >= surface.get_height():
					height = surface.get_height() - minY
				tempSurface = surface.subsurface(pygame.Rect(minX,minY,width,height)).copy()
				if minX == 0:
					blitX = width - thisRad*2
				else:
					blitX = 0
				if minY == 0:
					blitY = height - thisRad*2
				else:
					blitY = 0
				tempSurface.blit(scaledImage,(blitX,blitY))
				a = 255*p[2]/self.explosionLastTime
				tempSurface.set_alpha(a)

				surface.blit(tempSurface,(minX,minY))

	def getPoint(self,x,y,minRad=0,maxRad=150):
		self.explosionPoints.append([x,y,self.explosionLastTime - 1,minRad,maxRad])
