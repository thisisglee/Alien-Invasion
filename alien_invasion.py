#sys module to exit the game when player quits
import sys
#pygame to contain thye functionality to build the game
import pygame
#random for stars
from random import randint
#to pause the game for momnet when ship hits alien
from time import sleep

#importing the settings
from settings import Settings
#import gamestats
from game_stats import GameStats
#import scoreboard
from scoreboard import Scoreboard
#import button
from button import Button
#import star
from star import Star
#import rain
from raindrop import Raindrop
#importing ship
from ship import Ship
#inmporting Bullet0
from bullet import Bullet
#importing aliens
from alien import Alien

class AlienInvasion:
	"""Overall class to manage assets and behaviors"""
	def __init__(self):
		"""Initialize the game and create game resources"""
		pygame.init()

		#instance of settings
		self.settings = Settings()

		#OLD ONE - self.screen = pygame.display.set_mode((800,600))
		self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))

		#caption
		pygame.display.set_caption("Alien Invasion")

		#Create an instance to store game statistics,
		# and create a scoreboard
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		#Set the background color
		self.bg_color=(self.settings.bg_color)

		#instance of Stars
		self.stars = pygame.sprite.Group()
		self._create_stars_background()

		#instance of rain
		self.rain = pygame.sprite.Group()
		self._create_rain_background()

		#instance of Ship
		self.ship = Ship(self)

		#instance of bullet using sprite Group which behaves as a list but with extra functionality
		self.bullets = pygame.sprite.Group()

		#instance of Alien using sprite to group or fleet of aliens
		self.aliens = pygame.sprite.Group()
		self._create_fleet()

		#Make the play buton. 
		self.play_button =Button(self, "Play")

		#make the difficulty button
		#self.difficulty_button = Button(self,"Difficulty Level", 3)
		self.difficulty_buttons = pygame.sprite.Group()
		self._create_level_button()

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()
			#self._update_rain()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()

	def _check_events(self):
		#Respond to keyboard and mouse events.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			#when event pressed
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

			elif event.type == pygame.MOUSEBUTTONDOWN and self.stats.choose_level_active == True:
				mouse_pos = pygame.mouse.get_pos()
				self._check_difficulty_button(mouse_pos)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
				
			#when event released
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self.stats.choose_level_active = True

	def _create_level_button(self):
		"""Background full of stars"""
		screen_rect = self.screen.get_rect()
		height = self.settings.screen_height // 4
		msg = ["Rookie","Intermediate","Pro"]

		for level in range(0,3):
			self._create_level(msg[level], height)
			height += 100

	def _create_level(self, msg, row_number):
		difficulty_button = Button(self,msg)
		difficulty_button.rect.y = row_number

		difficulty_button._prep_msg(msg)
		self.difficulty_buttons.add(difficulty_button)
			
	def _start_game(self, difficulty_level):
		#Reset the game statistics.
			#Button for difficulty level
			level = 1.1
			if difficulty_level == "Rookie":
				level = 1.1
			if difficulty_level == "Intermediate":
				level = 1.3
			if difficulty_level == "Pro":
				level = 1.5

			self.speedup_scale = level

			self.stats.reset_stats()
			self.settings.initilaize_dynamic_settings()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#Get rid of any remianing aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#hide the cursor when game is playing
			pygame.mouse.set_visible(False)

	def _check_difficulty_button(self,mouse_pos):
		"""After new game select diffucty level-
			Rookie- 1.1 , Intermeditae- 1.2, Pro- 1.4"""
		for level in self.difficulty_buttons.sprites():
			if level.rect.collidepoint(mouse_pos):
				self.stats.choose_level_active = True
				self._start_game(level.msg)
		
	def _check_keydown_events(self, event):
		if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and not self.stats.game_active:
			#start game
			self.stats.choose_level_active = True
		elif event.key == pygame.K_RIGHT:
			#move ship to right by 1
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			#move ship to leftt by 1
			self.ship.moving_left = True
		elif event.key == pygame.K_UP:
			#move ship to up by 1
			self.ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			#move ship to down by 1
			self.ship.moving_down = True
		elif event.key == pygame.K_SPACE:
			#while event.key == pygame.K_SPACE:
				#fire bullet
			self._fire_bullet()
		elif event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			#stop moving ship when right key is realeas
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			#move ship to leftt by 1
			self.ship.moving_left = False
		elif event.key == pygame.K_UP:
			#move ship to up by 1
			self.ship.moving_up = False
		elif event.key == pygame.K_DOWN:
			#move ship to down by 1
			self.ship.moving_down = False

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets"""
		#Update bullet postions.
		self.bullets.update()

		#Get rid of the bullets that diapperared
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <=0:
				self.bullets.remove(bullet)

		self._check_bullet_collisions()

	def _check_bullet_collisions(self):
		#Check for any bullets that have hit aliens
		#if so, get rid of the bullet and the alien
		#collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
		# when powerful bullet to destroy all
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points *len(aliens)
				self.sb.prep_score()
				self.sb.check_high_score()
		if not self.aliens:
			self._start_new_level()
			

	def _start_new_level(self):
		#Destroy existing bullets and create new fleet.
		self.bullets.empty()
		self._create_fleet()
		self.settings.increase_speed()

		#increase level
		self.stats.level += 1
		self.sb.prep_level()

	def _create_stars_background(self):
		"""Background full of stars"""
		star = Star(self)
		star_width, star_height = star.rect.size
		available_space_x = self.settings.screen_width - (2 * star_width)
		number_stars_x = available_space_x // (star_width)

		#Determine the number of rows of aliens that fit on the screen
		number_rows = self.settings.screen_width // (star_height)

		#Create the full background of stars at random places
		max_stars = (number_stars_x * number_rows) // 50

		for times in range(max_stars):
			random_x, random_y = randint(0, number_stars_x), randint(0, number_rows)
			self._create_star(random_x, random_y)


		# for row_number in range(number_rows):
		# 	for star_number in range(number_stars_x):
		# 		#to randomize star position
		# 		random_bool = randint(0, 50)
		# 		if random_bool < 3:
		# 			self._create_star(star_number, row_number)

	def _create_star(self, star_number, row_number):
		star = Star(self)
		star_width,star_height = star.rect.size
		star.x = star_width + 2*star_width * star_number
		star.rect.x = star.x
		star.rect.y = star.rect.height + (2* star.rect.height) * row_number
		self.stars.add(star)

	def _create_rain_background(self):
		"""background of rain"""
		rain = Raindrop(self)
		raindrop_width, raindrop_height = rain.rect.size
		available_space_x = self.settings.screen_width - (2 * raindrop_width)

		number_raindrop_x = available_space_x // (raindrop_width)

		#Determine the number of rows of raindrop that fit on the screen
		number_rows = (self.settings.screen_width // raindrop_height)

		# #Create the full background of stars at random places
		max_rain = number_raindrop_x // 10

		for times in range(max_rain):
			random_x, random_y = randint(0, number_raindrop_x), randint(0, number_rows)
			self._create_rain(random_x, random_y)

	def _create_rain(self, raindrop_number, row_number):
		rain = Raindrop(self)
		rain_width,rain_height = rain.rect.size
		rain.x = rain_width + 2*rain_width * raindrop_number
		rain.rect.x = rain.x
		rain.rect.y = rain.rect.height + (2* rain.rect.height) * row_number
		self.rain.add(rain)

	def _check_rain_edges(self):
		"""Repsonod appropriately if raindrop reched bottom"""
		for raindrop in self.rain.sprites().copy(): 
			if raindrop.check_edges():
				random_x = randint(0, self.settings.screen_width)
				raindrop.x, raindrop.rect.x, raindrop.y, raindrop.rect.y = random_x, random_x, 0, 0
				# self.rain.remove(raindrop)
				# self._create_rain_background()
				# break

	def _update_rain(self):
		"""Check if the raindrop at an edge"""
		self._check_rain_edges()
		self.rain.update()

	def _create_fleet(self):
		"""Create fleet of aliens"""
		#make an alien
		#Spacing between each alien is equal to one alien width
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // ( 2 * alien_width)

		#Determine the number of rows of aliens that fit on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		#Create the full fleet of Aliens
		for row_number in range(number_rows):
			for alien_number in  range(number_aliens_x):
				#Create an alien and place it in the row
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size
		alien.x = alien_width + 2*alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + (2* alien.rect.height) * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge"""
		for alien in self.aliens.sprites(): 
			if alien.check_edges():
				self._change_fleet_direction() 
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_aliens(self):
		""" Check if the fleet is at an edge. Update the position of all the aliens in the fleet"""
		self._check_fleet_edges()
		self.aliens.update()

		#Look for alien ship collision
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		#Look for aliens hitting bottom of the screen
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""Respond to the ship being hit by an alien."""
		if self.stats.ships_left > 0:
			#Decrement ships_left and update score board
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			#Get rid of any remainimg aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()
			#Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()
			#pause
			sleep(0.5)		
		else:
			self.stats.game_active = False
			self.stats.choose_level_active = False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Treat this the same as if the ship got hit.
				self._ship_hit()
				break

	def _update_screen(self):
		#Redraw the screen during each phase through the loop
		self.screen.fill(self.bg_color)
		self.stars.draw(self.screen)
		#self.rain.draw(self.screen)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		if self.stats.game_active:
			self.aliens.draw(self.screen)
		#Draw the score information.
		self.sb.show_score()
		#Draw the play button if th egame is inactive
		if self.stats.game_active != True and self.stats.choose_level_active !=True:
			self.play_button.draw_button()
		if self.stats.game_active != True and self.stats.choose_level_active ==True:
			for level in self.difficulty_buttons.sprites():
				level.draw_button()
			
		#Make the most recenlty drwan screen visible.
		pygame.display.flip()

if __name__ == '__main__':
	#Make a game instance and run the game
	ai = AlienInvasion()
	ai.run_game()
