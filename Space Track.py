#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Justin Chun
#
# Created:     06-05-2019
# Copyright:   (c) Justin Chun 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()

import pygame
from pygame.locals import *
import random
pygame.init()

# Colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
subred = (194,36,36)

# Screen Dimensions
width = 375
height = 600

# Done variables for stopping main loops of several functions for displaying different screens
doneinst = False
donestart = False
donecred = False
doneover = False
donecom = False
donestop = False
player = None
powerstat = False

# Variable to determine the level which the player is at
global levelcount
levelcount = 0

# Background image for the main gameplay
space = pygame.image.load('Space.png')

# Initializing the sounds necessary for the game
one = pygame.mixer.Sound('Audio\BGM1.wav')
three = pygame.mixer.Sound('Audio\BGM.wav')
playerdeath = pygame.mixer.Sound('Audio\playerdeath.wav')
completed = pygame.mixer.Sound('Audio\complete.wav')

'''Classes for objects necessary throughout the game'''

class heart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('heart.png').convert_alpha(), (30, 30))

        self.rect = self.image.get_rect()

        # Instance variables that control the edges of where we bounce
        self.top = 0
        self.bottom = 0

        # Instance variables for animation
        self.changey = 0

    def update(self, kill):
        self.rect.y += self.changey

        if kill:
            self.kill()

class power(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('power.png').convert_alpha(), (30, 30))

        self.rect = self.image.get_rect()

        # Instance variables that control the edges of where we bounce
        self.top = 0
        self.bottom = 0

        # Instance variables for animation
        self.changey = 0

    def update(self, kill):
        self.rect.y += self.changey

        if kill:
            self.kill()

# Player Object
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        # Calling Parent's Constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.transform.scale(pygame.image.load('spaceship.png').convert_alpha(), (55, 67))

        # Make our top-left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector
        self.changex = 0
        self.changey = 0
        self.walls = None

    def changespeed(self,x,y):
        # Changing the speed of the player
        self.changex += x
        self.changey += y

    def update(self, kill):
        # Updating the player's position
        self.rect.x += self.changex

        # Checking if it hit  the wall or not
        block_hit_list = pygame.sprite.spritecollide(self,self.walls,False)
        for block in block_hit_list:
            if self.changex > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        # Moving up or down
        self.rect.y += self.changey

        # Check and see if player hits anything
        block_hit_list = pygame.sprite.spritecollide(self,self.walls,False)
        for block in block_hit_list:
            # Reset the position based on the top/bottom of the object.
            if self.changey > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        if kill:
            self.kill()

# Bullet shot from the player
class bullet(pygame.sprite.Sprite):
    def __init__(self):
        # Calling the parent constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('Bullet.png').convert_alpha(), (8,28))

        self.rect = self.image.get_rect()

    def update(self, kill):
        # Moving the bullet, or changing the location of the bullet
        self.rect.y -= 9

        if kill:
            self.kill()

# Powered bullet shot from the player
class pbullet(pygame.sprite.Sprite):
    def __init__(self):
        # Calling the parent constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('pbullet.png').convert_alpha(), (40,30))

        self.rect = self.image.get_rect()

    def update(self, kill):
        # Moving the powered bullet, or changing the location of the powered bullet
        self.rect.y -= 9

        if kill:
            self.kill()

# Interactive enemy with the player
class enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (30, 30))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(45,335)
        self.rect.y = random.randrange(-100,0)

        # Instance variables that control the edges of where we bounce
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

        # Instance variables for our current speed and direction
        self.changex = 0
        self.changey = 0

    def update(self, kill):
        self.changey = 1
        self.rect.y += self.changey

        if self.rect.bottom >= self.bottom or self.rect.top <= self.top:
            self.changey *= -1

        if kill:
            self.kill()

