import pygame
from pygame.locals import *
import time
import random

SIZE = 40 #This is the size of the block 
BACKGROUND_COLOR = (110,110,5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert() # This command loads the apple image.
        self.x = 120
        self.y = 120 #Apple initial coordinates

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y)) # To print the image on window surface at given coordinates.
        pygame.display.flip() 

    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE
    # Function to move the apple at random positions after the collision.
    

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert() # This command loads the block image.
        self.direction = 'down' #This is default direction for the snake
        
        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'    
    # These are function to make the snake move by changing default directions.

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        # Here after each change in direction the blocks are changing there positions and going 1 position ahead.
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()
    # Here we are changing the direction by changing coordinates.

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i])) # To print the image on window surface at given coordinates.
        
        pygame.display.flip() 
        # For loop is being used to move the snake after each tiem counter. 
        #This functon is used while moving the block or snake as it fills the screen after each time it is called.

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    # Method to increase the length of the snake after eating the apple.

class Game:
    def __init__(self):
        pygame.init() # This initializes all the imported pygame modules.
        pygame.display.set_caption("Codebasics Snake And Apple Game") #To apply heading for the window when it opens.
        
        pygame.mixer.init() # This initializes all the music related imported pygame modules.
        self.play_background_music() #To play backgroyund music.
        
        self.surface=pygame.display.set_mode((1000,800))   # This opens a window or screen for display.The arguement in it is for the screen resolution of the window when it is opened.
        self.snake=Snake(self.surface) #Snake class being declared inside Game class and surface is given as its arguement 
        self.snake.draw() # Now whenever draw is called it will draw a snake on surface
        self.apple=Apple(self.surface)
        self.apple.draw() # Now whenever draw is called it will draw an apple on surface
    
    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1,0)
    # To apply the background music.

    def play_sound(self,sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")
        
        pygame.mixer.Sound.play(sound)
    # TO play the different sounds when apple is eaten or game is over.

    def reset(self):
        self.snake=Snake(self.surface)
        self.apple=Apple(self.surface)
    # TO reset the game when enter key is pressed.

    # Snake COlliding with apple.
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2+ SIZE:
            if y1 >= y2 and y1 < y2+ SIZE:
                return True    
        return False
    # Function to detect the collision between the head and the apple.

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))
    # To apply background image.

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake collliding with apple.
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding") #To apply ding sound whenever an apple is eaten.
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with itelf.
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash") #To apply crash song when the game is over.
                raise"Collision Occured"
    # function to call the methods to draw and move the snake and apple position.

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))
    # Method to display the total score of the game.

    def show_game_over(self):
        font = pygame.font.SysFont('arial',30)
        line1=font.render(f"Game is Over! Your Score is {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(200,300))
        line2=font.render(f"To play again press Enter.To exit press Escape!",True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.mixer.music.pause() #To pause the music when game is over.
        pygame.display.flip()
    # Displaying Game Over Message.
    
    def run(self):
        running=True 
        pause=False #It is used to freeze screen when game is over until any new command is given

        while running:
            for event in pygame.event.get():  # event.get() takes all the events as an input from user here.
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        running=False
                    if event.key==K_RETURN:
                        pygame.mixer.music.unpause()
                        pause=False
                    if not pause:
                        if event.key==K_UP:
                            self.snake.move_up()
                        if event.key==K_DOWN:
                            self.snake.move_down()
                        if event.key==K_LEFT:
                            self.snake.move_left()
                        if event.key==K_RIGHT:
                            self.snake.move_right() # These commands are being used to move the coordinates after the respective keys aur pressed.
                elif event.type==QUIT:
                    running=False  # Here our windows will close whenever cancel or escape button is clicked.
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()
            time.sleep(.3) # The snake will automatically move after each 0.2 seconds 


if __name__=="__main__":
    game=Game()
    game.run()