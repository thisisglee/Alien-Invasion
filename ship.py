import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""A class to manage Ship"""

	def __init__(self, ai_game):
		"""Initialize the ship and set its starting position."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
		self.image = pygame.image.load('images/ship.bmp')
		self.image = pygame.transform.scale(self.image, (73, 128))
		self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
		self.rect.midbottom = self.screen_rect.midbottom

		# Store a float value for the ship's horizontal position
		self.x, self.y = float(self.rect.x), float(self.rect.y)

		#MOvement Flag
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self):
		"""Update the ship's positon based on the movement flag"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		elif self.moving_left and self.rect.left > self.screen_rect.left:
			self.x -= self.settings.ship_speed
		elif self.moving_up and self.rect.top > self.screen_rect.top:
			self.y -= self.settings.ship_speed
		elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.y += self.settings.ship_speed 

		#update rect object from self.x and self.y
		self.rect.x, self.rect.y = self.x, self.y

	def center_ship(self):
		"""Create the ship on the screen."""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x, self.y = float(self.rect.x), float(self.rect.y)
	
	def blitme(self):
		"""Draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)