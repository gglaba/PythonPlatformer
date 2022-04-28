import pygame as pg
from os import path
import pickle

pg.init()

screen_w = 1080
screen_h = 720
screen = pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption("tytul")
bgnd_img = pg.image.load('img/background.png')
player_img = pg.image.load('img/idle/idle_0.png')




class World():
    def __init__(self,data):
        self.tile_list = []
        
        clock = pg.time.Clock()
        fps = 60
        tile_s = 36
        col = 30
        width = 1080
        height = 720

        background = pg.image.load('img/background.png')
        tile1 = pg.image.load('img/Tile_01.png')
        tile2 = pg.image.load('img/Tile_02.png')
        tile3 = pg.image.load('img/Tile_03.png')
        tile4 = pg.image.load('img/Tile_12.png')

        row_count = 0

        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pg.transform.scale(tile1,(tile_s,tile_s))
                    imgRect = img.get_rect()
                    imgRect.x = col_count * tile_s
                    imgRect.y = row_count * tile_s
                    tile = (img,imgRect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pg.transform.scale(tile2,(tile_s,tile_s))
                    imgRect = img.get_rect()
                    imgRect.x = col_count * tile_s
                    imgRect.y = row_count * tile_s
                    tile = (img,imgRect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
    
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])



class Player():
    def __init__(self,x,y):
        img = pg.image.load('img/idle/idle_0.png')
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for n in range(1,7):
            img_right = pg.image.load(f'img/run/run_0{n}.png')
            img_right = pg.transform.scale(img_right,(180,120))
            img_left = pg.transform.flip(img_right,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)


        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.dir = 0
        self.hasJumped = False

    def update(self):
        dx = 0
        dy = 0
        w_cooldown = 0

        key = pg.key.get_pressed()
        if key[pg.K_SPACE] and self.hasJumped == False:
            self.vel_y = -15
            self.hasJumped = True
        if key[pg.K_SPACE] == False:
            self.hasJumped = False
        if key[pg.K_LEFT]:
            dx -= 3
            self.counter += 1
            self.dir = -1
        if key[pg.K_RIGHT]:
            dx += 3
            self.counter += 1
            self.dir = 1
        if key[pg.K_LEFT] == False and key[pg.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.dir == 1:
                self.image = self.images_right[self.index]
            if self.dir == -1:
                self.image = self.images_left[self.index]

        if self.counter > w_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.dir == 1:
                self.image = self.images_right[self.index]
            if self.dir == -1:
                self.image = self.images_left[self.index]


        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy



        self.rect.x += dx
        self.rect.y += dy


        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h
            dy = 0

        screen.blit(self.image,self.rect)
        





























level = 1

if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)



world = World(world_data)
player = Player(100, screen_h - 300)

run = True

while run:
    screen.blit(bgnd_img,(0,0))
    world.draw()

    player.update()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.display.update()







pg.quit()