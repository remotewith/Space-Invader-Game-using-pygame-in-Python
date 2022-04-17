import pygame
import random
import os
import time
pygame.font.init()# initialisation for the font

width , height = 750,750
win=pygame.display.set_mode((width,height))#our window
pygame.display.set_caption('MAJINS')

#load images
redship=pygame.image.load(os.path.join('assets','pixel_ship_red_small.png'))
greenship=pygame.image.load(os.path.join('assets','pixel_ship_green_small.png'))
blueship=pygame.image.load(os.path.join('assets','pixel_ship_blue_small.png'))

#player ship
yellowship=pygame.image.load(os.path.join('assets','pixel_ship_yellow.png'))

#lasers
redlaser=pygame.image.load(os.path.join('assets','pixel_laser_red.png'))
greenlaser=pygame.image.load(os.path.join('assets','pixel_laser_green.png'))
bluelaser=pygame.image.load(os.path.join('assets','pixel_laser_blue.png'))
yellowlaser=pygame.image.load(os.path.join('assets','pixel_laser_yellow.png'))

#background
bg=pygame.transform.scale(pygame.image.load(os.path.join('assets','background-black.png')),(width,height))


class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):# for ENEMY LASER
        self.y+=vel

    def off_screen(self,height):# gonna tell if the lasers go off screen
        return not( self.y< height and self.y>=0)

    def collision(self,obj):#gonna tell us if the laser collide with an object
        return collide(self,obj)

                                         

class Ship:
    COOLDOWN=20# if compared to fps then this is half sec
    def __init__(self,x,y,health=100):#we would import class thats why init and rest defined r the common charecters of the 4 ships     
        self.x=x#each ship would have its x and y value through this
        self.y=y#this is a general function in which values r common for every ship
        self.health=health
        self.ship_img=None#we can choose different image for different ships in later codes using this
        self.laser_img=None
        self.lasers=[]
        self.cool_down_counter=0#so there is a time diiference between laser shooting(of enemies)
    
    def draw(self,window):
        window.blit(self.ship_img , (self.x , self.y) )# when we call this function we need to give img,x,y for any ship
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):# this iss for the laser which is being shot by the ENEMY
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10# the obj is player ship
                self.lasers.remove(laser)# the laser which hits or go off screen is to be removed frm the list 'lasers'

                
    def cooldown(self):# assures that we do not shoot too fast or we have a delay in shooting
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter > 0:
            self.cool_down_counter +=1

    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
      
    def get_width(self):# to get the widht of the ships so that it can be used in the boundary conditions
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()
    

    
class Player(Ship):# this class will inherit charecters frm Ship so it can use any method defined under Ship
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)# this will directly call all the initialisation under __init__ in Ship within 1 line
        #super is the class(Ship) whose reference is being taken so that we could do things in 1 line only
        self.ship_img=yellowship
        self.laser_img=yellowlaser
        self.mask=pygame.mask.from_surface(self.ship_img)# for pixel perfect collision, this would take the ship_img as surface and will track it's pixels which would be helpful in collisions
        self.max_health=health

    def move_lasers(self,vel,objs):# this iss for the laser which is being shot by the PLAYER(as it is defined under Player)         
        self.cooldown()# objs here coz we have 3 diff type of ships to hit
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        
                        objs.remove(obj)# the obj is enemy ship which would be removed frm objs once we hit it
                        if laser in self.lasers:
                            
                            self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)
            
                        
    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width()*(self.health/self.max_health),10))
          
          

class Enemy(Ship):
    color_map={'red':(redship,redlaser),
               'green':(greenship,greenlaser),
               'blue':(blueship,bluelaser),
               
        }
    
    def __init__(self,x,y,color,health=100):
        super().__init__(x,y,health)# uses initialisation from Ship
        self.ship_img,self.laser_img=self.color_map[color]
        self.mask=pygame.mask.from_surface(self.ship_img)

    def move(self,vel):# for movement of the enemy ship,we just have to pass the velocity parameter
        self.y+=vel


    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x-15,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

        
