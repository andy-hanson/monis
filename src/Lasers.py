import math
import pygame
import random

import BlockManager
import helpers

class Lasers:
	def __init__(self, main):
		self.main = main

		self.firesLeft = 64
		self.time = 0
		self.fireFrec = 8

		for anObject in self.main.objects:
			if isinstance(anObject, BlockManager.lockManager):
				self.blockManager = anObject

	def compute(self):
		self.time += 1
		if self.time % self.fireFrec == 0:
			x = random.randint(0,self.blockManager.gridWidth-1)
			y = random.randint(0,self.blockManager.gridHeight-1)
			self.blockManager.grid[x][y] = None
			self.main.explosionGraphics.getPoint(
				x*self.blockManager.blockSize+self.blockManager.blockSize/2,
				y+self.blockManager.blockSize+self.blockManager.blockSize/2)

			self.main.objects.append(
				ShotLine(
					self.main,
					x*self.blockManager.blockSize + self.blockManager.blockSize/2,
					y*self.blockManager.blockSize + self.blockManager.blockSize/2))
			#+ blockSize/2 so it's in the center of the square, not the upper-left corner.

			self.firesLeft -= 1
			if self.firesLeft == 0:
				self.dead = 1

			helpers.playSound('laser.wav')

	def draw(self,surface):
		pass

class ShotLine:
	def __init__(self,main,x,y):
		self.main = main
		self.x = x
		self.y = y
		self.maxTime = 4
		self.time = self.maxTime

		for anObject in self.main.objects:
			if isinstance(anObject,BlockManager):
				blockManager = anObject

		self.centerx = blockManager.gridWidth*blockManager.blockSize/2
		self.centery = blockManager.gridHeight*blockManager.blockSize/2
		self.direction = math.atan2(self.y - self.centery,self.x - self.centerx)
		self.rad = (self.centerx**2 + self.centery**2)**.5 + 5
		self.color = (0,255,255)

	def compute(self):
		self.time -= 1
		if self.time == 0:
			self.dead = 1

	def draw(self,surface):
		pointDist = ((self.x - self.centerx)**2 + (self.y - self.centery)**2)**.5
		mult = 1 - pointDist/self.rad
		angDif = mult*math.pi/48# math.pi/108
		x2 = self.centerx + self.rad*math.cos(self.direction+angDif)
		if x2 > self.centerx*2:
			x2 = self.centerx*2
		y2 = self.centery + self.rad*math.sin(self.direction+angDif)
		x3 = self.centerx + self.rad*math.cos(self.direction-angDif)
		if x3 > self.centerx*2:
			x3 = self.centerx*2
		y3 = self.centery + self.rad*math.sin(self.direction-angDif)
		pygame.draw.polygon(surface,self.color,[(self.x,self.y),(x2,y2),(x3,y3)])
