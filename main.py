import pygame as pg
import yaml
from win import Win
from game import Game

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

win = Win(config)
g = Game(config)

fall_time=970
last_fall = pg.time.get_ticks()
clock = pg.time.Clock()

run = True
while run:
    win.win.fill((0, 0, 0))
    clock.tick(60)
    current_time = pg.time.get_ticks()

    new = None
    g.update_board()
    win.draw_board(g.board)
    win.draw_next_piece(g.next_piece)
    win.draw_held_piece(g.held_piece)
    g.get_ghost_cords()
    win.draw_ghost_piece(g.ghost_piece)
    win.draw_grid()
    win.blit_text(g.score)
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
