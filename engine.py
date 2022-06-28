import pygame
from os import path
import pickle
import time
import random


pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_w = 1080
screen_h = 720
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Swamp Knight")
bgnd_img = pygame.image.load('img/background.png')
player_img = pygame.image.load('img/idle/idle_0.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
score = 0
white = (255, 255, 255)
gameovr = 0
isInMain = True

score_font = pygame.font.Font("img/monogram.ttf",64)
title_font = pygame.font.Font("img/monogram.ttf",196)


def write_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#function to reset level
def reset_level(level):
    player.reset(100, screen_h - 130)
    opps.empty()
    portals.empty()
    Skeletons.empty()
    swamp_waters.empty()

    #load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world




class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.life = 10.0
        self.maxhealth = 10.0
        self.isIdle = True
        self.images_idle = []
        self.images_idleL = []
        for j in range(0,7):
            img_iright = pygame.image.load(f'img/idle/idle_{j}.png').convert_alpha()
            img_iright = pygame.transform.scale(img_iright,(50,60))
            img_ileft = pygame.transform.flip(img_iright,True,False)
            self.images_idle.append(img_iright)
            self.images_idleL.append(img_ileft)
        for n in range(1, 10):
            img_right = pygame.image.load(f'img/run/_Run_{n}.png').convert_alpha()
            img_right = pygame.transform.scale(img_right, (50, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.img_attacks = []
        self.img_attacksl =[]
        for i in range(1,3):
            img_attackr = pygame.image.load(f'img/attack/_Attack_{i}.png').convert_alpha()
            img_attackr = pygame.transform.scale(img_attackr, (50, 60))
            img_attackl = pygame.transform.flip(img_attackr, True, False)
            self.img_attacks.append(img_attackr)
            self.img_attacksl.append(img_attackl)

        self.image = self.images_idle[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.direction = 0
        self.hasJumped = False
        self.hasAttacked = False
        self.skeletonCounter = 0
        self.scor = 0
        
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.life = 10.0
        self.maxhealth = 10.0
        self.isIdle = True
        self.images_idle = []
        self.images_idleL = []
        for j in range(0,7):
            img_iright = pygame.image.load(f'img/idle/idle_{j}.png').convert_alpha()
            img_iright = pygame.transform.scale(img_iright,(50,60))
            img_ileft = pygame.transform.flip(img_iright,True,False)
            self.images_idle.append(img_iright)
            self.images_idleL.append(img_ileft)
        for n in range(1, 10):
            img_right = pygame.image.load(f'img/run/_Run_{n}.png').convert_alpha()
            img_right = pygame.transform.scale(img_right, (50, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.img_attacks = []
        self.img_attacksl =[]
        for i in range(1,3):
            img_attackr = pygame.image.load(f'img/attack/_Attack_{i}.png').convert_alpha()
            img_attackr = pygame.transform.scale(img_attackr, (50, 60))
            img_attackl = pygame.transform.flip(img_attackr, True, False)
            self.img_attacks.append(img_attackr)
            self.img_attacksl.append(img_attackl)

        self.image = self.images_idle[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.direction = 0
        self.hasJumped = False
        self.hasAttacked = False
        self.skeletonCounter = 0
        self.scor = 0
        
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.life = 10.0
        self.maxhealth = 10.0
        for n in range(1, 10):
            img_right = pygame.image.load(f'img/run/_Run_{n}.png').convert_alpha()
            img_right = pygame.transform.scale(img_right, (50, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.img_attacks = []
        self.img_attacksl =[]
        for i in range(1,3):
            img_attackr = pygame.image.load(f'img/attack/_Attack_{i}.png').convert_alpha()
            img_attackr = pygame.transform.scale(img_attackr, (50, 60))
            img_attackl = pygame.transform.flip(img_attackr, True, False)
            self.img_attacks.append(img_attackr)
            self.img_attacksl.append(img_attackl)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.direction = 0
        self.hasJumped = False
        self.hasAttacked = False


    def getScore(self):
        return self.scor
    

    def getStatus(self):
        return self.isIdle

    def gethealth(self):
        self.h = (self.life / self.maxhealth) * 100
        return self.h


    def update(self,gameovr):
        dx = 0
        dy = 0
        walk_cooldown = 5
        attack_cooldown = 10
        cntr = 0


        if gameovr == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
                self.isIdle = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
                self.isIdle = False
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
                self.isIdle = False
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                self.isIdle = True
                if self.direction == 1:
                    self.image = self.images_idle[self.index]
                if self.direction == -1:
                    self.image = self.images_idleL[self.index]
            if key[pygame.K_SPACE]:
                self.hasAttacked = True
                self.index = 0
                self.image = self.img_attacks[self.index]
                self.counter += 0.01
                self.isIdle = False


        if self.isIdle == True:
            cntr += 1
            if self.direction == 1:
               if cntr>5:
                   self.index += 1
                   cntr = 0
                   self.image = self.images_idle[self.index]
            if self.direction == -1:
                self.image = self.images_idleL[self.index]




        #handle animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.hasAttacked == False:
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            if self.hasAttacked == True:
                if self.index >= len(self.img_attacks):
                    self.index = 0
                    self.hasAttacked = False
                if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                    self.index += 1
                if self.direction == 1:
                    self.image = self.img_attacks[self.index]
                if self.direction == -1:
                    self.image = self.img_attacksl[self.index]


        #add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #check for collision
        for tile in world.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jumped = False

        if self.rect.x >= screen_w:
            self.rect.x = screen_w - 20
            dx = 0
       


        if self.hasAttacked == False and pygame.sprite.spritecollide(self,opps, False):
            self.life -= 0.5
            print("wydupcaj")
            self.rect.x -= dx * 5
            self.scor -= 10


        if self.hasAttacked == True and pygame.sprite.spritecollide(self,opps, True):
            self.scor += 20

        if self.life <= 0:
            gameovr = -1

        if pygame.sprite.spritecollide(self,portals,False):
            gameovr = 1

        if pygame.sprite.spritecollide(self,swamp_waters,False):
            gameovr = -1
            self.scor -= 200

        
        if self.hasAttacked == True and pygame.sprite.spritecollide(self,Skeletons, True):
            self.scor += 100

        if self.hasAttacked == False and pygame.sprite.spritecollide(self,Skeletons,False):
            self.life -= 2
            self.rect.x -= dx * 10
            self.scor -= 50

        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h
            dy = 0


        #draw player onto screen
        screen.blit(self.image,self.rect)
        return gameovr


class World():
    def __init__(self, data):
        self.tile_list = []

        tile_s = 36
        col = 30
        width = 1080
        height = 720

        background = pygame.image.load('img/background.png').convert_alpha()
        tile1 = pygame.image.load('img/Tile_01.png').convert_alpha()
        tile2 = pygame.image.load('img/Tile_02.png').convert_alpha()
        tile3 = pygame.image.load('img/Tile_03.png').convert_alpha()
        tile4 = pygame.image.load('img/Tile_12.png').convert_alpha()
        tile5 = pygame.image.load('img/portal/portal_01.png').convert_alpha()
        tile6 = pygame.image.load('img/Tile_30.png').convert_alpha()
     

        row_count = 0

        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(tile1, (tile_s, tile_s))
                    imgRect = img.get_rect()
                    imgRect.x = col_count * tile_s
                    imgRect.y = row_count * tile_s
                    tile = (img, imgRect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(tile2, (tile_s, tile_s))
                    imgRect = img.get_rect()
                    imgRect.x = col_count * tile_s
                    imgRect.y = row_count * tile_s
                    tile = (img, imgRect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(tile3, (tile_s, tile_s))
                    imgRect = img.get_rect()
                    imgRect.x = col_count * tile_s
                    imgRect.y = row_count * tile_s
                    tile = (img, imgRect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(tile4, (tile_s, tile_s))
                    imgRect = img.get_rect()
                    imgRect.x = col_count * tile_s
                    imgRect.y = row_count * tile_s
                    tile = (img, imgRect)
                    self.tile_list.append(tile)
                if tile == 7:
                    # img = pygame.transform.scale(tile6, (tile_s, tile_s))
                    # imgRect = img.get_rect()
                    # imgRect.x = col_count * tile_s
                    # imgRect.y = row_count * tile_s
                    # tile = (img, imgRect)
                    # self.tile_list.append(tile)
                    water = Swamp(col_count * tile_s, row_count * tile_s )
                    swamp_waters.add(water)

                if tile == 5:
                    opp = Opp(col_count * tile_s, row_count * tile_s )
                    opps.add(opp)
                if tile == 6:
                    exit = Portal(col_count * tile_s - 30, row_count * tile_s - 60)
                    portals.add(exit)

                if tile == 8:
                    skeleton = Skeleton(col_count * tile_s - 30, row_count * tile_s - 40 )
                    Skeletons.add(skeleton)
                
  

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])










class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index_p = 0
        for i in range(1,7):
            img = pygame.image.load(f'img/portal/portal_0{i}.png').convert_alpha()
            img = pygame.transform.scale(img,(100,100))
            self.images.append(img)
        self.image = self.images[self.index_p]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.cooldown = 0

    def update(self):
       self.cooldown += 1
       if gameovr == 0:
            #print(self.cooldown)
            if self.cooldown >= 8:
                self.index_p += 1
                self.cooldown = 0
                print(self.index_p)
                if self.index_p >= 6:
                    self.index_p = 0
                if self.index_p <= 6:
                    self.image = self.images[self.index_p]
 
        #  self.cooldown += 1
        # if gameovr == 0:
        #     print(self.cooldown)
        #     if self.cooldown >= 5:
        #         self.index += 1
        #         self.cooldown = 0
        #         print("SZKIELET: " + str(self.index))
        #         #self.image = self.images_r[self.index]
        #         if self.index > 16:
        #             self.index = 0
        #         if self.index < 16:
        #             self.image = self.images_r[self.index]



class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        screen.blit(self.image, self.rect)

        return action
        


class Skeleton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images_r = []
        self.images_l = []
        for i in range(0,17):
            img = pygame.image.load(f'img/skeleton/skeleton_0{i}.png').convert_alpha()
            img = pygame.transform.scale(img,(80,80))
            imgL = pygame.transform.flip(img,True,False)
            self.images_r.append(img)
            self.images_l.append(imgL)
        self.index = 0
        self.image = self.images_l[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.cooldown = 0
        self.life = 2


    def update(self):
        self.cooldown += 1
        if gameovr == 0:
            print(self.cooldown)
            if self.cooldown >= 5:
                self.index += 1
                self.cooldown = 0
                print("SZKIELET: " + str(self.index))
                #self.image = self.images_r[self.index]
                if self.index > 16:
                    self.index = 0
                if self.index < 16:
                    self.image = self.images_l[self.index]



            
        





class Opp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_right = pygame.image.load(f'img/enemy/enem_1.png').convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right,(40,40))
        self.image_left = pygame.transform.flip(self.image_right,True,False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1


        if self.move_direction == 1:
            self.image = self.image_left
        if self.move_direction == -1:
            self.image = self.image_right




class Swamp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/Tile_30.png').convert_alpha()
        self.image = pygame.transform.scale(img, (40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




level = 1


player = Player(10, screen_h - 100)

opps = pygame.sprite.Group()
portals = pygame.sprite.Group()
swamp_waters = pygame.sprite.Group()
Skeletons = pygame.sprite.Group()

if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

start_button = Button(screen_w // 2 - 150, screen_h // 2 - 100, start_img)
exit_button = Button(screen_w // 2 - 150 , screen_h // 2 + 100, exit_img)


run = True

while run:

    clock.tick(fps)

    

    screen.blit(bgnd_img, (0, 0))

    if isInMain == True:
        write_text("SWAMP KNIGHT", title_font,white,screen_w // 2 -  425, 50)
        if start_button.draw():
            isInMain = False
        if exit_button.draw():
            run = False

    else:

   
        world.draw()
        opps.draw(screen)
        portals.draw(screen)
        swamp_waters.draw(screen)
        Skeletons.draw(screen)
            
        opps.update()

        Skeletons.update()

        portals.update()

        gameovr = player.update(gameovr)

        write_text('Score:' + str(player.getScore()), score_font, white, screen_w /2 - 100, 10)

        health = player.gethealth()
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(20,20,health * 2,10))

        if gameovr == -1:
            world_data = []
            world = reset_level(level)
            gameovr = 0
            score = 0
        
        if gameovr == 1:
            level += 1
            score += 200
            world_data = []
            if level <= 3:
                world_data = []
                world = reset_level(level)
                gameovr = 0
            if level > 3:
                screen.blit(bgnd_img,(0,0))
                write_text("YOU WON! " , title_font,white,screen_w // 2 - 275, 50)
                scr = str(player.getScore())
                write_text("SCORE: " + str(player.getScore()),title_font,white,screen_w // 2 - 400, 150)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