# Class for different enemy
class enemy1(pygame.sprite.Sprite):
    def __init__(self):
        # Initializing several variables for location and animation
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('enemy1.png').convert_alpha(), (30, 30))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(45,335)
        self.rect.y = random.randrange(-100,0)

        # Instance variables that control the edges of where we bounce
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

        # Instance variables for our current speed and direction
        self.changex = 0
        self.changey = 0

    # Function to update the status of enemy1
    def update(self, kill):
        self.changey = 1
        self.rect.y += self.changey

        if self.rect.bottom >= self.bottom or self.rect.top <= self.top:
            self.changey *= -1

        if kill:
            self.kill()

# Wall the player can run into
class wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Making an invisible wall, with specified size
        self.image = pygame.Surface([width, height])
        self.image.fill(white)

        # Make top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

'''Functions to display different screens'''

# Main Menu
def start():
    # Storing background image in a variable
    background = pygame.image.load('mainscreen.png')

    # Setting the screen
    size = (width, height)
    screen = pygame.display.set_mode(size)

    # Initializing whatever is necessary
    pygame.init()
    font = pygame.font.SysFont('Calibri', 50, True, False)
    subfont = pygame.font.SysFont('Bookman', 35, True, False)

    # Calling the done variables
    global doneinst
    global donestart
    global donecred
    global doneover

    # Main loop for mechanics of the page, pressing buttons
    while not donestart:
        for event in pygame.event.get():
            #In case user force closes the screen
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()
                # Starting the game
                if 25 <= posx <= 345 and 370 <= posy <= 435:
                    donestart = True
                    doneinst = True
                    donecred = True
                # Instruction Screen
                elif 25 <= posx <= 345 and 445 <= posy <= 510:
                    instruction()
                # Credits Screen
                elif 25 <= posx <= 345 and 520 <= posy <= 585:
                    credits()

        # Use of graphics for showing buttons and background image
        screen.blit(background, [0,0])

        pygame.draw.rect(screen,white,[25,370,320,65])
        pygame.draw.rect(screen,black,[25,370,320,65],2)
        text = subfont.render("Start Game", True, black)
        screen.blit(text, [110,390])

        pygame.draw.rect(screen,white,[25,445,320,65])
        pygame.draw.rect(screen,black,[25,445,320,65],2)
        text = subfont.render("Instruction", True, black)
        screen.blit(text, [115,465])

        pygame.draw.rect(screen,white,[25,520,320,65])
        pygame.draw.rect(screen,black,[25,520,320,65],2)
        text = subfont.render("Credits", True, black)
        screen.blit(text, [135,540])

        text = font.render("Space Track", True, black)
        screen.blit(text, [35,45])

        pygame.draw.rect(screen,black,[25,40,265,60],2)

        pygame.display.flip()

# Function for instruction screen
def instruction():

    # Setting the screen
    background = pygame.image.load('mainscreen.png')
    size = (width, height)
    screen = pygame.display.set_mode(size)

    # Initializing whatever is necessary
    pygame.init()
    mainfont = pygame.font.Font(None, 37)
    subfont = pygame.font.Font(None, 23)

    # Calling the done variables
    global donestart
    global doneinst
    global donecred

    # Main loop to allow user to decide to go back to main menu
    while not doneinst:
        for event in pygame.event.get():

            # In case user force closes the screen
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # For exiting the instruction page, assigning value to the buttons
                posx, posy = pygame.mouse.get_pos()
                if 0 <= posx <= width and 0 <= posy <= height:
                    start()

        screen.blit(background, [0,0])

        pygame.draw.rect(screen, white, [5,10,365,585])
        pygame.draw.rect(screen, black, [5,10,365,585],2)

        # Components necessary for instruction screen
        text = mainfont.render("Instructions", True, black)
        screen.blit(text, [105,20])

        text = subfont.render("* Your main goal is to kill all the enemies!", True, black)
        screen.blit(text, [10,65])

        text = subfont.render("* You can move around by using arrowkeys", True, black)
        screen.blit(text, [10,105])
        text = subfont.render("   on your keyboard.", True, black)
        screen.blit(text, [10,125])

        text = subfont.render("* You start with three lives, you can extend", True, black)
        screen.blit(text, [10,165])
        text = subfont.render("  them throughout the game by collecting", True, black)
        screen.blit(text, [10,185])
        text = subfont.render("  them.", True, black)
        screen.blit(text, [10,205])

        text = subfont.render("* Press spacebar to shoot at enemies when", True, black)
        screen.blit(text, [10,245])
        text = subfont.render("  your spaceship aligns with the location of the", True, black)
        screen.blit(text, [10,265])
        text = subfont.render("  enemy.", True, black)
        screen.blit(text, [10,285])

        text = subfont.render("* Be sure not to collide with enemy, as it would", True, black)
        screen.blit(text, [10,325])
        text = subfont.render("  make your spaceship explode.", True, black)
        screen.blit(text, [10,345])

        text = subfont.render("* Also, be mindful that once the enemy passes", True, black)
        screen.blit(text, [10,385])
        text = subfont.render("  you and reach the end of the screen, you lose.", True, black)
        screen.blit(text, [10,405])

        text = subfont.render("Click anywhere to continue...", True, black)
        screen.blit(text, [140,570])

        pygame.display.flip()

