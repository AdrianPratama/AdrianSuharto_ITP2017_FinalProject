import random
from pygame import *
from pygame.sprite import *
from template import receive
#import modules
#create Box Class for the Box player
class Box(Sprite):
    def __init__(self):#initialize the sprite
        Sprite.__init__(self)
        self.image= pygame.image.load("RedBox.png")#load the image
        self.rect = self.image.get_rect()#creates hitbox
        self.rect.left = self.rect.top = 60#initial position
    def moveRight(self):#move the box to the right
        self.rect.left += 2
    def moveLeft(self):#move the box to the left
        self.rect.left -= 2
    def moveUp(self):#move the box forward
        self.rect.top -= 2
    def moveDown(self):#move the box backward
        self.rect.top += 2

class Maze(Sprite):#makes the maze
    def __init__(self,grid):
        #initializes class as well as asking for input from the template.py
        Sprite.__init__(self)
        self.M = 19 #amount of the blocks at the row
        self.N = 13 #amount of the blocks at the column
        self.maze = grid #accepts parameter
    def create(self,surface,image): #creates the wall
        self.mazewall = Group()#groups the wall
        bx = 0#x axis of the blocks
        by = 0#y axis of the blocks
        for i in range(0,self.M*self.N):#ranges the amount of blocks need to be declared
            if self.maze[bx + (by*self.M)]== 1:#
                tempwall = MazeWall(bx*50,by*50)
                self.mazewall.add(tempwall)#adds wall for every row

            bx = bx+1
            if bx > self.M-1:#resets the x axis blocks to 0
                bx = 0
                by = by+1#goes to the next colum
        return self.mazewall

class Finish(Sprite):#creates the finish class
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("FinishBox.png").convert()#loads the class image
        self.rect = self.image.get_rect()#creates hitbox
        x = (850,550)
        y = (850,50)
        z = (50,550)
        rand = [x,y,z]#list of available position
        (self.rect.left,self.rect.top) = rand[random.randint(0,2)]#randomize the position

class MazeWall(Sprite):#class for the maze blocks
    def __init__(self,x,y):
        Sprite.__init__(self)
        self.image= pygame.image.load("YellowBox.png").convert()#load the image
        self.rect = self.image.get_rect()#creates hitbox
        self.rect.top = y
        self.rect.left = x

def text_object(text, font):#renders the font
    textSurface = font.render(text, True, (BLACK))
    return textSurface, textSurface.get_rect()

#main function
pygame.init()#initialize everything
display_width = 950
display_height = 650
display = pygame.display.set_mode((display_width,display_height),HWSURFACE,0)#initialize the window
BLACK = (0,0,0)#values for RGB
WHITE = (255,255,255)

def menu():#function for menu
    pygame.display.set_caption("Welcome to a-MAZE-ing World")#caption for the window
    apple = True
    while apple:
        largeText = pygame.font.Font(None, 80)#declares the font template
        textSurf, textRect = text_object("PRESS SPACE TO START", largeText)#asks for input
        textRect.center = ((display_width/2), (display_height/2))
        display.fill((WHITE))#refill the background with white
        display.blit(textSurf, textRect)#blits the window
        for events in pygame.event.get():
            keys = key.get_pressed()#gets the keys to check for input
            if events.type == pygame.QUIT:
                pygame.quit()
            if keys[K_SPACE]:
                apple = False
        pygame.display.flip()

def tryagain():#function for trying the game again
    apple = True
    while apple:
        largeText = pygame.font.Font(None, 60)
        textSurf, textRect = text_object("You win! Do you want to Continue?", largeText)
        textRect.center = ((display_width/2), (display_height/2))
        display.fill((WHITE))
        display.blit(textSurf, textRect)
        for events in pygame.event.get():
            keys = key.get_pressed()
            if keys[K_q]:#pressing q quits the game
                pygame,quit()
                quit()
            if keys[K_c]:#pressing c starts another game
                game()
            if events.type == pygame.QUIT:#pressing quit leaves the game
                pygame.quit()
        pygame.display.flip()

def lose():#function for trying the game
    apple = True
    pygame.mixer.music.load("glass.wav")#loads the sound of losing
    pygame.mixer.music.play()#plays it
    while apple:
        largeText = pygame.font.Font(None, 60)
        textSurf, textRect = text_object("You lose! Do you want to Continue?", largeText)
        textRect.center = ((display_width/2), (display_height/2))
        display.fill((WHITE))
        display.blit(textSurf, textRect)
        for events in pygame.event.get():
            keys = key.get_pressed()
            if keys[K_q]:
                pygame,quit()
                quit()
            if keys[K_c]:
                game()
            if events.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()

def game():#starting the game function
    pygame.mixer.music.load("Solution.wav")#loads the music for the game
    pygame.mixer.music.play(-1)#loops the game sound
    pygame.mixer.music.set_volume(1)#sets the volume
    running = True
    x = random.randint(0,4)#randomized number between 0-4
    y = receive()#receive the list
    z = y[x]#getting value of the randomized number and use it to get the list's value
    player = Box()#initialize box class
    maze = Maze(z)#initialize maze class using the template
    finish = Finish()#initialize finish class
    mazewallgroup = maze.create(display,image)#create maze
    sprites = Group(player)#grouping the sprite
    sprite = Group(finish)#grouping the sprite

    while running:
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            player.moveRight()
            if spritecollideany(player,mazewallgroup):
                lose()
        if keys[K_LEFT]:
            player.moveLeft()
            if spritecollideany(player,mazewallgroup):
                lose()
        if keys[K_UP]:
            player.moveUp()
            if spritecollideany(player,mazewallgroup):
                lose()
        if keys[K_DOWN]:
            player.moveDown()
            if spritecollideany(player,mazewallgroup):
                lose()
        if keys[K_ESCAPE]:
            running = False
        if spritecollideany(player,sprite):
            tryagain()
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
        pygame.event.pump()#get event
        display.fill(BLACK)
        sprites.draw(display)#display everything
        sprite.draw(display)
        mazewallgroup.draw(display)
        pygame.display.flip()

menu()
game()
