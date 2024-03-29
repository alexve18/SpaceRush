import pygame
import math
import random
from Connection import connection

# -----------Variables-----------------
time = 0
speed = 1
score = 0
spawnrate = 200
grayship_spawnrate = 100
firespeed_low = 100
firespeed_high = 200
Invulnerablecounter = 0
life = 3
player_speed = 6
playername = 'Default'
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
font_size2 = 41
fontObj = pygame.font.Font(font_path, font_size)
fontObj2 = pygame.font.Font(font_path, font_size2)

# ----------Image Loader---------------
player_image = pygame.image.load('images/spaceship.png')
life_image = pygame.transform.scale(player_image, (25, 25))
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = grayship_image
        self.rect = self.image.get_rect()
    
    xtarget = 0 # defines the x target position(the position the grayship is moving to)
    ytarget = 0  # defines the y target position
    # defines how many moves it will take to get to the target
    fireRate = 0  # defines the space between fireing, lower number = more rapid fire
    moveSpeed = 0  # defines how many pixles the grayship moves per update


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

    def ThankYou(self):
        global fontObj2, score
        Title = fontObj2.render("Takk fyrir Skolagonguna", 1, (8, 255, 0))
        endtext = str("Thar sem thetta er sidasta verkefni")
        end2text = str("Sem eg geri i Taekniskolanum")
        end3text = str("Kvedja Alexander")
        endscreen = font.render(endtext, 1, (8, 255, 0))
        end2screen = font.render(end2text, 1, (8, 255, 0))
        end3screen = font.render(end3text, 1, (8, 255, 0))
        pygame.Surface.blit(screen, Title, (0, 100))
        pygame.Surface.blit(screen, endscreen, (100, 200))
        pygame.Surface.blit(screen, end2screen, (100, 225))
        pygame.Surface.blit(screen, end3screen, (100, 250))

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
            pygame.Surface.blit(screen, life_image, ((580 + (x * 35 + 10)), 60))

    def TopScorers(self):
        scorers = conn.Display()
        drawnumber = 90
        pygame.draw.rect(screen, (0,0,0), (590, 90, 150, 300))
        for x in range(len(scorers)):
            text = str(x + 1) + ". " + scorers[x]
            scorer = font.render(text, 1, (8, 255, 0))
            pygame.Surface.blit(screen, scorer, (590, drawnumber))
            drawnumber += 30


