#in oop concept how many use objects create class for each object like apple,snake...

import pygame
from pygame.locals import *  #from pygame.constants import KEYDOWN, QUIT this is constants in pygame
import time 
import random

SIZE = 40 #size of block
BACKGROUND_COLOR = 7, 87, 28

class Apple:
    def __init__(self, parent_screen):
        self.image=pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen=parent_screen #draw apple on screen
        self.x =120 #self.x = SIZE*3   #position for apple
        self.y =120  #self.y = SIZE*3
    
    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()
        
    def move(self):
        self.x = random.randint(1,24)*SIZE  #(1000-40=25) from 1 to 25*40 random value generate 1000->width of screen window not write 0 to 25*40 bcoz use from 0 get out of window
        self.y = random.randint(1,19)*SIZE  
        


class Snake: #for block using block create snake
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen #background screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        
        self.length = 1 #for number of blocks to create snake
        self.x = [40]     #self.x =[SIZE]*length #create empty array to store values of length ex-[34]*3=[34,34,34]
        self.y = [40]   #self.y = [SIZE]*length
        
    
    def move_up(self):
         self.direction = 'up' 
        #self.draw() #call draw() function because update x,y value and draw on window
        
    def move_down(self):
         self.direction = 'down' 
        #self.draw()
        
    def move_left(self):
        self.direction = 'left' 
        #self.draw()
    
    def move_right(self):
         self.direction = 'right' 
         #self.draw()
         
    def walk(self):
        #update body
        for i in range(self.length-1,0,-1):#(-1,0,-1)->-1-minus 1 from length,upto 0 means 1,-1->for reverse=all other bocks shifted previous block position of block means move (reverse-2 become 1 ,3 become 2 ...like)for loop work 5,4,3,2,1..
            self.x[i] = self.x[i-1] #current x postion shoud be previous block position
            self.y[i] = self.y[i-1]
        
        
        #update head
        if self.direction == 'left':
            self.x[0]-= SIZE #when we press left reduce x-axis value by SIZE is 40  pixel x[0]->head of snake block is on 0 position distance betwwen 2 blocks shoud be SIZE=40 pixel
        elif self.direction == 'right':
            self.x[0] += SIZE  #when we press right increase x-axis value by 10 pixel
        elif self.direction == 'up':
            self.y[0] -= SIZE  #when we press up key then only change y-axis value but x-axis is constant reduce y-axis by 10 pixel
        elif self.direction == 'down':
            self.y[0] += SIZE  #when we press up key then only change x-axis value but y-axis is constant(increase y-axis by 10 pixel)
            
        self.draw()  
        
        
    def draw(self):
            #self.parent_screen.fill(BACKGROUND_COLOR) #set background color for pygame window #call this method again to remove before  called all block and again fill with same color means only show current position of block
        
        for i in range(self.length): #use for loop because us multiple x,y axis(dimention)
            self.parent_screen.blit(self.image,(self.x[i],self.y[i]))# use to draw block on surface on x-axis=100,y-axis=100
        pygame.display.flip()  #if any changes do in window using this method we sow this changes on window(important method)
     
        
    
    def increase_length(self):
        self.length+=1 #increment of snake length
        self.x.append(-1)  #if increment of x & y value then store new value so need array and x&y work as array to store incremented length value
        self.y.append(-1)
    
   

