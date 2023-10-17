import pygame
pygame.font.init()

W,H=750,750
window=pygame.display.set_mode((W,H))
pygame.display.set_caption('OWASP Stops Aliens')

Enemy1=pygame.image.load("characters/PngItem_490764.png")
Enemy2=pygame.image.load("characters/PngItem_851324.png")
Enemy3=pygame.image.load("characters/pngwing.com.png")

Player=pygame.image.load("characters/Player.png")

#Lasers
red = pygame.image.load("characters/pixel_laser_red.png")
green = pygame.image.load("characters/pixel_laser_green.png")
blue = pygame.image.load("characters/pixel_laser_blue.png")
yellow = pygame.image.load("characters/pixel_laser_yellow.png")

bg=pygame.transform.scale(pygame.image.load("characters/background.jpeg"),(W,H))

class Ship:
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.shipImg=None
        self.laserImg=None
        self.lasers = []
        self.stopShooting = 0
    def draw(self,window):
        window.blit(self.shipImg,(self.x,self.y))
        # pygame.draw.rect(window,(255,0,0),(self.x,self.y,50,50))
class owaspTiet(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.shipImg = Player
        self.laserImg = yellow
        self.mask = pygame.mask.from_surface(self.shipImg)
        self.maxHealth=health

def main():
    run=True
    FPS=60
    level = 1
    lives=5
    velocity=4
    fonti=pygame.font.SysFont('stencil',40)
    player=owaspTiet(300,650)
    clk=pygame.time.Clock()
    while run:
        clk.tick(FPS)
        window.blit(bg, (0, 0))
        livesCount=fonti.render(f"Lives: {lives}",1,(255,255,255))
        levelCount=fonti.render(f"Levels: {level}",1,(255,255,255))
        window.blit(livesCount,(10,10))
        window.blit(levelCount,(W-levelCount.get_width()-10,10))
        player.draw(window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x-velocity>0:
            player.x-=velocity #Left
        if keys[pygame.K_d] and player.x +velocity<W-90:
            player.x+=velocity #Right
        if keys[pygame.K_w] and player.y-velocity>0:
            player.y-=velocity #Up
        if keys[pygame.K_s] and player.y+velocity<H-90:
            player.y+=velocity #Down

main()