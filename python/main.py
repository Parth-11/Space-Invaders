import pygame
import random
pygame.font.init()

#Window
W,H=600,600
window=pygame.display.set_mode((W,H))
pygame.display.set_caption('OWASP Stops Aliens')

#Load ships
Enemy1=pygame.transform.scale(pygame.image.load("python/characters/PngItem_490764.png"),(90,90))
Enemy2=pygame.transform.scale(pygame.image.load("python/characters/PngItem_851324.png"),(45,90))
Enemy3=pygame.transform.scale(pygame.image.load("python/characters/pngwing.com.png"),(90,90))
Player=pygame.image.load("python/characters/Player.png")

#Lasers
red = pygame.image.load("python/characters/pixel_laser_red.png")
green = pygame.image.load("python/characters/pixel_laser_green.png")
blue = pygame.image.load("python/characters/pixel_laser_blue.png")
yellow = pygame.image.load("python/characters/pixel_laser_yellow.png")

#Background
bg=pygame.transform.scale(pygame.image.load("python/characters/background.jpeg"),(W,H))

#Laser class--To display and move lasers on screen,handle collisions with ships
class Laser:
    def __init__(self, x, y, img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y+=vel

    def off_screen(self,height):
        return not (self.y<=height and self.y>=0)

    def collision(self, obj):
        return collide(self, obj)

#Ship class--Abstract class-parent for player class (owaspTiet) and Enemy class
#Attributes- x,y(coordinates),health(100),shipImg,laserImg(varies by ship),lasers[](list to hold laser objects),cooldown counter
#Methods- init,draw(ship and laser),moveLaser,width,height,cooldown counter,shoot(add laser object to laser list)
class Ship:
    INTERVAL=30  #30 milliseconds for cooldown
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.shipImg=None
        self.laserImg=None
        self.lasers = []
        self.coolDown = 0
        self.score=0

    def draw(self,window):
        window.blit(self.shipImg,(self.x,self.y))
        # pygame.draw.rect(window,(255,0,0),(self.x,self.y,50,50))
        for laser in self.lasers:
            laser.draw(window)

    def moveLasers(self, vel, obj):
        self.cooldown_counter()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(H):
                self.lasers.remove(laser)
            elif Laser.collision(self,obj):
                obj.health -=10
                self.lasers.remove(laser)

    def width(self):
        return self.shipImg.get_width()
    def height(self):
        return self.shipImg.get_height()

    def cooldown_counter(self):
        if self.coolDown>=self.INTERVAL:
            self.coolDown=0
        elif self.coolDown>0:
            self.coolDown+=1

    def shoot(self):
        if self.coolDown==0:
            laser=Laser(self.x, self.y, self.laserImg)
            self.lasers.append(laser)
            self.coolDown=1



#Player ship class- x,y,shipImg(player),laserImg(yellow),mask,health(100)
#Methods-init,moveLasers(remove object on collision,score+5,off screen condition),shoot
class owaspTiet(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.shipImg = Player
        self.laserImg = yellow
        self.mask = pygame.mask.from_surface(self.shipImg)
        self.maxHealth=health

    def moveLasers(self, vel, objs):
        self.cooldown_counter()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(H):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            self.score+=5


    def shoot(self):
        if self.coolDown==0:
            laser=Laser(self.x-5, self.y, self.laserImg)
            self.lasers.append(laser)
            self.coolDown=1


#Enemy ship class-dictionary for diff ships,Methods:init,move,shoot
class Enemy(Ship):
    shipMap={
            "red": (Enemy1,red),
            "green": (Enemy2,green),
            "blue": (Enemy3,blue)
            }
    def __init__(self,x,y,color,health=100):
        super().__init__(x,y,health)
        self.shipImg,self.laserImg=self.shipMap[color]
        self.mask=pygame.mask.from_surface(self.shipImg)

    def move(self,velocity,level):
        self.y+=velocity
        #if level>5:
            #self.x+=velocity

    def shoot(self):
        if self.coolDown==0:
            laser=Laser(self.x-5, self.y, self.laserImg)
            self.lasers.append(laser)
            self.coolDown=1

def collide(obj1, obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None

def main():
    run=True
    FPS=60

    level = 0
    lives=5
    velocity=4

    fonti=pygame.font.SysFont('stencil',30)
    lost_font = pygame.font.SysFont("stencil", 60)

    enemies=[]
    wave_length=5
    enemyVel=1

    laserVel=5

    player=owaspTiet((W/2)-(Player.get_width()/2),H*7/8-Player.get_height())

    clk=pygame.time.Clock()

    lost=False
    lost_count=0

    level_inc=False
    level_time=0


    def window_update():
            #bg,lives,level,score display
            window.blit(bg, (0, 0))
            livesCount=fonti.render(f"Lives: {lives}",1,(255,255,255))
            levelCount=fonti.render(f"Levels: {level}",1,(255,255,255))
            score_label=fonti.render(f"Score: {player.score}",1,(255,255,255))
            window.blit(livesCount,(10,10))
            window.blit(levelCount,(W-levelCount.get_width()-10,10))
            window.blit(score_label,(W/2-score_label.get_width()/2,10))

            #enemy and player display
            for enemy in enemies:
                enemy.draw(window)

            player.draw(window)

            #you lost text display
            if lost:
                lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
                window.blit(lost_label, (W/2 - lost_label.get_width()/2, H/2-lost_label.get_height()/2))

            #level text display
            if level_inc and level!=1:
                level_label = lost_font.render("Level Up!",1,(255,255,255))
                window.blit(level_label, (W/2 - level_label.get_width()/2, H/2-level_label.get_height()/2))

            pygame.display.update()

    while run:
        clk.tick(FPS)
        window_update()

        #if player loses,show lost screen for 3 seconds and quit
        if lives<= 0 or player.health <= 0:
            lost=True
            lost_count+=1
        if lost:
            if lost_count>FPS*3:
                run = False
            else:
                continue

        #if level increases,show level screen for 2 seconds
        if level_inc and level!=1:
            level_time+=1
            if level_time>FPS:
                level_inc=False
                level_time=0
            else:
                continue

        #Enemy spawn
        if len(enemies)==0:
            level+=1
            if level!=1:
                level_inc=True
            wave_length+=1
            for i in range(wave_length):
                enemy=Enemy(random.randrange(50,W-100),random.randrange(-400,-100),random.choice(["red","blue","green"]))
                enemies.append(enemy)

        #To quit game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False

        #keys for player movement
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x-velocity>0:
            player.x-=velocity #Left-a
        if keys[pygame.K_LEFT] and player.x-velocity>0:
            player.x-=velocity #Left-left arrow

        if keys[pygame.K_d] and player.x +velocity<W-player.width():
            player.x+=velocity #Right-d
        if keys[pygame.K_RIGHT] and player.x +velocity<W-player.width():
            player.x+=velocity #Right-right arrow

        if keys[pygame.K_w] and player.y-velocity>0:
            player.y-=velocity #Up-w
        if keys[pygame.K_UP] and player.y-velocity>0:
            player.y-=velocity #Up-up arrow

        if keys[pygame.K_s] and player.y+velocity<H-player.height():
            player.y+=velocity #Down-s
        if keys[pygame.K_DOWN] and player.y+velocity<H-player.height():
            player.y+=velocity #Down-down arrow

        if keys[pygame.K_SPACE]:
            player.shoot()

        #for enemy and enemy laser movement
        for enemy in enemies[:]:
            enemy.move(enemyVel,level)
            enemy.moveLasers(laserVel,player)

            if random.randrange(0,4*60)==1:
                enemy.shoot()
            if collide(enemy,player):
                player.health -=10
                enemies.remove(enemy)
            elif enemy.y + enemy.height()>H:
                lives-=1
                enemies.remove(enemy)

        #player laser
        player.moveLasers(-laserVel,enemies)

        window_update()

main()