class Game:
    def __init__(self): #constructor
       pygame.init() #pygame module initialize
       pygame.display.set_caption("Codebasics Snake And Apple Game")
       pygame.mixer.init() #to include sound
       
       self.play_background_music() #play bgsound when game start
       
       self.surface=pygame.display.set_mode((1000,800)) #pygame display window (height,width) main window for game (parent screen)
       self.snake = Snake(self.surface) #create snake class object and create member of game class (surface->parent screen pass to snake class) 1 is length of blocks which is pass to snake class
       self.snake.draw() #draw snake
       self.apple = Apple(self.surface)
       self.apple.draw()
       
    def reset(self):
        self.snake = Snake(self.surface) #reset snake with 1 and apple 
        self.apple = Apple(self.surface)
       
    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 <x2 +SIZE:
            if y1 >=y2 and y1 <y2 + SIZE:
                return True
            
        return False
    
    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3") #use music because use long music play background music
        pygame.mixer.music.play(-1,0)
    
    
    def render_background(self):
        bg=pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))
    

    def play_sound(self,sound_name):
        
        if sound_name == "crash":
            sound = pygame.mixer.Sound(f"resources/crash.mp3") #play sound after snake eat apple #use pygame.mixer.Sound->use sound because 1 time play short sound
        elif sound_name == "ding":
            sound = pygame.mixer.Sound(f"resources/ding.mp3")
        pygame.mixer.Sound.play(sound)
        #pygame.mixer.sound.stop()
        
       
    def play(self):
        self.render_background()
        self.snake.walk() #call snake block automatic walk this snakeblock every 0.2sec   
        self.apple.draw()  #if not write walf function call fill screen then fill screen not draw apple
        self.display_score()
        pygame.display.flip()
        
        # snake eating apple scenario
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y): #need only snake head position use x[0],y[0] & apple position x,y
            #print("collision")
             self.play_sound("ding")
             self.snake.increase_length()
             self.apple.move()
           
        # snake colliding with itself
        
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]): #x[0],y[0]->snake head,x[i],y[i]->snake other body
                #print("game over")
                self.play_sound("crash")#play sound after snake collapes itself
               
                raise "Collision Occurred "  # raise exception means->some thing happen when we go out of the game(through exception)
        
        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"
    
            
    def display_score(self):
        font=pygame.font.SysFont('arial',30) #pygame have font module
        score=font.render(f"Score: {self.snake.length}",True,(255,255,255))  #use python format string (255,255,255)->color code
        self.surface.blit(score,(800,10)) #to display anything on surface use blit (800,10)->display on top right corner 
        
    
    def show_game_over(self):
        self.render_background()
        font=pygame.font.SysFont('arial',40)
        line1 = font.render(f"Game is over! Your score is: {self.snake.length}",True,(214, 11, 17)) #after displaying final score end game
        self.surface.blit(line1,(200,300)) #show on screen in 200 x-axis & 300 y-axis
        line2 = font.render(f"To Play again press Enter. To exit press Escape!",True,(255,255,255))
        self.surface.blit(line2,(70,350))
        pygame.mixer.music.pause() #pause background music
        pygame.display.flip() #write because to show any changes on screen which is done (like refereshing your UI)
        
        
                
    
    def run(self):
        
        #UI concepts wait for user input.input either(keyboard,mouse)
        
        running = True #create one variable value is true
        pause = False #to stop after game over not work key 

        while running: #run while loop upto value of running variable is true
            for event in pygame.event.get(): #event in pygame (press keyboard or mouse get that event i.e get that action using get event)
                if event.type == KEYDOWN: #when press keys from keyboard(up,down,left,right)
                    if event.key == K_ESCAPE: #check which key press if its a escape key from keyboard  then also close window
                        running = False
                    
                    
                    if event.key == K_RETURN: #when key ENTER press or return
                        pygame.mixer.music.unpause()
                        pause = False
                        
                    if not pause:
                        if event.key == K_UP:  #when press key up from keyboard
                            self.snake.move_up() #call move_up function ,only direction change not walk then walk call walk() fun
                            
                            
                        if event.key == K_DOWN: #when press key down from keyboard
                            self.snake.move_down() #call move_down()
                          
                            
                        if event.key == K_LEFT: 
                            self.snake.move_left()
                            
                        if event.key == K_RIGHT: 
                           self.snake.move_right()
                            
                        
                elif event.type == QUIT: #when press on close button on pygame window
                    running = False
             
            try:                          #catch exception
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset() #reset the game when press enter to restart game again after game over 
                
            
            time.sleep(0.1) #use to sleep 0.2sec this while loop wait for 0.2 sec for execution (wait for 0.2 sec) if you want to increase snake block speed then change parameter
                    
        
        
if __name__ == '__main__':
    
    game = Game()
    game.run()
    
    
   



