#pygame testing
# Tutorial: https://realpython.com/pygame-a-primer/
# Sprite credit: Skorpio (spaceship) https://opengameart.org/content/spaceship-4
#				 samoliver (missile) https://opengameart.org/content/missile-0

import pygame
import random
from pygame.locals import (
	RLEACCEL,
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	KEYDOWN,
	QUIT
)

#Step 1: initialize
pygame.init()
score = 0

#Defining the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
    	if pressed_keys[K_UP]:
    		self.rect.move_ip(0, -2)
    	if pressed_keys[K_DOWN]:
    		self.rect.move_ip(0, 2)
    	if pressed_keys[K_LEFT]:
    		self.rect.move_ip(-2, 0)
    	if pressed_keys[K_RIGHT]:
    		self.rect.move_ip(2, 0)

    	# Keep player on the screen
    	if self.rect.left < 0:
        	self.rect.left = 0
    	if self.rect.right > SCREEN_WIDTH:
        	self.rect.right = SCREEN_WIDTH
    	if self.rect.top <= 0:
        	self.rect.top = 0
    	if self.rect.bottom >= SCREEN_HEIGHT:
        	self.rect.bottom = SCREEN_HEIGHT

#Defining the enemy
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.surf = pygame.Surface((20,10))
		self.surf.fill((255, 255, 255))
		self.rect = self.surf.get_rect(
			center = (
				random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
				random.randint(0, SCREEN_HEIGHT)
			)
		)
		self.speed = random.randint(1, 5)

	def update(self):
		self.rect.move_ip(-self.speed,0)
		if self.rect.right < 0:
			global score
			score += 1
			self.kill()



#Create window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])



#Create event for adding new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)


#Instantiate plyer and groups
player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


#Running loop
running = True
while running:

	#Check if user quit
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		elif event.type == ADDENEMY:
			new_enemy = Enemy()
			enemies.add(new_enemy)
			all_sprites.add(new_enemy)


	#Get keys pressed
	pressed_keys = pygame.key.get_pressed()


	#Update player and enemy locations
	player.update(pressed_keys)
	enemies.update()


	#Draw screen and objects
	screen.fill((0,0,0))


	#Draw player and enemy on the screen
	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)


	#Collision detection
	if pygame.sprite.spritecollideany(player, enemies):
		player.kill()
		running = False


	#Refresh display
	pygame.display.flip()

print(score)
pygame.quit()