class Spawn:
    def asteroids(self):
        for i in range(30 + score / 100):
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
        global firespeed_low, firespeed_high
        # defines the grayship
        grayship = GrayShip()

        # defines the grayship position
        grayship.rect.x = random.randrange(40,510)
        grayship.rect.y = random.randrange(40,160)

        grayship.xtarget = random.randrange(40,510)
        grayship.ytarget = random.randrange(40,160)

        grayship.fireRate = random.randrange(firespeed_low,firespeed_high)

        grayship.moveSpeed = random.randrange(1,3)

        all_sprites_list.add(grayship) #not in all sprites due to the fact they move differently
        enemy_list.add(grayship)


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
    def gameover(self):
        global Stop, score
        print("You Lost")
        missile_list.empty()
        enemy_missle_list.empty()
        asteroid_list.empty()
        enemy_list.empty()
        all_sprites_list.empty()
        Stop = True
        conn.newScorer(playername, score)
        bg.TopScorers()
        game.EndScreen()

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

    def StartScreen(self):
        global Start
        game.Init()
        bg.TopScorers()
        while not Start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Start = True
                        game.GameScreen()
                    if event.key == pygame.K_t:
                        Start = True
                        game.ThankScreen()

            bg.scroll()
            bg.openingscreen()
            pygame.display.flip()

    def ThankScreen(self):
        global Start
        game.Init()
        bg.TopScorers()
        while not Stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            bg.scroll()
            bg.ThankYou()
            pygame.display.flip()

    def GameScreen(self):
        global speed, score, life, time, Dualshot, Tripleshot, Invulnerable, Invulnerablecounter, Stop, grayship_spawnrate, firespeed_low, firespeed_high
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
                if score > 1500:
                    Dualshot = True
                    speed = 3
                    firespeed_low = 60
                    firespeed_high = 80
                if score > 3000:
                    Tripleshot = True
                    Dualshot = False
                    speed = 5
                    grayship_spawnrate = 50
                    firespeed_low = 40
                    firespeed_high = 60

            if pygame.sprite.groupcollide(missile_list, asteroid_list, True, True):
                score += 10
                bg.scoreBoard()
            if pygame.sprite.spritecollide(player, asteroid_list, False):
                if not Invulnerable:
                    life -= 1
                    bg.lifeBoard()
                    if life == 0:
                        game.gameover()
                    else:
                        print('Collided')
                        Invulnerable = True
                        Invulnerablecounter = 0
            if pygame.sprite.spritecollide(player, enemy_missle_list, False):
                if not Invulnerable:
                    life -= 1
                    bg.lifeBoard()
                    if life == 0:
                        game.gameover()
                    else:
                        print('Collided')
                        Invulnerable = True
                        Invulnerablecounter = 0
            if pygame.sprite.groupcollide(missile_list, enemy_list, True, True):
                score += 20
                bg.scoreBoard()

            # Missiles move at a constant speed up the screen, towards the grayship
            for shot in missile_list:
                shot.rect.y -= 5
                if shot.rect.y == 0:
                    missile_list.remove(shot)
                    all_sprites_list.remove(shot)

            # Enemy Missles
            for shot in enemy_missle_list:
                shot.rect.y += 5
                if shot.rect.y == 350:
                    enemy_missle_list.remove(shot)
                    all_sprites_list.remove(shot)

            # All the enemies move down the screen at a constant speed
            for comic in asteroid_list:
                comic.rect.y += speed + 1
                if comic.rect.y == 400:
                    asteroid_list.remove(comic)
                    all_sprites_list.remove(comic)

            for hostile in enemy_list:
                xpos = hostile.rect.x
                ypos = hostile.rect.y
                    
                xtarget = hostile.xtarget
                ytarget = hostile.ytarget

                moveSpeed = hostile.moveSpeed

                xdist = abs(xtarget - xpos)
                ydist = abs(ytarget - ypos)


                dist = int(math.sqrt(xdist**2 + ydist**2))
                if ydist == 0 or xdist == 0:
                    pass
                else:
                    ymove = int(ydist/xdist)
                if ymove > 3:
                    ymove = 3
                if ydist < moveSpeed:
                    ypos = ytarget
                    ymove = 0
                if dist <= moveSpeed:
                    xpos = xtarget
                    ypos = ytarget
                    xtarget = random.randrange(40,510)
                    ytarget = random.randint(40,160)
                else:
                    if xtarget > xpos:
                        xpos = xpos + moveSpeed
                    elif xpos > xtarget:
                        xpos = xpos - moveSpeed
                    if ytarget > ypos:
                        ypos = ypos + ymove
                    elif ypos > ytarget:
                        ypos = ypos - ymove

                hostile.rect.x = xpos
                hostile.rect.y = ypos
                hostile.xtarget = xtarget
                hostile.ytarget = ytarget
                if time % hostile.fireRate == 0:
                    enemyshot = Missile()
                    enemyshot.rect.x = hostile.rect.x + 18
                    enemyshot.rect.y = hostile.rect.y + 30
                    enemy_missle_list.add(enemyshot)
                    all_sprites_list.add(enemyshot)

            # Draw all the spites
            all_sprites_list.draw(screen)
            # Limit to 60 frames per second
            clock.tick(60)
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

    def EndScreen(self):
        global speed, Start, Stop
        while Stop:
            speed = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Stop = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game.StartScreen()
            bg.scroll()
            bg.endscreen()
            pygame.display.flip()
    def Init(self):
        global speed, Start, Stop, score, life, Dualshot, Tripleshot

        Stop = False
        Start = False
        Dualshot = False
        Tripleshot = False
        speed = 1
        score = 0
        life = 3
        player.rect.x = 320
        player.rect.y = 350
        all_sprites_list.add(player)
        bg.lifeBoard()
        bg.scoreBoard()


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
# Group to hold all enemys
enemy_list = pygame.sprite.Group()

enemy_missle_list = pygame.sprite.Group()
# This is a list of every sprite. All blocks and the player block as well.
# Having an extra group for all sprites makes it far easier to draw them
# all onto the screen.  In fact it's done by a single line of code(line 122)
all_sprites_list = pygame.sprite.Group()

# Create a player block
player = Player()
# Creates the background
bg = Background()
bg.create()
# Spawns enemies
spawner = Spawn()
spawner.asteroids()
# Upgrades
upgrade = Uprades()
# Loop until the user clicks the close button.
game = Game()
# The Database connection
conn = connection()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------------Opening Screen --------------
while len(playername) > 4:
    playername = raw_input('Type your name here to start the game (only 4 letters): ')
game.StartScreen()
# -------- Main Program Loop -----------
# We need to check out what happens when the player hits the space bar in order to "shoot".
# A new missile is created and gets it's initial position in the "middle" of the player.
# Then this missile is added to the missile sprite-group and also to the all_sprites group.

pygame.quit()
