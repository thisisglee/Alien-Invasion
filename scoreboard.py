import pygame.font
from pygame.sprite import Sprite
from ship import Ship

class Scoreboard:
	"""A class to report scoring information"""
	def __init__(self, ai_game):
		"""Initialize scorekeeping attributes."""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		#Font settings for scoring information
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont(None, 40)

		#Prepare the initial score image
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		"""Turn the score into a rendered image."""
		rounded_score = round(self.stats.score, -1)
		#string format directive for comma seprators
		score_str = "{:,}".format(rounded_score)
		score_str = f' Current Score: {score_str}'
		self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

		#Display the core at the top right of the screen.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Turn the highscore into a rendered image."""
		high_score = self.all_time_high_score()
		high_score_str = "{:,}".format(high_score)
		high_score_str = f' High Score: {high_score_str}'
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

		#Center the high score at the top of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def prep_level(self):
		"""Turn the level into a renedered image."""
		level_str = f' Level: {str(self.stats.level)}'
		self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

		#Position the level below the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		"""Show how many ships are left."""
		self.ships = pygame.sprite.Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)

			#chagne the size of ship
			ship.image = pygame.image.load('images/ship.bmp')
			ship.image = pygame.transform.scale(ship.image, (36, 64))
			ship.rect = ship.image.get_rect()

			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def all_time_high_score(self):
		try:
			with open("highscore.txt", 'r') as f:
				all_time_high_score = (f.read()).rstrip()
				if all_time_high_score == "":
					return 0
				else:
					return int(all_time_high_score)
		except Exception as e:
			raise e


	def check_high_score(self):
		"""Check to see if there's a new high score."""
		print(self.stats.high_score < self.stats.score)
		if self.stats.high_score < self.stats.score:
			self.stats.high_score = self.stats.score
			# write to highscore.txt
			try:
				with open("highscore.txt", 'wt') as f:
			   		f.write(f"{self.stats.high_score}\n")
			except Exception as e:
				raise e
			self.prep_high_score()

	def show_score(self):
		"""Draw score to the screen."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)