# Function for credits screen
def credits():

    # Setting the screen
    background = pygame.image.load('mainscreen.png')
    size = (width, height)
    screen = pygame.display.set_mode(size)

    # Initializing whatever is necessary
    pygame.init()
    mainfont = pygame.font.Font(None, 37)
    subfont = pygame.font.Font(None, 23)

    # Calling done variables
    global doneinst
    global donestart
    global donecred

    while not donecred:
        for event in pygame.event.get():
            # In case user force closes the screen
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()
                # For exiting the credit page
                if 0 <= posx <= width and 0 <= posy <= height:
                    start()

        # Key components for showing list of people or things to give credits to
        screen.blit(background, [0,0])

        pygame.draw.rect(screen, white, [5,10,365,585])
        pygame.draw.rect(screen, black, [5,10,365,585],2)

        text = mainfont.render("Credits", True, black)
        screen.blit(text, [140, 20])

        text = subfont.render("Game developed by:", True, black)
        screen.blit(text, [105, 65])
        text = subfont.render("Justin Chun", True, black)
        screen.blit(text, [135, 85])

        text = subfont.render("Sprite Template Provided by:", True, black)
        screen.blit(text, [72, 125])
        text = subfont.render("shutterstock.com", True, black)
        screen.blit(text,[115,145])

        text = subfont.render("Created on Dell Inspiron", True, black)
        screen.blit(text, [95, 185])

        text = subfont.render("Special Thanks to:", True, black)
        screen.blit(text, [120, 225])
        text = subfont.render("Jeremy, Roman", True, black)
        screen.blit(text, [130, 245])

        text = subfont.render("Click anywhere to continue...", True, black)
        screen.blit(text, [140, 570])

        pygame.display.flip()

# Function for displaying screen when the user has died
def gameover():
    backgroundend = pygame.image.load('explosion.png')

    # Conditionals to check where the user died at, and determining which music to stop
    if levelcount == 1 or levelcount == 2:
        one.stop()

    elif levelcount == 3:
        three.stop()

    # Sound dedicated when the user loses
    playerdeath.play()

    size = (width, height)
    screen = pygame.display.set_mode(size)
    global doneover

    pygame.init()

    # Necessary formats for words
    font = pygame.font.SysFont('Calibri', 50, True, False)
    subfont = pygame.font.SysFont('Calibri', 25, True, False)
    button = pygame.font.SysFont('Bookman', 35, True, False)

    clock = pygame.time.Clock()

    # Main program loop
    while not doneover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()
                '''For choosing whether to play again or quit the game'''
                # Choosing to play again
                if 25 <= posx <= 345 and 435 <= posy <= 505:
                    all_sprite_list.update(True)
                    enemy_list.update(True)
                    enemy1_list.update(True)

                    # Determining which level to go to depending on which level player died at
                    if levelcount == 1:
                        levelcount == 1
                        level1()

                    elif levelcount == 2:
                        levelcount == 2
                        level2()

                    elif levelcount == 3:
                        levelcount = 3
                        level3()

                # Choosing to quit the game
                elif 25 <= posx <= 345 and 515 <= posy <= 585:
                    doneover = True
                    pygame.quit()

        # Key components for Game Over screen
        screen.blit(backgroundend, [0,0])

        text = font.render("Mission Failed!", True, white)
        screen.blit(text, [35, 45])

        text = subfont.render("Try Again?", True, white)
        screen.blit(text, [130, 100])

        pygame.draw.rect(screen,white,[25,435,320,70])
        pygame.draw.rect(screen,black,[25,435,320,70],2)
        text = button.render("Try Again", True, black)
        screen.blit(text, [122, 460])

        pygame.draw.rect(screen,white,[25,515,320,70])
        pygame.draw.rect(screen,black,[25,515,320,70],2)
        text = button.render("Quit Game", True, black)
        screen.blit(text, [115, 537])

        pygame.display.flip()

