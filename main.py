import pygame
import random
import time
import os
pygame.font.init()
WIDTH,HEIGHT=800,650

WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SPACE FIGHT")
#LOAD IMAGE
RED_SHIP=pygame.image.load(os.path.join("space_invader","ship_red3.png"))
BROWN_SHIP=pygame.image.load(os.path.join("space_invader","ship_brown4.png"))
PURPLE_SHIP=pygame.image.load(os.path.join("space_invader","ship_purple5.png"))

#Player Ship
HERO_SHIP=pygame.image.load(os.path.join("space_invader","pixel_ship_yellow.png"))
#LASER BULLETS
BLUE_LASER=pygame.image.load(os.path.join("space_invader","laser_blue3.png"))
RED_LASER=pygame.image.load(os.path.join("space_invader","laser_red.png"))
#Background
BG=pygame.image.load(os.path.join("space_invader","galaxy.jpg"))

class Laser():
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self,win):
        win.blit(self.img,(self.x,self.y))

    def off_screen(self,height):
        return not (self.y<=height and self.y>=0)

    def move(self,vel):
        self.y+=vel

    def collision(self,obj):
        return  collide(self,obj)
           
        
class ship():
    COOLDOWN=30
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cooldowncounter=0
    def draw(self,win):
        win.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(win) 
    
    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health-=10
                self.lasers.remove(laser)    
    def cooldown(self):
        if self.cooldowncounter>=self.COOLDOWN:
            self.cooldowncounter=0
        elif self.cooldowncounter>0:
            self.cooldowncounter+=1    


    def shoot(self):
        if self.cooldowncounter==0:
            laser=Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cooldowncounter=1    

    def get_width(self):
        return self.ship_img.get_width() 
    def get_height(self):
        return self.ship_img.get_height()        

class Player(ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img=HERO_SHIP
        self.laser_img=BLUE_LASER
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.max_health=health

    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:    
               for obj in objs:
                   if laser.collision(obj):
                       objs.remove(obj)
                    
                       if laser in self.lasers:
                           self.lasers.remove(laser)
                              
class Enemy(ship):
    COLOR_MAP={"red" :(RED_SHIP,RED_LASER),
               "purple":(PURPLE_SHIP,RED_LASER),
               "brown":(BROWN_SHIP,RED_LASER)
              }
    def __init__(self, x, y,color, health=100):
        super().__init__(x, y, health)
        self.ship_img,self.laser_img=self.COLOR_MAP[color]
        self.mask=pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y+=vel 

    def shoot(self):
        if self.cooldowncounter==0:
            laser=Laser(self.x-5,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cooldowncounter=1    
    

def collide(obj1,obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj2.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y))!=None


def main():  #main
    run=True
    FPS=60
    lives=5
    level=0
    lost=False
    lost_count=0
    enemies=[]
    wave_length=5
    enemy_vel=1
    player_vel=5
    laser_vel=5
    player=Player(300,550)
    main_font=pygame.font.SysFont("comicsans",50)
    lost_font=pygame.font.SysFont("comicsans",50)
    clock=pygame.time.Clock()
    def redrawwindow():
        WIN.blit(BG,(0,0))
        level_label=main_font.render(f"Level:{level}",1,(255,255,255))
        lives_label=main_font.render(f"Lives:{lives}",1,(255,255,255))
        WIN.blit(level_label,(WIDTH-level_label.get_width()-10,10))
        WIN.blit(lives_label,(10,10))
        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)
        if lost:
            lost_label=lost_font.render("You Lost!!",1,(255,255,255))
            WIN.blit(lost_label,(WIDTH/2-lost_label.get_width()/2,325))

        pygame.display.update()
    while run:
        clock.tick(FPS)
        redrawwindow()
        if lives<=0 or player.health<=0:
            lost=True
            lost_count+=1
        if lost:
            if lost_count>FPS*3:
                run=False
            else:
                continue        
        
        if len(enemies)==0:
            level+=1
            wave_length+=3
            for i in range(wave_length):
                enemy=Enemy(random.randrange(50,WIDTH-100),random.randrange(-1700,-200),random.choice(["red","purple","brown"]))
                #if enemy.x+enemy.get_width()>enemy.y+enemy.get_height()+30:
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x-player_vel>0:
            player.x-=player_vel
        if keys[pygame.K_RIGHT] and player.x+player_vel+player.get_width()<WIDTH:
            player.x+=player_vel
        if keys[pygame.K_DOWN] and player.y+player_vel+player.get_height()<HEIGHT:
            player.y+=player_vel
        if keys[pygame.K_UP]  and player.y-player_vel>0:
            player.y-=player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)
            if random.randrange(0,2*60)==1:
                enemy.shoot()
            if collide(enemy,player):
                player.health-=10
                enemies.remove(enemy)    
            elif enemy.y+enemy.get_height()>HEIGHT:
                lives-=1
                enemies.remove(enemy)
        
        player.move_lasers(-laser_vel,enemies) # enemylist
main()                