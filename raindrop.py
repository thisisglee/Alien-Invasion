import pygame
from random import randint
from pygame.sprite import Sprite


class Raindrop(Sprite):
	"""A class to manage rain"""
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		#load the image and get its rect
		self.image = pygame.image.load('images/rain.bmp')
		self.image = pygame.transform.scale(self.image, (16, 25))
		self.rect = self.image.get_rect()

		#start each new rain drop at the top of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#store the rain's exact veritcal position
		self.y = float(self.rect.y)

	def check_edges(self):
		"""Return True if rain drop hits bottom of the screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.y == screen_rect.bottom:
			return True

	def update(self):
		"""Move the raindrop to bottom of the screen."""
		self.y += self.settings.raindrop_speed
		self.rect.y = self.y
