import pygame
import sys
from random import*
from pygame.locals import*
from time import*
import pyganim

width = 600
height = 700
fps = 30

score=0
star_score=0

pygame.init()

e1=pygame.image.load('images/spaceshooter/PNG/Enemies/enemyBlack1.png')
e2=pygame.image.load('images/spaceshooter/PNG/Enemies/enemyBlack2.png')
e3=pygame.image.load('images/spaceshooter/PNG/Enemies/enemyBlack3.png')
e4=pygame.image.load('images/spaceshooter/PNG/Enemies/enemyBlack4.png')
e5=pygame.image.load('images/spaceshooter/PNG/Enemies/enemyBlack5.png')

meteors=[]
lasers=[]
enemies=[]

e1_down=pygame.transform.flip(e1,False,True)
e2_down=pygame.transform.flip(e2,False,True)
e3_down=pygame.transform.flip(e3,False,True)
e4_down=pygame.transform.flip(e4,False,True)
e5_down=pygame.transform.flip(e5,False,True)

enemy_anim_down=[e1_down,
                 e2_down,
                 e3_down,
                 e4_down,
                 e5_down]


#player

im1=pygame.image.load('images/spaceshooter/PNG/playerShip1_red.png')
im2=pygame.image.load('images/spaceshooter/PNG/playerShip2_red.png')
im3=pygame.image.load('images/spaceshooter/PNG/playerShip3_red.png')

im1_left=pygame.transform.rotate(im1,90)
im2_left=pygame.transform.rotate(im2,90)
im3_left=pygame.transform.rotate(im3,90)

im1_right=pygame.transform.rotate(im1,-90)
im2_right=pygame.transform.rotate(im2,-90)
im3_right=pygame.transform.rotate(im3,-90)

anim_left=[im1_left,
           im2_left,
           im3_left]

anim_right=[im1_right,
            im2_right,
            im3_right]

anim_up=['images/spaceshooter/PNG/playerShip1_red.png',
         'images/spaceshooter/PNG/playerShip2_red.png',
         'images/spaceshooter/PNG/playerShip3_red.png']

anim_down=['images/spaceshooter/PNG/playerShip1_red_down.png',
           'images/spaceshooter/PNG/playerShip2_red_down.png',
           'images/spaceshooter/PNG/playerShip3_red_down.png']

left=False
right=False
up=False
down=False

a=pygame.display.set_mode((width,height),0,0)
pygame.display.set_caption('Game')
pygame.display.set_icon(pygame.image.load('icon.ico'))

pygame.time.set_timer(pygame.USEREVENT,3000)

bg=pygame.image.load('images/spaceshooter/Backgrounds/purple.png')
bg=pygame.transform.scale(bg,(600,700))
clock=pygame.time.Clock()

laser_list=pygame.sprite.Group()
enemy_list=pygame.sprite.Group()