# Screen when user completes a level
def complete():
    backgroundcom = pygame.image.load('complete.png')

    # Conditionals to see which level user completed from, and stopping the music accordingly
    if levelcount == 1 or levelcount == 2:
        one.stop()
    elif levelcount == 3:
        three.stop()

    # Playing music dedicated for a situation which the user has won
    completed.play()

    # Setting the screen, calling done variables
    size = (width, height)
    screen = pygame.display.set_mode(size)
    global donecom

    pygame.init()

    # Storing necessary fonts and sizes for the texts
    font = pygame.font.SysFont('Calibri', 40, True, False)
    subfont = pygame.font.SysFont('Calibri', 25, True, False)
    button = pygame.font.SysFont('Bookman', 35, True, False)

    clock = pygame.time.Clock()

    # Main program loop
    while not donecom:
        for event in pygame.event.get():
            # In case the user force closes the game
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()
                '''For choosing whether to play again or quit the game'''
                # Choosing to play again
                if 25 <= posx <= 345 and 435 <= posy <= 505:
                    all_sprite_list.update(True)
                    enemy_list.update(True)

                    # Determining which level to go to
                    if levelcount == 1:
                        level2()

                    elif levelcount == 2:
                        level3()

                # Choosing to quit the game
                elif 25 <= posx <= 345 and 515 <= posy <= 585:
                    donecom = True
                    pygame.quit()

        screen.blit(backgroundcom, [0,0])

        # Setting key components for the completion screen
        text = font.render("Mission Completed!", True, white)
        screen.blit(text, [26, 45])

        text = subfont.render("Proceed to Next Mission?", True, white)
        screen.blit(text, [52, 100])

        pygame.draw.rect(screen,white,[25,435,320,70])
        pygame.draw.rect(screen,black,[25,435,320,70],2)
        text = button.render("Proceed", True, black)
        screen.blit(text, [130, 460])

        pygame.draw.rect(screen,white,[25,515,320,70])
        pygame.draw.rect(screen,black,[25,515,320,70],2)
        text = button.render("Quit Game", True, black)
        screen.blit(text, [115, 537])

        pygame.display.flip()

# When the user is out of lives to continue the game
def stop():
    backgroundstop = pygame.image.load('end.png')
    backgroundstop = pygame.transform.scale(backgroundstop, [375,440])

    # Conditionals to check which level user died from, and stopping the music accordingly
    if levelcount == 1 or levelcount == 2:
        one.stop()
    elif levelcount == 3:
        three.stop()

    # Sound effect played when the user dies
    playerdeath.play()

    # Setting the screen, calling done variables for stop screen
    size = (width, height)
    screen = pygame.display.set_mode(size)
    global donestop

    pygame.init()

    font = pygame.font.SysFont('Calibri', 40, True, False)
    subfont = pygame.font.SysFont('Calibri', 23, True, False)
    button = pygame.font.SysFont('Bookman', 35, True, False)

    clock = pygame.time.Clock()

    # Main program loop
    while not donestop:
        for event in pygame.event.get():
            # In case the user forces closes the game
            if event.type == pygame.QUIT:
                pygame.quit()
            # Button down mechanism
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()

                # Choosing to quit the game
                if 25 <= posx <= 345 and 515 <= posy <= 585:
                    donestop = True
                    pygame.quit()

        screen.blit(backgroundstop, [0,0])

        # Key components for this screen
        text = subfont.render("You couldn't protect the galaxy...", True, white)
        screen.blit(text, [35, 460])

        pygame.draw.rect(screen,white,[25,515,320,70])
        pygame.draw.rect(screen,black,[25,515,320,70],2)
        text = button.render("Quit Game", True, black)
        screen.blit(text, [115, 537])

        pygame.display.flip()

