import pygame
import os

def roundPoint(v0,v1=None):
	if v1 is not None:
		return (int(v0),int(v1))
	else:
		return (int(v0[0]),int(v0[1]))

def loadImage(name,colorkey=None):
	fullname = os.path.join('data','images',name)
	img = pygame.image.load(fullname)
	if colorkey:
		img.set_colorkey(colorkey)
	return img, img.get_rect()

def loadTGA(name):
	fullname = os.path.join('data','images',name + '.tga')
	image = pygame.image.load(fullname).convert_alpha()
	return image,image.get_rect()

def equalLists(lista,listb):
	'''Ignores order of elements.'''
	if len(lista) != len(listb):
		return 0
	for element in lista:
		if listb.count(element) != lista.count(element):
			return 0
	return 1

def removeRepeats(listy):
	'''Removes repeats from a list. Non-destructive.'''
	listarg = list(listy)
	index = 0
	while index < len(listarg):
		if listarg.count(listarg[index]) > 1:
			listarg.remove(listarg[index])
			index -= 1
		index += 1
	return listarg

def getNearbySames(x, y, matrix):
	'''Takes a matrix and a position in that matrix and finds all identical elements to the left, right, above, or below (x,y).'''
	'''Returns a list of coordinates.'''
	returnlist = []
	coordinates = []
	#I don't want negative coordinates, and if (x,y) is on the edge x + 1 or y + 1 would make an error normally.
	try:
		if x - 1 >= 0:
			matrix[x-1][y]
			coordinates.append([x-1,y])
	except IndexError:
		pass
	try:
		matrix[x+1][y]
		coordinates.append([x+1,y])
	except IndexError:
		pass
	try:
		if y - 1 >= 0:
			matrix[x][y-1]
			coordinates.append([x,y-1])
	except IndexError:
		pass
	try:
		matrix[x][y+1]
		coordinates.append([x,y+1])
	except IndexError:
		pass
	for coordinate in coordinates:
		if matrix[x][y] == matrix[coordinate[0]][coordinate[1]]:
			returnlist.append(coordinate)
	return returnlist

def getAdjacents(x,y,matrix):
	'''Like getNearbySames, but returns the elements near the near ones, etc.'''
	#List ex: [[x1,y1],[x2,y2],[x3,y3]]
	oldList = []
	newList = [[x,y]]
	while not equalLists(oldList,newList):
		oldList = list(newList)
		index = len(newList)
		while index > 0:
			index -= 1
			for coordinate in getNearbySames(newList[index][0],newList[index][1],matrix):
				newList.append(coordinate)
		newList = removeRepeats(newList)
	return newList

def readHighScore():
	inFile = open(os.path.join('data','high.txt'),'r')
	asStrings = inFile.readlines()
	inFile.close()
	return int(asStrings[0])

def writeHighScore(num):
	outFile = open(os.path.join('data','high.txt'),'w')
	outFile.write(str(num))
	outFile.close()

def playSound(name,volume=0.1):
	'''Plays a sound effect once.'''

	path = os.path.join('data', 'sounds', name)
	try:
		assert os.path.exists(path)
		sound = pygame.mixer.Sound(path)
		sound.set_volume(volume)
		sound.play()
	except:
		print('Cannot load sound:', path)
		raise SystemExit