class Laser(pygame.sprite.Sprite):
    def __init__(self,x,y,filename,dir):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((13,37))
        self.rect=self.image.get_rect(centerx=x,centery=y)
        self.image.set_colorkey((0, 0, 0))
        self.im = pygame.image.load(filename)
        lasers.append(self)
        self.image.blit(self.im, (0, 0))
        a.blit(self.image,self.rect)
        pygame.display.update()
        self.speedy=0
        self.speedx=0
        if dir=='left':
            self.image=pygame.transform.rotate(self.image, 90)
            self.speedx=-9
            self.speedy = 0

        if dir=='right':
            self.image=pygame.transform.rotate(self.image, -90)
            self.speedx=9
            self.speedy = 0
        if dir=='up':
            self.image=pygame.transform.flip(self.image, False, True)
            self.speedy=-9
            self.speedx=0
        if dir=='down':
            self.image=pygame.transform.flip(self.image, False, True)
            self.speedy=9
            self.speedx = 0

    def update(self):

        if self.rect.bottom<0 or self.rect.right>width or self.rect.top>height or self.rect.left<0:
            self.kill()

        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        #a.blit(self.image,(self.rect.x+self.speedx, self.rect.y+self.speedy))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((56, 56))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(centerx=randint(0,600), centery=0)
        self.speed = randint(0,7)
        anim_delay = 0.3
        enemies.append(self)
        boltanim = []
        for anim in enemy_anim_down:
            boltanim.append((anim, anim_delay))
        self.boltanim = pyganim.PygAnimation(boltanim)
        self.boltanim.play()

    def animate(self):
        a.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.image.fill((94, 63, 107))
        self.image.set_colorkey((94, 63, 107))
        self.boltanim.blit(self.image, (0, 0))
        self.animate()

        if self.rect.top>height:
            self.kill()
        self.rect.y+=self.speed
    def shoot(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_sprite=pygame.Surface((56,48))
        self.image_sprite.set_colorkey((0,0,0))
        self.rect=self.image_sprite.get_rect(centerx=100,centery=500)
        self.speed=7
        self.dir=None
        anim_delay = 0.3

        boltanim=[]
        for anim in anim_left:
            boltanim.append((anim,anim_delay))
        self.boltanimleft=pyganim.PygAnimation(boltanim)
        self.boltanimleft.play()

        boltanim = []
        for anim in anim_right:
            boltanim.append((anim, anim_delay))
        self.boltanimright= pyganim.PygAnimation(boltanim)
        self.boltanimright.play()

        boltanim = []
        for anim in anim_up:
            boltanim.append((anim, anim_delay))
        self.boltanimup = pyganim.PygAnimation(boltanim)
        self.boltanimup.play()

        boltanim = []
        for anim in anim_down:
            boltanim.append((anim, anim_delay))
        self.boltanimdown = pyganim.PygAnimation(boltanim)
        self.boltanimdown.play()

        self.last_anim=self.boltanimup

    def animate(self):
        a.blit(self.image_sprite, (self.rect.x, self.rect.y))

    def update(self,left,right,up,down):
        if left:
            self.image_sprite.fill((94, 63, 107))
            self.image_sprite.set_colorkey((94, 63, 107))
            self.boltanimleft.blit(self.image_sprite, (0, 0))
            self.rect.x-=self.speed
            self.last_anim=self.boltanimleft
            #self.dir='left'
        if right:
            self.image_sprite.fill((94, 63, 107))
            self.image_sprite.set_colorkey((94, 63, 107))
            self.boltanimright.blit(self.image_sprite, (0, 0))
            self.rect.x+=self.speed
            self.last_anim = self.boltanimright
            #self.dir='right'
        if up:
            self.image_sprite.fill((94, 63, 107))
            self.image_sprite.set_colorkey((94, 63, 107))
            self.boltanimup.blit(self.image_sprite, (0, 0))
            self.rect.y-=self.speed
            self.last_anim = self.boltanimup
            #self.dir='up'
        if down:
            self.image_sprite.fill((94, 63, 107))
            self.image_sprite.set_colorkey((94, 63, 107))
            self.boltanimdown.blit(self.image_sprite, (0, 0))
            self.rect.y+=self.speed
            self.last_anim = self.boltanimdown
            #self.dir='down'

        if not(left or right or up or left):
            self.image_sprite.fill((94,63,107))
            self.image_sprite.set_colorkey((94,63,107))
            self.last_anim.blit(self.image_sprite,(0,0))
            #self.dir='up'
        self.animate()

    def shoot(self):
        if self.last_anim==self.boltanimleft:
            self.dir='left'
        if self.last_anim==self.boltanimright:
            self.dir='right'
        if self.last_anim==self.boltanimup:
            self.dir='up'
        if self.last_anim==self.boltanimdown:
            self.dir='down'
        #self.update(left,right,up,down)
        laser=Laser(self.rect.x,self.rect.y,'images/spaceshooter/PNG/Lasers/laserGreen12.png',self.dir)
        laser.update()
        laser_list.add(laser)
        pygame.display.update()

class Star(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((31,30))
        self.image.fill((94, 63, 107))
        self.image.set_colorkey((94, 63, 107))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.im=pygame.image.load('images/spaceshooter/PNG/Power-ups/star_silver.png')
        self.image.blit(self.im,(0,0))
        pygame.display.update()

star_list=pygame.sprite.Group()

for i in range(5):
    star=Star(randint(25,550),randint(25,650))
    star_list.add(star)

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_list=['images/spaceshooter/PNG/Meteors/meteorGrey_med2.png',
                         'images/spaceshooter/PNG/Meteors/meteorBrown_big4.png',
                         'images/spaceshooter/PNG/Meteors/meteorGrey_tiny1.png',
                         'images/spaceshooter/PNG/Meteors/meteorBrown_med3.png',
                         'images/spaceshooter/PNG/Meteors/meteorGrey_med1.png',
                         'images/spaceshooter/PNG/Meteors/meteorBrown_tiny2.png']

        self.image=pygame.image.load(choice(self.image_list))
        self.rect=self.image.get_rect(centerx=randint(0,600),centery=0)
        meteors.append(self)
        self.speedx=randint(0,7)
        self.speedy=randint(0,7)

    def update(self):
        if self.rect.left<0:
            self.speedx*=-1
        if self.rect.right>width:
            self.speedx*=-1
        if self.rect.top>height:
            self.kill()

        self.rect.y += self.speedy
        self.rect.x += self.speedx
        a.blit(self.image, (self.rect.x, self.rect.y))

player=Player()
meteor_list=pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                left=True
                right=False
                up=False
                down=False
            if event.key==pygame.K_RIGHT:
                right=True
                left=False
                up = False
                down = False
            if event.key==pygame.K_UP:
                up=True
                down=False
                left = False
                right = False
            if event.key==pygame.K_DOWN:
                down=True
                up=False
                left = False
                right = False
            if event.key==pygame.K_SPACE:
                if player.last_anim == player.boltanimleft:
                    player.dir = 'left'
                if player.last_anim == player.boltanimright:
                    player.dir = 'right'
                if player.last_anim == player.boltanimup:
                    player.dir = 'up'
                if player.last_anim == player.boltanimdown:
                    player.dir = 'down'
                player.update(left,right,up,down)
                player.shoot()

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                left=False
                right=False
                up=False
                down=False

            if event.key==pygame.K_RIGHT:
                right=False
                left=False
                up = False
                down = False

            if event.key==pygame.K_UP:
                up=False
                down=False
                up = False
                down = False

            if event.key==pygame.K_DOWN:
                down=False
                up=False
                up = False
                down = False


        if event.type==pygame.USEREVENT:
            for i in range(randint(0,2)):
                m1=Meteor()
                meteor_list.add(m1)
            for i in range(randint(0,3)):
                en=Enemy()
                enemy_list.add(en)

    clock.tick(fps)

    a.blit(bg, (0, 0))
    player.update(left,right,up,down)
    a.blit(player.image_sprite, (player.rect.x, player.rect.y))
    for m in meteor_list:
        m.update()
    meteor_list.draw(a)
    for e in enemy_list:
        e.update()
    enemy_list.draw(a)
    for l in laser_list:
        l.update()
    laser_list.draw(a)
    star_list.draw(a)
    hits=pygame.sprite.spritecollide(player,meteor_list,True)
    if hits:
        text='Game Over!'
        font=pygame.font.SysFont('Arial',25)
        text=font.render(text,True,(255,255,255))
        a.blit(text,[250,300])
        pygame.display.update()
        sleep(3)
        pygame.quit()
        sys.exit()
    hits_with_enemy = pygame.sprite.spritecollide(player, enemy_list, True)
    if hits_with_enemy:
        text = 'Game Over!'
        font = pygame.font.SysFont('Arial', 35)
        text = font.render(text, True, (255, 255, 255))
        a.blit(text, [250, 300])
        pygame.display.update()
        sleep(3)
        pygame.quit()
        sys.exit()
    laser_hits=pygame.sprite.groupcollide(laser_list,enemy_list,True,True)
    if laser_hits:
        score+=1
    stone_hits=pygame.sprite.groupcollide(laser_list,meteor_list,True,True)
    if stone_hits:
        score+=1
    star_hits = pygame.sprite.groupcollide(laser_list, star_list, True, True)
    if star_hits:
        star_score += 1
    hits_star = pygame.sprite.spritecollide(player, star_list, True)
    if hits_star:
        star_score += 1
    score_text='Score: '+str(score)
    font = pygame.font.SysFont('Arial', 25)
    text = font.render(score_text, True, (0, 255, 0))
    a.blit(text, [25, 650])

    star_text = 'Star: ' + str(star_score)
    font = pygame.font.SysFont('Arial', 25)
    text = font.render(star_text, True, (0, 255, 0))
    a.blit(text, [525, 650])
    pygame.display.update()
