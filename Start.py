import pygame
import random


# -----------Variables-----------------
time = 0
speed = 1
score = 0
spawnrate = 200
grayship_spawnrate = 100
Invulnerablecounter = 0
life = 3
player_speed = 6
Invulnerable = False
Stop = False
Start = False
WHITE = (255, 255, 255)
DARK_GREY = (50, 50, 50)

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 400
# ------------- Font ------------
pygame.font.init()
font_path = "fonts/Titlefont.otf"
font_size = 64
fontObj = pygame.font.Font(font_path, font_size)

# ----------Image Loader---------------
player_image = pygame.image.load('images/spaceship.png')
player_imagedark = pygame.image.load('images/spaceship1.png')
player_imagelight = pygame.image.load('images/spaceship2.png')
life_image = pygame.transform.scale(player_image, (20, 20))
asteroid_image = pygame.image.load('images/asteroid.png')
missile_image = pygame.image.load('images/missile.png')
grayship_image = pygame.image.load('images/spaceship1.png')


# -------------------------------------

# --------------Classes----------------
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

class GrayShip(pygame.sprite.Sprite):
    xpos = 0                                # defines the x spawn position
    ypos = 0                                # defines the y spaw position
    xtarget = 0                             # defines the x target position(the position the grayship is moving to)
    ytarget = 0                             # defines the y target position
                        # defines how many moves it will take to get to the target
    fireRate = random.randrange(500,750)    # defines the space between fireing, lower number = more rapid fire
    moveSpeed = random.randrange(5)         # defines how many pixles the grayship moves per update
    onTarget = False                        # defines if the grayship is on target

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = grayship_image
        self.rect = self.image.get_rect()


class Background:
    def create(self):
        global x, y, x1, y1, w, h, background, background_size, background_rect, screen
        background = pygame.image.load('images/space.jpg')
        background_size = background.get_size()
        background_rect = background.get_rect()
        w, h = background_size
        x = 0
        y = 0

        x1 = 0
        y1 = -h

    def scroll(self):
        global y1, y, h, background, screen, speed
        y1 += speed
        y += speed
        screen.blit(background, (x, y))
        screen.blit(background, (x1, y1))
        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

    def openingscreen(self):
        global fontObj
        Title = fontObj.render("Space Rush", 1, (8, 255, 0))
        help = font.render("Use arrows keys to move and Spacebar to shoot", 1, (8, 255, 0))
        startext = font.render("Press Spacebar to Start", 1, (8, 255, 0))
        pygame.Surface.blit(screen, Title, (120, 100))
        pygame.Surface.blit(screen, help, (60, 250))
        pygame.Surface.blit(screen, startext, (180, 300))

    def endscreen(self):
        global fontObj, score
        Title = fontObj.render("Game Over", 1, (8, 255, 0))
        endscoretext = str("You finished with " + str(score) + " Score")
        endscore = font.render(endscoretext, 1, (8, 255, 0))
        credit = font.render("This game was made by Alexander and Pall", 1, (8, 255, 0))
        pygame.Surface.blit(screen, Title, (110, 100))
        pygame.Surface.blit(screen, endscore, (150, 250))
        pygame.Surface.blit(screen, credit, (80, 300))

    def scoreBoard(self):
        global score, life
        scoretext = font.render("Score:" + str(score), 1, (8, 255, 0))
        pygame.draw.rect(screen, (0, 0, 0), (590, 10, 150, 20))
        pygame.Surface.blit(screen, scoretext, (590, 10))

    def lifeBoard(self):
        lifetext = font.render("Life:", 1, (8, 255, 0))
        pygame.draw.rect(screen, (0, 0, 0), (590, 40, 150, 50))
        pygame.Surface.blit(screen, lifetext, (590, 40))
        for x in range(life):
            pygame.Surface.blit(screen, life_image, ((580 + (x * 25 + 10)), 70))


class Spawn:
    def asteroids(self):
        for i in range(30):
            asteroid = Asteroid()
            # Set a random location for the new asteroid.
            # All the asteroids are within the left / right boundaries of the screen
            asteroid.rect.x = random.randrange(550 - 20)
            # make sure the asteroids are first above the visual top and then they
            # appear "from above" :-)
            asteroid.rect.y = -random.randrange(120)

            asteroid_list.add(asteroid)
            all_sprites_list.add(asteroid)

    def Grayship(self):
        #defines the grayship
        grayship = GrayShip()

        #defines the grayship position
        grayship.rect.x = random.randrange(550)
        grayship.rect.y = random.randrange(100)

        def findTarget(self): #defines the grayship target
            grayship.xtarget = random.randrange(550)
            grayship.ytarget = random.randrange(300)


        if grayship.onTarget == True:
            findTarget()
            grayship.onTarget = False
        
        grayship_list.add(grayship)
        all_sprites_list.add(grayship)
        def move(self):
            distX = grayship.xtarget - grayship.rect.x
            distY = grayship.ytarget - grayship.rect.y
            #target = 
            

            #if the dist is bigger than the moveSpeed
            #if it is smaller. Set the pos = the target
            #if lean is pos
                #move the moveSpeed on X and the moveSpeed * lean on Y
            #if lean is neg
                #move the-moveSpeed on X and the moveSpood * lean on Y


