from BlockManager import BlockManager
import helpers

class Border:
	def __init__(self,main):
		self.main = main
		self.image, self.rect = helpers.loadImage('Border.bmp')
		for anObject in self.main.objects:
			if isinstance(anObject, BlockManager):
				self.rect.x = anObject.gridWidth * anObject.blockSize
		self.rect.y = 0 #Not really needed. It's the default.

	def compute(self):
		pass

	def draw(self, surface):
		surface.blit(self.image, (self.rect.x, self.rect.y))
