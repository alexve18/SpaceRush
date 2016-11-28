class Enemy(pygame.sprite.Sprite):
	xpos = 0								# defines the x spawn position
	ypos = 0								# defines the y spaw position
	xtarget = 0								# defines the x target position(the position the enemy is moving to)
	ytarget = 0								# defines the y target position
	fireRate = random.randrange(500,750)	# defines the space between fireing, lower number = more rapid fire
	moveSpeed = random.randrange(5)			# defines how many pixles the enemy moves per update
	onTarget = False						# defines if the enemy is on target




	"""docstring for enemy"""
	def __init__(self, arg):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_image
		self.rect = self.image.get_rect()




