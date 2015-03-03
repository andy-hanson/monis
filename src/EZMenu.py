import os
import pygame

import helpers


def EZMenu(title,strings,fontsize=24):
	'''Displays a list of strings and lets the user choose one. Returns the chosen string.'''
	#Set the size to just barely fit everything.
	pygame.font.init()
	font = pygame.font.Font('data/CRYSRG__.ttf',fontsize)
	longest = 0
	for string in strings:
		if font.size(string)[0] > longest: #[0] - only intersted in x-coordinate
			longest = font.size(string)[0]
	WIDTH = longest + 10 #Add a margin
	HEIGHT = fontsize*(len(strings))

	backgroundColor = (0,0,0)
	offColor = (128,128,128)
	onColor = (255,255,255)
	activeIndex = 0#The string that is currently selected.

	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(title)
	pygame.display.set_icon(helpers.loadImage('MenuIcon.bmp',(255,0,255))[0])
	pygame.draw.rect(screen,backgroundColor,pygame.Rect(0,0,WIDTH,HEIGHT))

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return strings[activeIndex]
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN: #The enter key! Remember kids, 'RETURN' is just 'ENTURR' rearranged!
					pygame.quit()
					return strings[activeIndex]
				elif event.key == pygame.K_DOWN:
					if activeIndex < len(strings) - 1:
						activeIndex += 1
				elif event.key == pygame.K_UP:
					if activeIndex > 0:
						activeIndex -= 1

		screen.fill(backgroundColor)
		drawStrings(screen,strings,offColor,fontsize,backgroundColor,activeIndex + 1,onColor)
		#1 is added to activeIndex because title is part of the string list passed to drawStrings.
		pygame.time.wait(100)
		pygame.display.flip()

def drawStrings(surface, strings, color, fontsize, backgroundColor, specialIndex=-1, specialColor=(255,255,255)):
	'''Draws the strings onto the surface. specialIndex is drawn in specialColor.'''
	pygame.font.init()
	font = pygame.font.Font('data/CRYSRG__.ttf',fontsize)
	ypos = fontsize/2
	index = 0
	while index < len(strings):
		if index == specialIndex - 1:
			text = font.render(strings[index],1,specialColor)
		else:
			text = font.render(strings[index],1,color)
		pos = text.get_rect(centerx = surface.get_width()/2,centery = ypos)
		surface.blit(text,pos)
		ypos += fontsize
		index += 1
