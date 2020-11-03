import pygame
from pygame.sprite import Sprite
class Star(Sprite):
	""" A class to manage stars"""
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen

		#load the star image and get is rect
		self.image = pygame.image.load('images/star.bmp')
		self.image = pygame.transform.scale(self.image, (16, 12))
		#transform image ??

		self.rect = self.image.get_rect()

		#Start each new at the top left of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

