import pygame as pg
import random

pg.init()
win = pg.display.set_mode((800, 800))
pg.display.set_caption("Tetris")

pg.font.init(), 
my_font = pg.font.SysFont('Times New Roman', 30)

clock = pg.time.Clock()

tetrisLogo = pg.image.load("tetrisLogo.png")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PIECES = ["square", "line", "s", "z", "backL", "l", "t"]

class currentPiece:
    def __init__(self, piece):
        self.id = piece
        if piece == "square":
            self.color = (240, 240, 0)
            self.cords = [[120, 200], [150, 200], [120, 230], [150, 230]]
            self.shifts = [[(0, 0), (0, 0), (0, 0), (0, 0)]]
            self.rotation = 0

        if piece == "line":
            self.color = (0, 240, 240)
            self.cords = [[90, 200], [120, 200], [150, 200], [180, 200]]
            self.shifts = [[(60, 0), (30, 30), (0, 60), (-30, 90)], [(-60, 0), (-30, -30), (0, -60), (30, -90)]]
            self.rotation = 0

        if piece == "s":
            self.color = (0, 240, 0)
            self.cords = [[90, 230], [120, 230], [120, 200], [150, 200]]
            self.shifts = [[(60, 30), (30, 0), (0, 30), (-30, 0)], [(-60, -30), (-30, 0), (0, -30), (30, 0)]]
            self.rotation = 0
        
        if piece == "z":
            self.color = (240, 0, 0)
            self.cords = [[90, 200], [120, 200], [120, 230], [150, 230]]
            self.shifts = [[(60, 30), (30, 0), (0, 30), (-30, 0)], [(-60, -30), (-30, 0), (0, -30), (30, 0)]]
            self.rotation = 0

        if piece == "backL":
            self.color = (0, 0, 240)
            self.cords = [[90, 200], [90, 230], [120, 230], [150, 230]]
            self.shifts = [[(60, 0), (30, -30), (0, 0), (-30, 30)], [(30, 30), (60, 0), (30, -30), (0, -60)],
                           [(-60, 30), (-30, 60), (0, 30), (30, 0)], [(-30, -60), (-60, -30), (-30, 0), (0, 30)]]
            self.rotation = 0
        
        if piece == "l":
            self.color = (240, 160, 0)
            self.cords = [[90, 230], [120, 230], [150, 230], [150, 200]]
            self.shifts = [[(30, -30), (0, 0), (-30, 30), (0, 60)], [(30, 30), (0, 0), (-30, -30), (-60, 0)],
                           [(-30, 30), (0, 0), (30, -30), (0, -60)], [(-30, -30), (0, 0), (30, 30), (60, 0)]]
            self.rotation = 0
        
        if piece == "t":
            self.color = (160, 0, 240)
            self.cords = [[90, 230], [120, 230], [150, 230], [120, 200]]
            self.shifts = [[(30, -30), (0, 0), (-30, 30), (30, 30)], [(30, 30), (0, 0), (-30, -30), (-30, 30)],
                           [(-30, 30), (0, 0), (30, -30), (-30, -30)], [(-30, -30), (0, 0), (30, 30), (30, -30)]]
            self.rotation = 0

    def drawPiece(self):
        for i in self.cords:
            pg.draw.rect(win, self.color, pg.Rect(i[0], i[1], 30, 30))

    def rotatePiece(self):
        if self.rotation == len(self.shifts):
            self.rotation = 0
        for i in range(len(self.cords)):
            shift = self.shifts[self.rotation][i]
            self.cords[i][0] += shift[0]
            self.cords[i][1] += shift[1]
        for i in self.cords:
            if i[0] < 0 or i[0] >= 300:
                for i in range(len(self.cords)):
                    shift = self.shifts[self.rotation][i]
                    self.cords[i][0] -= shift[0]
                    self.cords[i][1] -= shift[1]
                return
            if i[1] < 200 or i[1] > 770:
                for i in range(len(self.cords)):
                    shift = self.shifts[self.rotation][i]
                    self.cords[i][0] -= shift[0]
                    self.cords[i][1] -= shift[1]
                return

        self.rotation += 1

def drawGameBoard():
    for y, lis in enumerate(gameboard):
        for x in range(len(lis)):
            if gameboard[y][x] != 0:
                pg.draw.rect(win, gameboard[y][x], pg.Rect(x * 30, (y * 30) + 200, 30, 30))

