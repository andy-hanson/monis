import pygame
import random

import BlockManager
import helpers
from Lasers import Lasers

class ItemManager:
	def __init__(self,main):
		self.main = main
		self.items = [] #Type, x, y, time remaining

		'''
			Type List:
			0 - Combo bonus
			1 - vertical bomb
			2 - horizontal bomb
			3 - diagonal bomb, up-left to down-right
			4 - diagonal bomb, down-left to up-right
			5 - Destroy a 7*7 squared centered around (x,y)
			6 - Create a Lasers object.
			7 - Randomly choose.
		'''

		self.time = 0

		# These are set by BlockManager
		self.itemFrec = None
		self.itemLastTime = None #Start value does not matter.

		for anObject in self.main.objects:
			if isinstance(anObject,BlockManager.BlockManager):
				self.blockManager = anObject

		self.itemImages = [
			helpers.loadImage('comboBonus.png')[0],
			helpers.loadTGA('V')[0],
			helpers.loadTGA('H')[0],
			helpers.loadTGA('ULtoDR')[0],
			helpers.loadTGA('DLtoUR')[0],
			helpers.loadTGA('Mega')[0],
			helpers.loadTGA('Fire')[0],
			helpers.loadTGA('Random')[0]
		]

		self.itemFlickerTime = 64 #Item begins to flicker when its time reaches this number

		self.itemsAvailable = 8

	def compute(self):
		i = 0
		while i < len(self.items):
			self.items[i][3] -= 1
			if self.items[i][3] == 0:
				self.items.remove(self.items[i])
				i -= 1
			i += 1

		self.time += 1
		if self.itemFrec: #It can be set to None to turn off items.
			if self.time % self.itemFrec == 0:
				x = random.randint(0,self.blockManager.gridWidth-1)
				y = random.randint(0,self.blockManager.gridHeight-1)

				#Make sure no two items are on the same spot.
				works = 0
				while not works:
					works = 1
					for item in self.items:
						if item[1] == x and item[2] == y:
							works = 0
							x = random.randint(0,self.blockManager.gridWidth-1)
							y = random.randint(0,self.blockManager.gridHeight-1)


				itemType = random.randint(0, self.itemsAvailable-1)
				self.items.append([itemType,x,y,self.itemLastTime])

	def draw(self,surface):
		for item in self.items:
			if item[3] > self.itemFlickerTime or item[3] % 2:
				surface.blit(self.itemImages[item[0]],(item[1]*self.blockManager.blockSize,item[2]*self.blockManager.blockSize))

	def getDestroyedBlocks(self,points):
		for point in points:
			i = 0
			while i < len(self.items):
				if self.items[i][1] == point[0] and self.items[i][2] == point[1]:
					self.getItemActivated(self.items[i][0],self.items[i][1],self.items[i][2])
					self.items.remove(self.items[i])
					i -= 1
				i += 1

	def getItemActivated(self,itemType,x,y):
		# TODO: Object orientation...

		if itemType == 7:
			itemType = random.randint(0,5) #It's a ?. Randomly picks between the other options.

		if itemType == 0:
			self.main.scorer.comboPlusTen()

		elif itemType == 1:
			#vertical bomb
			for y2 in range(0,self.blockManager.gridHeight):
				self.destroyPoint(x,y2)
			helpers.playSound('bomb.wav',.5)

		elif itemType == 2:
			#horizontal bomb
			for x2 in range(0,self.blockManager.gridWidth):
				self.destroyPoint(x2,y)
			helpers.playSound('bomb.wav',.5)

		elif itemType == 3:
			#diagonal bomb, up-left to down-right
			x2 = x
			y2 = y
			while x2 < self.blockManager.gridWidth and y2 < self.blockManager.gridHeight:
				self.destroyPoint(x2,y2)
				x2 += 1
				y2 += 1
			x2 = x
			y2 = y
			while x2 >= 0 and y2 >= 0:
				self.destroyPoint(x2,y2)
				x2 -= 1
				y2 -= 1
			helpers.playSound('bomb.wav',.5)

		elif itemType == 4:
			#diagonal bomb, down-left to up-right
			x2 = x
			y2 = y
			while x2 < self.blockManager.gridWidth and y2 >= 0:
				self.destroyPoint(x2,y2)
				x2 += 1
				y2 -= 1
			x2 = x
			y2 = y
			while x2 >= 0 and y2 < self.blockManager.gridHeight:
				self.destroyPoint(x2,y2)
				x2 -= 1
				y2 += 1
			helpers.playSound('bomb.wav',.5)

		elif itemType == 5:
			#Destroy a 7*7 squared centered around (x,y)
			startX = x - 3
			if startX < 0:
				startX = 0
			endX = x + 3
			if endX > self.blockManager.gridWidth - 1:
				endX = self.blockManager.gridWidth - 1
			startY = y - 3
			if startY < 0:
				startY = 0
			endY = y + 3
			if endY > self.blockManager.gridHeight - 1:
				endY = self.blockManager.gridHeight - 1
			for x2 in range(startX,endX+1):
				for y2 in range(startY,endY+1):
					self.destroyPoint(x2,y2)
			helpers.playSound('bomb.wav',.5)

		elif itemType == 6:
			self.main.objects.append(Lasers(self.main))

	def destroyPoint(self,x,y):
		if self.blockManager.grid[x][y] is not None:
				self.main.explosionGraphics.getPoint(x*self.blockManager.blockSize+self.blockManager.blockSize/2,y*self.blockManager.blockSize+self.blockManager.blockSize/2)
		self.blockManager.grid[x][y] = None
