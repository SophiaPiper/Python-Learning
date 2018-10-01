import pygame
import time
import random

pygame.init()

## Color Settings
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

pause = False

## Display Settings
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Boats don\'t move like this!')
## Game Clock
clock = pygame.time.Clock()

## Load the boat image from file
boatImg = pygame.image.load('boat2.png')
boat_width = 25

pygame.display.set_icon(boatImg)

## Scoring function
def things_dodged(count):
	font = pygame.font.SysFont(None, 30)
	text = font.render('Dodged: ' +str(count), True, white)
	gameDisplay.blit(text, [20,20])

## Define the boat function and location
def boat(x,y):
	gameDisplay.blit(boatImg, (x,y))

## Define things to avoid
def things(thingx, thingy, thingw, thingh, color):
	pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

## Text Definitions
def text_objects(text, font):
	textSurf = font.render(text, True, black)
	return textSurf, textSurf.get_rect()
	game_loop()

def button(msg,x,y,w,h,ic,ac,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x + w > mouse[0] > x and y + 50 > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if click[0] == 1 and action != None:
			if action == "play":
				game_loop()
			if action == "quit":
				pygame.quit()
				quit()
			if action == "unpause":
				unpause()
	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
		
	smallText = pygame.font.Font("freesansbold.ttf",20)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ((x + (w/2)), (y + (h/2)))
	gameDisplay.blit(textSurf, textRect)


## Intro to the Game
def game_intro():
	intro = True

	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(white)
		largeText = pygame.font.Font('freesansbold.ttf', 90)
		TextSurf, TextRect = text_objects("It\'s a Boat Game", largeText)
		TextRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(TextSurf, TextRect)
					
		## Play Button
		button("Wavy",150,450,100,50,green,bright_green,"play")
		
		##Exit Button
		button("Quit",550,450,100,50,red,bright_red,"quit")
		
		pygame.display.update()
		clock.tick(15)

## Crash Function
def crash():
	largeText = pygame.font.Font('freesansbold.ttf', 90)
	TextSurf, TextRect = text_objects("You\'re Sunk", largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf, TextRect)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		## Replay Button
		button("Play Again",150,450,120,50,green,bright_green,"play")
		
		##Exit Button
		button("Quit",550,450,100,50,red,bright_red,"quit")
		
		pygame.display.update()
		clock.tick(15)

def paused():
	global pause
	#gameDisplay.fill(white)
	largeText = pygame.font.Font('freesansbold.ttf', 90)
	TextSurf, TextRect = text_objects("Paused", largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf, TextRect)

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		
		## Continue Button
		button("Continue",150,450,100,50,green,bright_green,"unpause")
		
		##Exit Button
		button("Quit",550,450,100,50,red,bright_red,"quit")
		
		pygame.display.update()
		clock.tick(15)

def unpause():
	global pause
	pause = False

## Game Loop Function
def game_loop():
	x = (display_width * 0.45)
	y = (display_height * 0.7)

	x_change = 0
	dodged = 0

	global pause

	## Start values for things to avoid
	thing_startx = random.randrange(0, display_width)
	thing_starty = -600
	thing_speed = 3
	thing_width = 75
	thing_height = 75

	## gameExit Default
	gameExit = False

	## Begin Loop
	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			### Key Presses
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -5
				if event.key == pygame.K_RIGHT:
					x_change = 5
				if event.key == pygame.K_p:
					pause = True
					paused()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0

		x += x_change
		
		## Draw the bg
		gameDisplay.fill(blue)
		## Start drawing objects
		things(thing_startx, thing_starty, thing_width, thing_height, red)
		thing_starty += thing_speed
		boat(x,y)
		things_dodged(dodged)

		## Game Logic
		#### Boundaries
		if x > display_width - boat_width or x < 0:
			crash()
		#### Repeating thingies
		if thing_starty > display_height:
			thing_starty = 0 - thing_height
			thing_startx = random.randrange(0, display_width)
			dodged += 1
			thing_speed += .5
			#thing_width += (dodged * 1.2)
		
		#### Crashing into thingies
		if y < thing_starty + thing_height:
			## print('y xover')

			if x > thing_startx and x < thing_startx + thing_width or x + boat_width > thing_startx and x + boat_width < thing_startx + thing_width:
				## print('x xover')
				crash()

		## Update the display, set tick
		pygame.display.update()
		clock.tick(60)

game_intro()

game_loop()

pygame.quit()
quit()