# Which the user completes the whole game
def end():
    backgroundcom = pygame.image.load('end1.png')
    backgroundcom = pygame.transform.scale(backgroundcom, [580,440])

    if levelcount == 3:
        three.stop()

    size = (width, height)
    screen = pygame.display.set_mode(size)
    donecom = False

    pygame.init()

    subfont = pygame.font.SysFont('Calibri', 19, True, False)
    button = pygame.font.SysFont('Bookman', 35, True, False)

    clock = pygame.time.Clock()

    # Main program loop
    while not donecom:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()

                # Choosing to quit the game
                if 25 <= posx <= 345 and 515 <= posy <= 585:
                    donestop = True
                    pygame.quit()

        screen.blit(backgroundcom, [0,0])

        # Key components for the completion screen
        text = subfont.render("You have succesfully protected the galaxy!", True, white)
        screen.blit(text, [18, 460])

        pygame.draw.rect(screen,white,[25,515,320,70])
        pygame.draw.rect(screen,black,[25,515,320,70],2)
        text = button.render("Quit Game", True, black)
        screen.blit(text, [115, 537])

        pygame.display.flip()


# Call this function so the Pygame library can initialize ifself
pygame.init()

# Create a screen
screen = pygame.display.set_mode([width, height])

# Set the title of the window
pygame.display.set_caption("Space Track")

# Lists for various purposes
all_sprite_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
heart_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
enemy1_list = pygame.sprite.Group()
power_list = pygame.sprite.Group()
pbullet_list = pygame.sprite.Group()

# Initializing necessary variables
lives = 3
kills = 0
dead = True

# Make the wall around the screen
wall_list = pygame.sprite.Group()

Wall = wall(0,0,5,600)
wall_list.add(Wall)
all_sprite_list.add(Wall)

Wall = wall(0,0,375,5)
wall_list.add(Wall)
all_sprite_list.add(Wall)

Wall = wall(370,0,5,600)
wall_list.add(Wall)
all_sprite_list.add(Wall)

Wall = wall(0,595,375,5)
wall_list.add(Wall)
all_sprite_list.add(Wall)

clock = pygame.time.Clock()

# Initializing the font
button = pygame.font.SysFont('Bookman', 35, True, False)

