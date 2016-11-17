import pygame
import random


# If we want to use sprites we create a class that inherits from the Sprite class.
# Each class has an associated image and a rectangle.
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid_image
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()

class Background:
    def Create(self):
        global x, y, x1, y1, w, h, background, background_size, background_rect, screen
        background = pygame.image.load('images/space.jpg')
        background_size = background.get_size()
        background_rect = background.get_rect()
        w, h = background_size
        x = 0
        y = 0

        x1 = 0
        y1 = -h
    def Scroll(self):
        global y1, y, h, background, screen
        y1 += 5
        y += 5
        screen.blit(background, (x, y))
        screen.blit(background, (x1, y1))
        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

class Spawn:
    def Asteroids(self):
        for i in range(30):
            asteroid = Asteroid()
            # Set a random location for the new asteroid.
            # All the asteroids are within the left / right boundaries of the screen
            asteroid.rect.x = random.randrange(SCREEN_WIDTH - 20)
            # make sure the asteroids are first above the visual top and then they
            # appear "from above" :-)
            asteroid.rect.y = -random.randrange(120)

            asteroid_list.add(asteroid)
            all_sprites_list.add(asteroid)

class Uprades:
    def Basic(self):
        shot = Missile()
        shot.rect.x = player.rect.x + 17
        shot.rect.y = player.rect.y - 15
        missile_list.add(shot)
        all_sprites_list.add(shot)
    def DualShot(self):
        shot = Missile()
        shot.rect.x = player.rect.x + 5
        shot.rect.y = player.rect.y - 15
        missile_list.add(shot)
        all_sprites_list.add(shot)
        shot2 = Missile()
        shot2.rect.x = player.rect.x + 30
        shot2.rect.y = player.rect.y - 15
        missile_list.add(shot2)
        all_sprites_list.add(shot2)
    def TripleShot(self):
        shot = Missile()
        shot.rect.x = player.rect.x + 17
        shot.rect.y = player.rect.y - 15
        missile_list.add(shot)
        all_sprites_list.add(shot)
        shot2 = Missile()
        shot2.rect.x = player.rect.x + 5
        shot2.rect.y = player.rect.y - 15
        missile_list.add(shot2)
        all_sprites_list.add(shot2)
        shot3 = Missile()
        shot3.rect.x = player.rect.x + 30
        shot3.rect.y = player.rect.y - 15
        missile_list.add(shot3)
        all_sprites_list.add(shot3)

pygame.init()

# Lets load the game images and put them into variables
player_image = pygame.image.load('images/spaceship.png')
asteroid_image = pygame.image.load('images/asteroid.png')
missile_image = pygame.image.load('images/missile.png')

WHITE = (255, 255, 255)
DARK_GREY = (50, 50, 50)

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
asteroid_list = pygame.sprite.Group()
# Group to hold missiles
missile_list = pygame.sprite.Group()
# This is a list of every sprite. All blocks and the player block as well.
# Having an extra group for all sprites makes it far easier to draw them
# all onto the screen.  In fact it's done by a single line of code(line 122)
all_sprites_list = pygame.sprite.Group()

# Create a player block
player = Player()
player.rect.x = 320
player.rect.y = 350

all_sprites_list.add(player)

#Creates the background
bg = Background()
bg.Create()

#Spawns enemies
spawner = Spawn()
spawner.Asteroids()

#Upgrades
upgrade = Uprades()
Dualshot = False
Tripleshot = False

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0

# -------- Main Program Loop -----------
# We need to check out what happens when the player hits the space bar in order to "shoot".
# A new missile is created and gets it's initial position in the "middle" of the player.
# Then this missile is added to the missile sprite-group and also to the all_sprites group.
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Dualshot == True:
                    upgrade.DualShot()
                elif Tripleshot == True:
                    upgrade.TripleShot()
                else:
                    upgrade.Basic()
            if event.key == pygame.K_b:
                spawner.Asteroids()
            if event.key == pygame.K_d:
                if Tripleshot != True:
                    Dualshot = True
            if event.key == pygame.K_t:
                if Dualshot == True:
                    Tripleshot = True
                    Dualshot = False
                else:
                    Tripleshot = True

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        if player.rect.x < -65:
            player.rect.x = 550
        player.rect.x -= 5
    if key[pygame.K_RIGHT]:
        if player.rect.x > 550:
            player.rect.x = - 65
        player.rect.x += 5
    if key[pygame.K_UP]:
        if player.rect.y < 0:
            player.rect.y = 0
        player.rect.y -= 5
    if key[pygame.K_DOWN]:
        if player.rect.y > 350:
            player.rect.y = 350
        player.rect.y += 5

    bg.Scroll()

    # Below is another good example of Sprite and SpriteGroup functionality.
    # It is now enough to see if some missile has collided with some asteroid
    # and if so, they are removed from their respective groups.
    # In other words:  A missile exploded and so did an asteroid.

    # See if the player block has collided with anything.
    pygame.sprite.groupcollide(missile_list, asteroid_list, True, True)
    if pygame.sprite.spritecollide(player, asteroid_list, False):
        all_sprites_list.remove(player)
        print('Collided')

    # Missiles move at a constant speed up the screen, towards the enemy
    for shot in missile_list:
        shot.rect.y -= 5
        if shot.rect.y == 0:
            missile_list.remove(shot)
            all_sprites_list.remove(shot)

    # All the enemies move down the screen at a constant speed
    for block in asteroid_list:
        block.rect.y += 1
        if block.rect.y == 400:
            asteroid_list.remove(block)
            all_sprites_list.remove(block)

    # Draw all the spites
    all_sprites_list.draw(screen)
    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
pygame.quit()