import pygame.font
from pygame.sprite import Sprite

class Button(Sprite):

	def __init__(self, ai_game, msg):
		"""Initialize button attributes."""
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		#Set the dimesnion and properties of the button
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		self.width, self.height = 300, 50
		self.rect = pygame.Rect(0,0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		#the button message needs to be prepared only once
		self.msg = msg
		self._prep_msg(msg)

	def _prep_msg(self, msg):
		"""Turn msg into a rendered image and center text on the button.
		the boolean value turns antialiasing on or off (meaning  edges of the text smoother)
		remianing arguments specify the font color and background color"""
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		#Draw blank button and then draw message.
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)