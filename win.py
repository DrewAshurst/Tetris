import pygame as pg


class Win:
    def __init__(self, config):
        self.config = config
        self.screen_height = int(self.config["screen_height"])
        self.screen_width = int(self.config["screen_width"])
        self.block_size = int(self.config["block_size"])
        self.rows = int(self.config["rows"])
        self.columns = int(self.config["columns"])
        self.win = pg.display.set_mode((self.screen_height, self.screen_width))
        self.height_offset = int(self.screen_height / 4)
        pg.font.init()

    def update_window(self, game):
        game.update_board()
        game.get_ghost_cords()
        self.win.fill((0, 0, 0))
        self.draw_board(game.board)
        self.draw_next_piece(game.next_piece)
        self.draw_held_piece(game.held_piece)
        self.draw_ghost_piece(game.ghost_piece)
        self.draw_grid()
        self.blit_text(game.score)

    def draw_grid(self):
        for x in range(0, self.columns * self.block_size, self.block_size):
            for y in range(self.height_offset, self.screen_height, self.block_size):
                rect = pg.Rect(x, y, self.block_size, self.block_size)
                pg.draw.rect(self.win, (255, 255, 255), rect, 1)

    def draw_board(self, board):
        for y in range(len(board)):
            for x in range(len(board[y])):
                pg.draw.rect(
                    self.win,
                    board[y][x][2],
                    pg.Rect(
                        self.block_size * x,
                        self.block_size * y + 200,
                        self.block_size,
                        self.block_size,
                    ),
                )

    def draw_ghost_piece(self, ghost_piece):
        for cord in ghost_piece:
            pg.draw.rect(
                self.win,
                (0, 255, 255),
                pg.Rect(
                    (cord[1] * self.block_size),
                    cord[0] * self.block_size + 200,
                    self.block_size,
                    self.block_size,
                ),
                width=5,
            )

    def draw_held_piece(self, held_piece):
        if held_piece:
            for cord in held_piece["cords"]:
                pg.draw.rect(
                    self.win,
                    held_piece["color"],
                    pg.Rect(
                        cord[1] * self.block_size,
                        cord[0] * self.block_size + (3 * self.block_size),
                        self.block_size,
                        self.block_size,
                    ),
                )
                pg.draw.rect(
                    self.win,
                    (255, 255, 255),
                    pg.Rect(
                        cord[1] * self.block_size,
                        cord[0] * self.block_size + (3 * self.block_size),
                        self.block_size,
                        self.block_size,
                    ),
                    1,
                )

    def draw_next_piece(self, next_piece):
        x_offset = 425
        y_offset = 450
        for cord in next_piece["cords"]:
            pg.draw.rect(
                self.win,
                next_piece["color"],
                pg.Rect(
                    cord[1] * self.block_size + x_offset,
                    cord[0] * self.block_size + (3 * self.block_size) + y_offset,
                    self.block_size,
                    self.block_size,
                ),
            )
            pg.draw.rect(
                self.win,
                (255, 255, 255),
                pg.Rect(
                    cord[1] * self.block_size + x_offset,
                    cord[0] * self.block_size + (3 * self.block_size) + y_offset,
                    self.block_size,
                    self.block_size,
                ),
                1,
            )

    def blit_text(self, score):
        font = pg.font.SysFont("Arial", 36)
        hold = font.render("Held Piece:", True, (255, 255, 255))
        score = font.render(f"Score: {score}", True, (255, 255, 255))
        next_piece = font.render("Next Piece:", True, (255, 255, 255))
        self.win.blit(hold, (0, 0))
        self.win.blit(score, (475, self.height_offset))
        self.win.blit(next_piece, (450, 400))
