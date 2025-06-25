import pygame as pg
import yaml
from win import Win
from game import Game

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

win = Win(config)
g = Game(config)

fall_time = 970
last_fall = pg.time.get_ticks()
clock = pg.time.Clock()

run = True
while run:
    clock.tick(60)
    current_time = pg.time.get_ticks()

    win.update_window(g)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                g.rotate_piece()
            if event.key == pg.K_DOWN:
                g.move_piece(-1)
            if event.key == pg.K_RIGHT:
                g.move_piece(1)
            if event.key == pg.K_LEFT:
                g.move_piece(0)
            if event.key == pg.K_SPACE:
                while g.move_piece(-1, True):
                    continue
            if event.key == pg.K_LSHIFT:
                g.hold_piece()

    if current_time - last_fall > fall_time:
        g.move_piece(-1)
        last_fall = current_time

    pg.display.flip()