# Main Program Loop
def level1():
    global dead
    global lives
    global kills
    global player
    done = False
    counter = 0

    # Indication of level
    levelcount = 1

    if dead:
        start()
        dead = False

    # Setting the number of enemies
    for i in range(7):
        Enemy = enemy()
        enemy_list.add(Enemy)

    # Creating player object
    player = Player(145, 500)
    player.walls = wall_list

    all_sprite_list.add(player)

    # Repeating the background music
    one.play(-1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True

            # Control Mechanism
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-4, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(4, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, -4)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, 4)
                elif event.key == pygame.K_SPACE:
                    # Fires bullet when spacebar is pressed
                    Bullet = bullet()
                    # Set the bullet at where the player is
                    Bullet.rect.x = player.rect.x+23
                    Bullet.rect.y = player.rect.y-6
                    # Add the bullet to the list
                    all_sprite_list.add(Bullet)
                    bullet_list.add(Bullet)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(4, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(-4, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, 4)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, -4)

        for Heart in heart_list:
            # Checks if the heart is obtained by player
            hearts_hit_list = pygame.sprite.spritecollide(player,heart_list,True)
            for Heart in hearts_hit_list:
                lives += 1
                print(lives)

        for Bullet in bullet_list:
            # Checks if the bullet hits the enemy
            bullet_hit_list = pygame.sprite.spritecollide(Bullet,enemy_list,True)

            # When the bullet hits the enemy, remove the bullet and increase kill count
            for i in bullet_hit_list:
                bullet_list.remove(Bullet)
                all_sprite_list.remove(Bullet)
                kills += 1
                counter += 1

        for Enemy in enemy_list:
            # Checks if the enemy collides with the player
            enemy_hit_list = pygame.sprite.spritecollide(player,enemy_list,True)

            # When the enemy collides, remove enemy and player, decrease life count
            for Enemy in enemy_hit_list:
                enemy_list.remove(Enemy)
                all_sprite_list.remove(Enemy)
                lives -= 1
                kills = 0
                print(lives)

                # Checking the number of lives which the player has
                if lives  == 0:
                    stop()
                else:
                    levelcount = 1
                    gameover()

        # Losing the game when enemy reaches the end of the screen
        if Enemy.rect.y == (height + 1):
            lives -= 1
            if lives == 0:
                stop()
            else:
                levelcount = 1
                gameover()

        # Completing the level by killing all enemies
        if kills == 7:
            kills = 0
            complete()

        all_sprite_list.update(False)

        screen.blit(space, [0,0])

        # Updating the sprites on the level
        all_sprite_list.update(False)
        all_sprite_list.draw(screen)
        enemy_list.update(False)
        enemy_list.draw(screen)

        # Showing the number of lives which the player has
        screen.blit(button.render("Lives: ", True, white), (230,35))
        text = button.render(lives.__str__(), True, white)
        screen.blit(text, [320,35])

        clock.tick(60)

        pygame.display.flip()

def level2():
    global dead
    global lives
    global kills
    global player
    done = False
    counter = 0

    # Indication of the level
    levelcount = 2

    if dead:
        start()
        dead = False

    # Setting the number of enemies on the screen
    for i in range(15):
        Enemy = enemy()
        enemy_list.add(Enemy)

    # Creating player object
    player = Player(145, 500)
    player.walls = wall_list

    all_sprite_list.add(player)

    #Repeating the background music
    one.play(-1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True

            # Control mechanism
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-4, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(4, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, -4)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, 4)
                elif event.key == pygame.K_SPACE:
                    # Fires bullet when spacebar is pressed
                    Bullet = bullet()
                    # Set the bullet at where the player is
                    Bullet.rect.x = player.rect.x+23
                    Bullet.rect.y = player.rect.y-6
                    # Add the bullet to the list
                    all_sprite_list.add(Bullet)
                    bullet_list.add(Bullet)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(4, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(-4, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, 4)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, -4)

        for Heart in heart_list:
            # Checks if the heart is obtained by player
            hearts_hit_list = pygame.sprite.spritecollide(player,heart_list,True)
            for Heart in hearts_hit_list:
                lives += 1
                print(lives)

        for Bullet in bullet_list:
            # Checks if the bullet hits the enemy
            bullet_hit_list = pygame.sprite.spritecollide(Bullet,enemy_list,True)

            # When the bullet hits the enemy, remove the bullet and increase kill count
            for i in bullet_hit_list:
                bullet_list.remove(Bullet)
                all_sprite_list.remove(Bullet)
                kills += 1
                counter += 1

                if counter >= 8:
                    # Representing heart object
                    Heart = heart()

                    Heart.rect.x = random.randrange(45,335)
                    Heart.rect.y = 0

                    Heart.changey = 3
                    Heart.top = 0
                    Heart.bottom = height

                    # Add the block to the list of objects
                    heart_list.add(Heart)
                    all_sprite_list.add(Heart)

                    counter = 0

        for Enemy in enemy_list:
            # Checks if the enemy collides with the player
            enemy_hit_list = pygame.sprite.spritecollide(player,enemy_list,True)

            # When the enemy collides, remove enemy and player, decrease life count
            for Enemy in enemy_hit_list:
                enemy_list.remove(Enemy)
                all_sprite_list.remove(Enemy)
                lives -= 1
                kills = 0
                print(lives)

                # Checking the number of lives which the player has
                if lives  == 0:
                    stop()
                else:
                    levelcount = 2
                    gameover()

        # Losing when enemies reach the end of the screen
        if Enemy.rect.y == (height + 1):
            lives -= 1
            if lives == 0:
                stop()
            else:
                levelcount = 2
                gameover()

        # Completing the level when all enemies are killed
        if kills == 15:
            kills = 0
            complete()

        all_sprite_list.update(False)

        screen.blit(space, [0,0])

        # Updating the sprites on the level
        all_sprite_list.update(False)
        all_sprite_list.draw(screen)
        enemy_list.update(False)
        enemy_list.draw(screen)

        # Showing number of lives which the player has
        screen.blit(button.render("Lives: ", True, white), (230,35))
        text = button.render(lives.__str__(), True, white)
        screen.blit(text, [320,35])

        clock.tick(60)

        pygame.display.flip()