def collide(obj1,obj2):# will tale two objects and will tell us if they r collided or not(using the mask thing here)
    offset_x= obj2.x - obj1.x# will tell the x distance b/w top right hand corner of the two objects
    offset_y= obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None #confirms if the mask of objects r overlaping using their offsets returns true or none


    

                                         
def main():# defining things here so we can use it later 
    run=True
    fps=60#so that there is no ambguity in collisions(higher value means faster and vice-versa),this is 1 sec value
    level=0
    lives=5
    main_font=pygame.font.SysFont('comicsans',50)#font and size of the texts that r to be drawn on window
    lost_font=pygame.font.SysFont('comicsans',70)

    enemies=[]# will store the positions of the enemies

    enemy_vel=2

    wave_length=5# the wave of the enemies for each level will vary with level
    
    player_vel=12# this is the no. of pixels the ship is gonna move
    laser_vel=8   
    player=Player(300,630)
    
    clock=pygame.time.Clock()

    lost=False
    lost_count=0

    def redraw_window():# writing code for drawing things on window
        win.blit(bg,(0,0))
        
        #draw text for live and level
        lives_label=main_font.render(f'Lives:{lives}',1,(255,255,255))
        level_label=main_font.render(f'Level:{level}',1,(255,255,255))

        win.blit(lives_label,(10,10))
        win.blit(level_label,(width-level_label.get_width()-10,10))
        
        for enemy in enemies:# drawing enemies in the window
            enemy.draw(win)
        
        player.draw(win)

        if lost:
            lost_label = lost_font.render('You Lost!!',1,(255,255,255))
            win.blit(lost_label,(width/2 - lost_label.get_width()/2,350))
            
        
        pygame.display.update()#refresing the window after some action

        
    
    while run:
        clock.tick(fps)# the 3 steps ahead which r fps clock= and clock.tick will maintain the consistency of game in any device clock.tick saves 60 frames per sec
        redraw_window()
        
        if lives<=0 or player.health <=0:# for defeat time
            lost=True
            lost_count+=1
            
        if lost:# to stop the game once we lose
            if lost_count> fps*3:# display message of lost for 3 sec
                run=False
            else:
                continue
            
        if len(enemies)==0:# after a level is over the list 'enemies' would go empty so we will increase the level
            level+=1
            wave_length+=5#adding 5 enemies per level can change accordingly
            for i in range(wave_length):# enemies r going to be at diff height(on -ve y axis) and will come below at same rate so it will appear that the r coming differently
                enemy=Enemy(random.randrange(50,width-100),random.randrange(-1500,-100),random.choice(['red','blue','green']))
                enemies.append(enemy)# will apeend the enemies in the list 'enemies'

            
        
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                run=False

        #for pressing of keys for player
        keys=pygame.key.get_pressed()#this returns a dict of all the keys and tells whether thy r pressed or not
        if keys[pygame.K_a] and player.x - player_vel > 0: #left
            player.x-=player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < width: #right
            player.x+=player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: #up
            player.y-=player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 10 < height: #down
            player.y+=player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        
        for enemy in enemies[:]:# to make enemies move,the second one makes a copy wich can be used to remove that enemy which crosses the height from real list 'enemies'
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)

            if random.randrange(0,4*60)==1:
                enemy.shoot()

            if collide(enemy,player):
                player.health-=10
                enemies.remove(enemy)                
                
            
            elif enemy.y + enemy.get_height() > height:# if the enemy crosses the height the live reduces by 1 with this code
                lives-=1
                enemies.remove(enemy)


        player.move_lasers(-(laser_vel+8),enemies)

def main_menu():
    title_font=pygame.font.SysFont('comicsans',70)
    run=True
    while run:
        win.blit(bg,(0,0))
        title_label=title_font.render('Press mouse to begin...',1,(255,255,255))
        win.blit(title_label,(width/2 - title_label.get_width() / 2 , 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                main()
                
                       
main_menu()        
        
