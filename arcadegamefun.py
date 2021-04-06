import pygame
import random
pygame.init()
# Colors  R  G  B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
LILAC = (200, 162, 200)
GREY = (100, 100, 100)
PUTRID = (242, 232, 104)
YELLOW = (255, 255,0)

timer = 0

colorlist = [BLACK,RED,GREEN,BLUE,PURPLE,LILAC,GREY,PUTRID,YELLOW]

#List of settings for the game:
tripleshot = True
powermodetoggle = True



# Classes

class Block(pygame.sprite.Sprite):
    # this is THE BLOCK
    def __init__(self,color):
        #call the parent class, (Sprite class constructor)
        super().__init__()
        self.image = pygame.Surface([20,15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y += 1.75
class Player (pygame.sprite.Sprite):
#This  class represents the user/player themselves
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface ([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

def bulletspawn(quantity,spawnx,spawny):
    for i in range (quantity):
        #pew pew time
        bullet = Bullet()
        bullet.rect.x = spawnx
        bullet.rect.y = spawny
        all_sprites_list.add(bullet)
        bullet_list.add(bullet)
def sidebulletspawn(quantity,spawnx,spawny):
    for i in range(quantity):
        bullet = SideBullet()
        bullet.rect.x = spawnx
        bullet.rect.y = spawny
        all_sprites_list.add(bullet)
        bullet_list.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([8,20])
        colorchoice = colorlist[random.randint(0,8)]
        self.image.fill(colorchoice)
        self.rect = self.image.get_rect()
    def update(self):
            self.rect.y += -10
class SideBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20,8])
        colorchoice = colorlist[random.randint(0,8)]
        self.image.fill(colorchoice)
        self.rect = self.image.get_rect()
        self.direction = random.randint(0,1)
    def update(self):
        if self.direction == 1:
            self.rect.x += -10
        elif self.direction == 0:
            self.rect.x += 10

        '''
        self.rect.x += random.randint(-10,10)
        self.rect.y += random.randint(-10,10)
        colorchoice = colorlist[random.randint(0,9)]
        self.image.fill(colorchoice)
        '''

#----------------------------------------------------------------------------- So it begins. -----------------------------------------------------------------------------------------------------------
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width,screen_height])


all_sprites_list = pygame.sprite.Group()
block_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
pygame.display.set_caption("Wheee")
#oh no, sprite time
"""for i in range(10):
    block = Block(BLUE)
    block.rect.x = random.randrange(screen_width)
    block.rect.y = 10
    block_list.add(block)
    all_sprites_list.add(block)"""
spawnnumber = 0

player = Player()
all_sprites_list.add(player)

done = False

clock = pygame.time.Clock()
score = 0
player.rect.y = 370
pygame.mouse.set_visible(0)



""" Main loop time! Ya--hoooey!"""
lives = 10
powermode = False
while not done:
    while lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bulletspawn(1,player.rect.x,player.rect.y)
                    if tripleshot == True:
                        bulletspawn(1,player.rect.x +15, player.rect.y)
                        bulletspawn(1,player.rect.x -15, player.rect.y)
                elif event.key == pygame.K_w:
                    screen.fill(WHITE)
                elif event.key == pygame.K_t:
                    for bullet in bullet_list:
                        bullet_list.remove(bullet)
                        all_sprites_list.remove(bullet)
                if score % 25 == 0:
                    powermode = True
                if score % 50 == 0:
                    powermode = False

        all_sprites_list.update()
        """if  5 > len(block_list):
            for i in range(1):
                blue = Block(BLUE)
                blue.rect.x = random.randrange(screen_width-10)
                blue.rect.y = 10
                block_list.add(blue)
                all_sprites_list.add(blue)"""
        if spawnnumber % 300 == 1:
            for i in range(5):
                blue = Block(BLUE)
                blue.rect.x = random.randrange(screen_width-10)
                blue.rect.y = 10
                block_list.add(blue)
                all_sprites_list.add(blue)
        for sidebullet in bullet_list:
            block_hit_list = pygame.sprite.spritecollide(sidebullet,block_list,True)
            for block in block_hit_list:
                gravex = (sidebullet.rect.x + random.randint(-10,10))
                gravey = (sidebullet.rect.y + random.randint(-10,10))
                if powermode == True:
                    sidebulletspawn(5,gravex,gravey)
                bullet_list.remove(sidebullet)
                all_sprites_list.remove(sidebullet)
                score += 1
                print(score)
            if sidebullet.rect.x < -10 or sidebullet.rect.x > 710:
                bullet_list.remove(sidebullet)
                all_sprites_list.remove(sidebullet)
        for bullet in bullet_list:
            #check to see if bullet has gone and done a murder
            block_hit_list = pygame.sprite.spritecollide(bullet,block_list,True)

            for block in block_hit_list:
                gravex = (bullet.rect.x + random.randint(-10,10))
                gravey = (bullet.rect.y + random.randint(-10,10))
                if powermode == True:
                    sidebulletspawn(5,gravex,gravey)
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                print(score)
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
        for blue in block_list:
            if blue.rect.y > screen_height:
                block_list.remove(blue)
                all_sprites_list.remove(blue)
                lives -= 1
        screen.fill(WHITE)
        all_sprites_list.draw(screen)

        clock.tick(60)
        pygame.display.flip()
        spawnnumber += 1

    font = pygame.font.SysFont('timesnewroman',25,False, True)
    text = font.render("GAME OVER",True, BLACK, WHITE)
    screen.blit(text,[100,50])
    pygame.display.flip()
pygame.quit()