def level3():
    global dead
    global lives
    global kills
    global player
    global powerstat
    done = False
    counter = 0
    heartcount = 0

    # Indication of which level player is playing at
    levelcount = 3

    if dead:
        start()
        dead = False

    # Setting the number of enemies on the screen
    for i in range(16):
        Enemy = enemy()
        enemy_list.add(Enemy)

    for n in range(14):
        Enemy1 = enemy1()
        enemy1_list.add(Enemy1)

    # Creating player object
    player = Player(145, 500)
    player.walls = wall_list

    all_sprite_list.add(player)

    # Repeating the background music
    three.play(-1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True

            # Control mechanism
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-4, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(4, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, -4)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, 4)
                elif event.key == pygame.K_SPACE:
                    # Checking if player has gained power-up
                    if powerstat == False:
                        # Fires bullet when spacebar is pressed
                        Bullet = bullet()
                        # Set the bullet at where the player is
                        Bullet.rect.x = player.rect.x+23
                        Bullet.rect.y = player.rect.y-6
                        # Add the bullet to the list
                        all_sprite_list.add(Bullet)
                        bullet_list.add(Bullet)

                    elif powerstat == True:
                        # Fires bullet when spacebar is pressed
                        Pbullet = pbullet()
                        # Set the bullet at where the player is
                        Pbullet.rect.x = player.rect.x+8
                        Pbullet.rect.y = player.rect.y-6
                        # Add the bullet to the list
                        all_sprite_list.add(Pbullet)
                        pbullet_list.add(Pbullet)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(4, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(-4, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, 4)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, -4)

        for Heart in heart_list:
            # Checks if the heart is obtained by player
            hearts_hit_list = pygame.sprite.spritecollide(player,heart_list,True)
            for Heart in hearts_hit_list:
                lives += 1
                print(lives)

        for Power in power_list:
            # Checks if the power-up is obtained by player
            power_hit_list = pygame.sprite.spritecollide(player,power_list,True)
            for Power in power_hit_list:
                powerstat = True

        for Bullet in bullet_list:
            # Checks if the bullet hits the enemy
            bullet_hit_list = pygame.sprite.spritecollide(Bullet,enemy_list,True)

            # When the bullet hits the enemy, remove the bullet and increase kill count
            for i in bullet_hit_list:
                bullet_list.remove(Bullet)
                all_sprite_list.remove(Bullet)
                kills += 1
                counter += 1
                heartcount += 1
                print(kills)

        for Bullet in bullet_list:
            # Checks if the bullet hits the enemy
            bullet_hit_list = pygame.sprite.spritecollide(Bullet,enemy1_list,True)

            # When the bullet hits the enemy, remove the bullet and increase kill count
            for i in bullet_hit_list:
                bullet_list.remove(Bullet)
                all_sprite_list.remove(Bullet)
                kills += 1
                counter += 1
                heartcount += 1
                print(kills)

        for Enemy in enemy_list:
            # Checks if the enemy collides with the player
            enemy_hit_list = pygame.sprite.spritecollide(player,enemy_list,True)

            # When the enemy collides, remove enemy and player, decrease life count
            for Enemy in enemy_hit_list:
                enemy_list.remove(Enemy)
                all_sprite_list.remove(Enemy)
                lives -= 1
                kills = 0
                print(lives)

                # Checking the number of lives which the player has
                if lives  == 0:
                    stop()
                else:
                    levelcount = 3
                    gameover()

        for Enemy1 in enemy1_list:
            # Checks if the enemy collides with the player
            enemy_hit_list = pygame.sprite.spritecollide(player,enemy1_list,True)

            # When the enemy collides, remove enemy and player, decrease life count
            for Enemy1 in enemy_hit_list:
                enemy1_list.remove(Enemy1)
                all_sprite_list.remove(Enemy1)
                lives -= 1
                kills = 0
                print(lives)

                # Checking the number of lives which the player has
                if lives  == 0:
                    stop()
                else:
                    levelcount = 3
                    gameover()

        # Losing when the enemies reach the end of the screen
        if Enemy.rect.y == (height + 1):
            lives -= 1
            if lives == 0:
                stop()
            else:
                levelcount = 3
                gameover()

        if Enemy1.rect.y == (height + 1):
            lives -= 1
            if lives == 0:
                stop()
            else:
                levelcount = 3
                gameover()

        # Checking if the player has gained power-up, then changing the bullet type
        if powerstat == True:
            for Pbullet in pbullet_list:
                # Checks if the powered bullet hits the enemy
                pbullet_hit_list = pygame.sprite.spritecollide(Pbullet,enemy_list,True)

                # When the powered bullet hits the enemy, remove the bullet and increase kill count
                for i in pbullet_hit_list:
                    pbullet_list.remove(Pbullet)
                    all_sprite_list.remove(Pbullet)
                    kills += 1
                    print(kills)

            for Pbullet in pbullet_list:
                # Checks if the powered bullet hits the enemy
                pbullet_hit_list = pygame.sprite.spritecollide(Pbullet,enemy1_list,True)

                # When the powered bullet hits the enemy, remove the bullet and increase kill count
                for i in pbullet_hit_list:
                    pbullet_list.remove(Pbullet)
                    all_sprite_list.remove(Pbullet)
                    kills += 1
                    print(kills)

        # Dropping heart or power-up after the player gains specific amount of kills
        if counter >= 11:
            # Representing power-up object
            Power = power()

            Power.rect.x = random.randrange(45,335)
            Power.rect.y = 0

            Power.changey = 3
            Power.top = 0
            Power.bottom = height

            # Add the block to the list of objects
            power_list.add(Power)
            all_sprite_list.add(Power)

            counter = 0

        if heartcount >= 8:
            # Representing heart object
            Heart = heart()

            Heart.rect.x = random.randrange(45,335)
            Heart.rect.y = 0

            Heart.changey = 3
            Heart.top = 0
            Heart.bottom = height

            # Add the block to the list of objects
            heart_list.add(Heart)
            all_sprite_list.add(Heart)

            heartcount = 0

        # Ending the game when player kills all enemies given on the screen
        if kills == 30:
            kills = 0
            end()

        all_sprite_list.update(False)

        screen.blit(space, [0,0])

        # Updating all sprites on the level
        all_sprite_list.update(False)
        all_sprite_list.draw(screen)
        enemy_list.update(False)
        enemy_list.draw(screen)
        enemy1_list.update(False)
        enemy1_list.draw(screen)

        # Showing the number of lives
        screen.blit(button.render("Lives: ", True, white), (230,35))
        text = button.render(lives.__str__(), True, white)
        screen.blit(text, [320,35])

        clock.tick(60)

        pygame.display.flip()

level1()
level2()
level3()

pygame.quit()