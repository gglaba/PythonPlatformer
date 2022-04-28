import pickle
from os import path
import pygame as pg

pg.init()

clock = pg.time.Clock()
fps = 60
tile = 36
col = 30
width = 1080
height = 720

screen = pg.display.set_mode((width,height))
pg.display.set_caption("Generator poziomow")

background = pg.image.load('img/background.png')
tile1 = pg.image.load('img/Tile_01.png')
tile2 = pg.image.load('img/Tile_02.png')
tile3 = pg.image.load('img/Tile_03.png')
tile4 = pg.image.load('img/Tile_12.png')

clicked = False
level = 1

white = (255,255,255)


world_data = []

for row in range(col):
    r = [0] * 30
    world_data.append(r)

def grid():
    for column in range(30):
        pg.draw.line(screen,white,(column*tile,0),(column*tile,height))
        pg.draw.line(screen,white,(0,column*tile),(width,column*tile))

def draw_map():
    for row in range(30):
        for col in range(30):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    img = pg.transform.scale(tile1,(tile,tile))
                    screen.blit(img,(col * tile,row * tile))
                if world_data[row][col] == 2:
                    img = pg.transform.scale(tile2,(tile,tile))
                    screen.blit(img,(col * tile,row * tile))
                if world_data[row][col] == 3:
                    img = pg.transform.scale(tile3,(tile,tile))
                    screen.blit(img,(col * tile,row * tile))
                if world_data[row][col] == 4:
                    img = pg.transform.scale(tile4,(tile,tile))
                    screen.blit(img,(col * tile,row * tile))


run = True

while run:
    clock.tick(fps)


    screen.blit(background,(0,0))
    
    events = pg.event.get()

    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                pickle_out = open(f'level{level}_data','wb')
                pickle.dump(world_data,pickle_out)
                pickle_out.close()
            if event.key == pg.K_d:
                if path.exists(f'level{level}_data'):
                    pickle_in = open(f'level{level}_data', 'rb')
                    world_data = pickle.load(pickle_in)
    
    grid()
    draw_map()

    for event in events:
        if event.type == pg.QUIT:
            run = False



        if event.type == pg.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
            pos = pg.mouse.get_pos()
            x = pos[0] // tile
            y = pos[1] // tile

            if x < 30 and y < 30:
                if pg.mouse.get_pressed()[0] == 1:
                     world_data[y][x] += 1
                elif pg.mouse.get_pressed()[2] == 1:
                    world_data[y][x] = 0

                
                    
        if event.type == pg.MOUSEBUTTONUP:
            clicked = False
    
    pg.display.update()

pg.quit()

