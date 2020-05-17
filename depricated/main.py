import pygame as pg
import depricated.drawable.round_rect as rr


def draw_bg(window):
    bg_color = (255, 255, 0)
    vert_0 = rr.AAfilledRoundedRect(window, (0, 0, 10, 490), bg_color, radius=0.8)
    vert_1 = rr.AAfilledRoundedRect(window, (160, 0, 10, 490), bg_color, radius=0.8)
    vert_2 = rr.AAfilledRoundedRect(window, (320, 0, 10, 490), bg_color, radius=0.8)
    vert_3 = rr.AAfilledRoundedRect(window, (480, 0, 10, 490), bg_color, radius=0.8)

    hor_0 = rr.AAfilledRoundedRect(window, (0, 0, 490, 10), bg_color, radius=0.8)
    hor_1 = rr.AAfilledRoundedRect(window, (0, 160, 490, 10), bg_color, radius=0.8)
    hor_2 = rr.AAfilledRoundedRect(window, (0, 320, 490, 10), bg_color, radius=0.8)
    hor_3 = rr.AAfilledRoundedRect(window, (0, 480, 490, 10), bg_color, radius=0.8)

    font_color = (0,0,255)
    rectangles = []
    for i in range(3):
        temp = []
        for j in range(3):
            temp.append(pg.draw.rect(window,font_color,(10 + i * 160,10 + j*160,150,150)))
        rectangles.append(temp)
    return rectangles

pg.init()

window = pg.display.set_mode((490, 490))
pg.display.set_caption('Tic-Tac-Toe')

run = True

rectangles = draw_bg(window)
while run:

    pg.time.delay(100)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.display.update()
pg.quit()
