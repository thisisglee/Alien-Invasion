import pygame
from scoreboard import Scoreboard
class GameStats:
	"""Track statistics for Alien Invasion"""

	def __init__(self, ai_game):
		"""Iniitialize statistics."""
		self.settings = ai_game.settings
		self.reset_stats()

		#Start Alien Invasion in an inactive state.
		self.game_active = False
		self.choose_level_active = False

		#highscore should never be reset
		self.high_score = Scoreboard.all_time_high_score(self)

	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1