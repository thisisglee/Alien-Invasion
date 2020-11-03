import pygame
#sprite will group all elementd related at once and on e can use them together
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class to manage Bullet fired from the ship"""
	def __init__(self, ai_game):
		"""Create a bullet at the Ship's current poistion."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		#Create a bullet rect at (0,0) and then set correct position
		self.rect = pygame.Rect((0,0, self.settings.bullet_width, self.settings.bullet_height))
		self.rect.midtop = ai_game.ship.rect.midtop

		#Store the bullet position as a decimal value
		self.y = float(self.rect.y)

	def update(self):
		""" Move bullet up the screen"""
		#Update the decimal value of the bullet
		self.y -= self.settings.bullet_speed
		#Update the rect position
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw the bullet to the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)