class Uprades:
    def basic(self):
        shot = Missile()
        shot.rect.x = player.rect.x + 17
        shot.rect.y = player.rect.y - 15
        missile_list.add(shot)
        all_sprites_list.add(shot)

    def dualShot(self):
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

    def tripleShot(self):
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

class Game:
    def End(self):
        global Stop
        print("You Lost")
        missile_list.empty()
        asteroid_list.empty()
        all_sprites_list.empty()
        Stop = True
    def Hit(self):
        global Invulnerablecounter, Invulnerable
        if time % 3 == 0:
            all_sprites_list.remove(player)
        else:
            if Invulnerablecounter == 70:
                Invulnerable = False
                all_sprites_list.add(player)
            else:
                Invulnerablecounter += 1
                all_sprites_list.add(player)



# ---------------------------------------------

pygame.init()
pygame.display.set_caption('SpaceRush')
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
font = pygame.font.Font(None, 30)

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
asteroid_list = pygame.sprite.Group()
# Group to hold missiles
missile_list = pygame.sprite.Group()
#Group to hold the grayships
grayship_list = pygame.sprite.Group()
# This is a list of every sprite. All blocks and the player block as well.
# Having an extra group for all sprites makes it far easier to draw them
# all onto the screen.  In fact it's done by a single line of code(line 122)
all_sprites_list = pygame.sprite.Group()

# Create a player block
player = Player()
player.rect.x = 320
player.rect.y = 350

all_sprites_list.add(player)

# Creates the background
bg = Background()
bg.create()
bg.scoreBoard()
bg.lifeBoard()

# Spawns enemies
spawner = Spawn()
spawner.asteroids()

# Upgrades
upgrade = Uprades()
Dualshot = False
Tripleshot = False

# Loop until the user clicks the close button.
game = Game()
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#-------------Opening Screen --------------
while not Start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Start = True
    bg.scroll()
    bg.openingscreen()
    pygame.display.flip()
# -------- Main Program Loop -----------
# We need to check out what happens when the player hits the space bar in order to "shoot".
# A new missile is created and gets it's initial position in the "middle" of the player.
# Then this missile is added to the missile sprite-group and also to the all_sprites group.
while not Stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Dualshot:
                    upgrade.dualShot()
                elif Tripleshot:
                    upgrade.tripleShot()
                else:
                    upgrade.basic()
            if event.key == pygame.K_b:
                spawner.asteroids()
            if event.key == pygame.K_d:
                if not Tripleshot:
                    Dualshot = True
            if event.key == pygame.K_t:
                if Dualshot:
                    Tripleshot = True
                    Dualshot = False
                else:
                    Tripleshot = True
            if event.key == pygame.K_s:
                speed += 1


    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        if player.rect.x < 5:
            player.rect.x = 5
        player.rect.x -= player_speed
    if key[pygame.K_RIGHT]:
        if player.rect.x > 540:
            player.rect.x = 540
        player.rect.x += player_speed
    if key[pygame.K_UP]:
        if player.rect.y < 0:
            player.rect.y = 0
        player.rect.y -= player_speed
    if key[pygame.K_DOWN]:
        if player.rect.y > 350:
            player.rect.y = 350
        player.rect.y += player_speed

    time += 1
    if Invulnerable:
        game.Hit()

    if not Stop:
        bg.scroll()

    if not Stop:
        if time % 10 == 0:
            score += 1
            bg.scoreBoard()
        if time % spawnrate == 0:
            spawner.asteroids()
        if time % grayship_spawnrate == 0:
            spawner.Grayship()

    if pygame.sprite.groupcollide(missile_list, asteroid_list, True, True):
        score += 10
        bg.scoreBoard()
    if pygame.sprite.spritecollide(player, asteroid_list, False):
        if not Invulnerable:
            life -= 1
            bg.lifeBoard()
            if life == 0:
                game.End()
            else:
                print('Collided')
                Invulnerable = True
                Invulnerablecounter = 0
    if pygame.sprite.groupcollide(missile_list, grayship_list, True, True):
        score += 20
        bg.scoreBoard()


    # Missiles move at a constant speed up the screen, towards the grayship
    for shot in missile_list:
        shot.rect.y -= 5
        if shot.rect.y == 0:
            missile_list.remove(shot)
            all_sprites_list.remove(shot)

    # All the enemies move down the screen at a constant speed
    for comic in asteroid_list:
        comic.rect.y += speed + 1
        if comic.rect.y == 400:
            asteroid_list.remove(comic)
            all_sprites_list.remove(comic)

    for ship in grayship_list:
        if ship.rect.x > 520:
            ship.rect.x -= random.randint(1, 20)
        elif ship.rect.x < 10:
            ship.rect.x += random.randint(1, 20)
        else:
            ship.rect.x += random.randint(-50, 50)
        if ship.rect.y == 400:
            grayship_list.remove(ship)
            all_sprites_list.remove(ship)

    # Draw all the spites
    all_sprites_list.draw(screen)
    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

while Stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Stop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Start = True
    bg.scroll()
    bg.endscreen()
    pygame.display.flip()

pygame.quit()
