import pygame
import os

import BlockManager
import helpers

class Scorer:
	def __init__(self,main):
		self.main = main

		self.score = 0

		self.combo = 1
		self.comboGain = 1
		for anObject in self.main.objects:
			if isinstance(anObject,BlockManager.BlockManager):
				maxTimeTillNew = anObject.maxTimeTillNew
				self.centerx = (self.main.FIELD_WIDTH + anObject.gridWidth*anObject.blockSize + 50)/2 #For blitting text. Border has a width of 50.

		self.comboLastTime = maxTimeTillNew * 5
		self.comboLoseCounter = self.comboLastTime

		self.highFont = pygame.font.Font(os.path.join('data','CRYSRG__.TTF'), 64)
		self.score1Font = pygame.font.Font(os.path.join('data','CRYSRG__.TTF'), 128)
		self.score2Font = pygame.font.Font(os.path.join('data','CRYSRG__.TTF'), 256)
		self.combo1Font = pygame.font.Font(os.path.join('data','CRYSRG__.TTF'), 128)
		self.combo2Font = pygame.font.Font(os.path.join('data','CRYSRG__.TTF'), 256)

		self.highScore = helpers.readHighScore()

	def compute(self):
		if self.combo > 1:
			self.comboLoseCounter -= 1
			if self.comboLoseCounter == 0:
				self.combo = 1
				self.comboLoseCounter = self.comboLastTime

	def draw(self,surface):
		text = self.highFont.render('High: ' + str(self.highScore),1,(255,255,255))
		pos = text.get_rect(centerx = self.centerx,top=0)
		surface.blit(text,pos)

		text = self.score1Font.render('Score',1,(255,255,255))
		pos = text.get_rect(centerx = self.centerx,bottom=260)
		surface.blit(text,pos)
		text = self.score2Font.render(str(self.score),1,(255,255,255))
		pos = text.get_rect(centerx = self.centerx,top=230)
		surface.blit(text,pos)

		text = self.combo1Font.render('Combo',1,(255,255,255))
		pos = text.get_rect(centerx = self.centerx,bottom=670)
		surface.blit(text,pos)
		text = self.combo2Font.render(str(self.combo),1,(255,255,255))
		pos = text.get_rect(centerx = self.centerx,top=650)
		surface.blit(text,pos)

	def getDestroyedBlocks(self,num):
		'''Get num new blocks to use to calculate the score.'''
		self.score += 2**(num-3) * self.combo

		#Make a noise based on the combo before the block landed.
		maxCombo = 15
		combo = self.combo
		if combo > maxCombo:
			combo = maxCombo
		helpers.playSound('combo' + str(combo) + '.wav')

		self.combo += self.comboGain * (num-2)
		self.comboLoseCounter = self.comboLastTime

		if self.score > 9999:
			self.score = 9999

	def comboPlusTen(self):
		self.combo += 10

