import pygame
import os

from BlockManager import BlockManager
from Border import Border
from ItemManager import ItemManager
from scorer import Scorer
import helpers
import graphics
import EZMenu

class Main:
	def __init__(self):
		pygame.display.init()
		info = pygame.display.Info()
		self.COMPUTER_RESOLUTION = (info.current_w,info.current_h)

		self.FIELD_WIDTH = 1440
		self.FIELD_HEIGHT = 900
		#fullscreenString = EZMenu.EZMenu("Pick a display mode. Use arrow keys and enter.",["Fullscreen","Window"],80)
		self.fullscreen = False #fullscreenString == "Fullscreen"

		self.setScreen()

		pygame.font.init()

		self.FPS = 30
		self.clock = pygame.time.Clock()

		self.objects = []
		self.objects.append(BlockManager(self))
		self.scorer = Scorer(self)
		self.objects.append(self.scorer)
		self.objects.append(ItemManager(self))
		self.objects.append(Border(self))

		self.font = pygame.font.Font(os.path.join('data','CRYSRG__.TTF'),64) #For FPS warnings

		self.explosionGraphics = graphics.ExplosionGraphics()
		self.background = helpers.loadImage('Background.png')[0]

		pygame.mixer.init()
		pygame.display.set_caption('Monis 2 - Dec 22 09 - Use arrow keys to move, p to pause')

		self.go()

	def toggleFullscreen(self):
		self.fullscreen = not self.fullscreen
		self.setScreen()

	def setScreen(self):
		if self.fullscreen:
			self.drawScreen = self.drawScreen = pygame.Surface((self.FIELD_WIDTH,self.FIELD_HEIGHT))
			self.screen = pygame.display.set_mode(self.COMPUTER_RESOLUTION,pygame.FULLSCREEN)

			self.xMargin = 0
			self.yMargin = 0
			size = (self.screen.get_width() + 0.0)/self.screen.get_height() #Commonly 4/3 or 16/9.
			drawScreenDimensions = (self.FIELD_WIDTH + 0.0)/self.FIELD_HEIGHT
			if size > drawScreenDimensions: #The screen is tall, ex. 4/3
				self.SCREEN_FACTOR = (self.screen.get_width() + 0.0)/self.FIELD_WIDTH
				self.yMargin = int((self.screen.get_height() - self.FIELD_HEIGHT*self.SCREEN_FACTOR)/2)
			elif size < drawScreenDimensions: #The screen is wide, ex. 16/9
				self.SCREEN_FACTOR = (self.screen.get_height() + 0.0)/self.FIELD_HEIGHT
				self.xMargin = int((self.screen.get_width() - self.FIELD_WIDTH*self.SCREEN_FACTOR)/2)
			else:
				self.SCREEN_FACTOR = 1
				self.drawScreen = self.screen #They are the same size, so just blit directly!

		else:
			self.drawScreen = pygame.Surface((self.FIELD_WIDTH,self.FIELD_HEIGHT))
			self.SCREEN_WIDTH = 1440
			self.SCREEN_HEIGHT = 900
			self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))

	def go(self):
		self.done = 0
		while not self.done:
			self.getInput()
			self.computeAll()
			self.drawAll()
			self.clock.tick(self.FPS)
		pygame.quit()

	def getInput(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					for anObject in self.objects:
						try:
							anObject.getDown()
						except AttributeError:
							pass
				elif event.key == pygame.K_LEFT:
					for anObject in self.objects:
						try:
							anObject.getLeft()
						except AttributeError:
							pass
				elif event.key == pygame.K_RIGHT:
					for anObject in self.objects:
						try:
							anObject.getRight()
						except AttributeError:
							pass
				elif event.key == pygame.K_ESCAPE:
					self.done = 1
				elif event.key == pygame.K_p:
					self.pause()
				elif event.key == pygame.K_f:
					self.toggleFullscreen()

			if event.type == pygame.QUIT:
				self.done = 1

	def computeAll(self):
		i = 0
		while i < len(self.objects):
			self.objects[i].compute()

			try:
				if self.objects[i].dead:
					self.objects.remove(self.objects[i])
					i -= 1
			except AttributeError:
				pass
			i += 1
			self.explosionGraphics.compute()

	def drawAll(self):
		self.drawScreen.fill((0,0,0))
		self.drawScreen.blit(self.background,(0,0))

		for anObject in self.objects:
			anObject.draw(self.drawScreen)
		self.explosionGraphics.draw(self.drawScreen)

		#Show a warning if the framerate is low
		fps = self.clock.get_fps()
		if fps < self.FPS and 0:
			text = self.font.render('LOW FPS ' + str(int(self.clock.get_fps())) + '/' + str(self.FPS),1,(255,0,0))
			centerx = self.scorer.centerx
			pos = text.get_rect(centerx=centerx,centery=100)
			self.drawScreen.blit(text,pos)

		if self.fullscreen:
			if self.SCREEN_FACTOR == 1:
				pass
			else:
				self.screen.blit(pygame.transform.smoothscale(self.drawScreen, \
								(int(self.FIELD_WIDTH*self.SCREEN_FACTOR),int(self.FIELD_HEIGHT*self.SCREEN_FACTOR))),(self.xMargin,self.yMargin))
		if not self.fullscreen:
			self.screen.blit(pygame.transform.smoothscale(self.drawScreen,(self.SCREEN_WIDTH,self.SCREEN_HEIGHT)),(0,0))
		pygame.display.flip()

	def pause(self):
		done = 0
		while not done:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					done = 1

	def lose(self):
		score = self.scorer.score
		highScore = self.scorer.highScore
		if score > highScore:
			helpers.writeHighScore(score)

		self.drawScreen.fill((0,0,0))
		text = self.font.render('GAME OVER',1,(255,255,255))
		textpos = text.get_rect(centerx = self.FIELD_WIDTH/2,centery = self.FIELD_HEIGHT/4)
		self.drawScreen.blit(text,textpos)
		text = self.font.render('Score: ' + str(score),1,(255,255,255))
		textpos = text.get_rect(centerx = self.FIELD_WIDTH/2,centery = self.FIELD_HEIGHT/2)
		self.drawScreen.blit(text,textpos)
		if score < highScore:
			text = self.font.render('High Score: ' + str(highScore),1,(255,255,255))
			textpos = text.get_rect(centerx = self.FIELD_WIDTH/2,centery = self.FIELD_HEIGHT*3/4)
			self.drawScreen.blit(text,textpos)
		else:
			text = self.font.render('NEW HIGH SCORE!',1,(255,255,255))
			textpos = text.get_rect(centerx = self.FIELD_WIDTH/2,centery = self.FIELD_HEIGHT*3/4)
			self.drawScreen.blit(text,textpos)

		if not self.fullscreen:
			self.screen.blit(pygame.transform.scale(self.drawScreen,(self.SCREEN_WIDTH,self.SCREEN_HEIGHT)),(0,0))

		pygame.display.flip()
		pygame.time.wait(16000)
		self.done = 1


a = Main()