def create_gameboard():
    board = []
    for i in range(20):
        board.append([0 for i in range(10)])

    return board 

def drawGrid():
    blockSize = 30 #Set the size of the grid block
    for x in range(0, 300, blockSize):
        for y in range(200, 800, blockSize):
            rect = pg.Rect(x, y, blockSize, blockSize)
            pg.draw.rect(win, WHITE, rect, 1)

def drawHoldPiece():
    pg.draw.rect(win, WHITE, (75, 25, 150, 150), 1)
    if heldPiece == "line":
        cords = [[90, 70], [120, 70], [150, 70], [180, 70]]
        for i in cords:
            pg.draw.rect(win, (0, 240, 240), pg.Rect(i[0], i[1], 30, 30))
    if heldPiece == "square":
        cords = [[120, 70], [150, 70], [120, 100], [150, 100]]
        for i in cords:
            pg.draw.rect(win, (240, 240, 0), pg.Rect(i[0], i[1], 30, 30))
    if heldPiece == "s":
        cords = [[165, 55], [135, 55], [135, 85], [105, 85]]
        for i in cords:
            pg.draw.rect(win, (0, 240, 0), pg.Rect(i[0], i[1], 30, 30))
    if heldPiece == "z":
        cords = [[105, 55], [135, 55], [135, 85], [165, 85]]
        for i in cords:
            pg.draw.rect(win, (240, 0, 0), pg.Rect(i[0], i[1], 30, 30))
    if heldPiece == "backL":
        cords = [[105, 115], [135, 115], [135, 85], [135, 55]]
        for i in cords:
            pg.draw.rect(win, (0, 0, 240), pg.Rect(i[0], i[1], 30, 30))
    if heldPiece == "l":
        cords = [[165, 115], [135, 115], [135, 85], [135, 55]]
        for i in cords:
            pg.draw.rect(win, (240, 160, 0), pg.Rect(i[0], i[1], 30, 30))
    if heldPiece == "t":
        cords = [[135, 85], [105, 115], [135, 115], [165, 115]]
        for i in cords:
            pg.draw.rect(win, (160, 0, 240), pg.Rect(i[0], i[1], 30, 30))

def drawNextPiece():
    pg.draw.rect(win, WHITE, (575, 25, 150, 150), 1)
    if nextPiece == "line":
        cords = [[590, 70], [620, 70], [650, 70], [680, 70]]
        for i in cords:
            pg.draw.rect(win, (0, 240, 240), pg.Rect(i[0], i[1], 30, 30))
    if nextPiece == "square":
        cords = [[620, 70], [650, 70], [620, 100], [650, 100]]
        for i in cords:
            pg.draw.rect(win, (240, 240, 0), pg.Rect(i[0], i[1], 30, 30))
    if nextPiece == "s":
        cords = [[665, 55], [635, 55], [635, 85], [605, 85]]
        for i in cords:
            pg.draw.rect(win, (0, 240, 0), pg.Rect(i[0], i[1], 30, 30))
    if nextPiece == "z":
        cords = [[605, 55], [635, 55], [635, 85], [665, 85]]
        for i in cords:
            pg.draw.rect(win, (240, 0, 0), pg.Rect(i[0], i[1], 30, 30))
    if nextPiece == "backL":
        cords = [[605, 115], [635, 115], [635, 85], [635, 55]]
        for i in cords:
            pg.draw.rect(win, (0, 0, 240), pg.Rect(i[0], i[1], 30, 30))
    if nextPiece == "l":
        cords = [[665, 115], [635, 115], [635, 85], [635, 55]]
        for i in cords:
            pg.draw.rect(win, (240, 160, 0), pg.Rect(i[0], i[1], 30, 30))
    if nextPiece == "t":
        cords = [[635, 85], [605, 115], [635, 115], [665, 115]]
        for i in cords:
            pg.draw.rect(win, (160, 0, 240), pg.Rect(i[0], i[1], 30, 30))


def drawScreen():
    win.fill(BLACK)
    win.blit(tetrisLogo, (275, 25))
    message = my_font.render('Score: ' + str(score), False, (255, 255, 255))
    win.blit(message, (375, 200))
    
    drawGameBoard()
    piece.drawPiece()
    drawGrid()
    drawHoldPiece()
    drawNextPiece()
    
def checkClearedLines():
    clearedLines = 0
    for i in range(len(gameboard)):
        if 0 not in gameboard[i]:
            clearedLines += 1
            for x in range(i + 1):
                if i - x == 0:
                    gameboard[i - x] = [0 for i in range(10)]
                else:
                    gameboard[i - x] = gameboard[i - x - 1]
    if clearedLines == 0:
        return 0
    if clearedLines == 1:
        return 1
    if clearedLines == 2:
        return 4
    if clearedLines == 3:
        return 10
    if clearedLines == 4:
        return 20

def movePieceDown(piece):
    for i in piece.cords:
                    i[1] += 30
    for i in piece.cords:
        if i[1] == 770 or gameboard[int((i[1] - 200) / 30) + 1][int(i[0] / 30)] != 0:
            for i in piece.cords:
                gameboard[int((i[1] - 200) / 30)][int(i[0] / 30)] = piece.color
            checkClearedLines()
            piece = currentPiece(PIECES[random.randint(0, 6)])
            return piece 
    return piece

def movePieceDownSpace(piece, nextPiece):
    while True:
        for i in piece.cords:
                        i[1] += 30
        for i in piece.cords:
            if i[1] == 770 or gameboard[int((i[1] - 200) / 30) + 1][int(i[0] / 30)] != 0:
                for i in piece.cords:
                    gameboard[int((i[1] - 200) / 30)][int(i[0] / 30)] = piece.color
                
                piece = currentPiece(nextPiece)
                nextPiece = PIECES[random.randint(0, 6)]
                return piece , nextPiece

gameboard = create_gameboard()

piece = currentPiece(PIECES[random.randint(0, 6)])
run = True
fall_time = 0

heldPiece = ""
nextPiece = PIECES[random.randint(0, 6)]

score = 0

while run:
    move = True
    drawScreen()

    fall_speed = 0.97
    fall_time += clock.get_rawtime()
    clock.tick()
    if fall_time/1000 >= fall_speed:
        fall_time = 0
        piece = movePieceDown(piece)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                piece = movePieceDown(piece)
                
            if event.key == pg.K_RIGHT:
                for i in piece.cords:
                    if i[0] + 30 >= 300 or gameboard[int((i[1] - 200) / 30)][int(i[0] / 30) + 1] != 0:
                        move = False
                        break
                if move:
                    for i in piece.cords:
                        i[0] += 30
                for i in piece.cords:
                    if i[1] == 770 or gameboard[int((i[1] - 200) / 30) + 1][int(i[0] / 30)] != 0:
                        for i in piece.cords:
                            gameboard[int((i[1] - 200) / 30)][int(i[0] / 30)] = piece.color
                        score += checkClearedLines()
                        piece = currentPiece(nextPiece)
                        nextPiece = PIECES[random.randint(0, 6)]
                        break 

            if event.key == pg.K_LEFT:
                for i in piece.cords:
                    if i[0] - 30 < 0 or gameboard[int((i[1] - 200) / 30)][int(i[0] / 30) - 1] != 0:
                        move = False
                        break
                if move:
                    for i in piece.cords:
                        i[0] -= 30
                for i in piece.cords:
                    if i[1] == 770 or gameboard[int((i[1] - 200) / 30) + 1][int(i[0] / 30)] != 0:
                        for i in piece.cords:
                            gameboard[int((i[1] - 200) / 30)][int(i[0] / 30)] = piece.color
                        score += checkClearedLines()
                        piece = currentPiece(nextPiece)
                        nextPiece = PIECES[random.randint(0, 6)]
                        break 

            if event.key == pg.K_UP:
                piece.rotatePiece()
            
            if event.key == pg.K_SPACE:
                piece, nextPiece = movePieceDownSpace(piece, nextPiece)
                score += checkClearedLines()

            if event.key == pg.K_LSHIFT:
                if heldPiece == "":
                    heldPiece = piece.id 
                    piece = currentPiece(nextPiece)
                    nextPiece = PIECES[random.randint(0, 6)]
                else:
                    old = heldPiece
                    heldPiece = piece.id 
                    piece = currentPiece(old)
    
    pg.display.flip()
    
pg.quit()






