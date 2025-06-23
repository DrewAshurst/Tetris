import yaml
import random
import copy


class Game:
    def __init__(self, config):
        self.config = config
        self.score = 0
        self.board = [
            [[0, 0, (0, 0, 0)] for i in range(int(self.config["columns"]))]
            for i in range(int(self.config["rows"]))
        ]
        self.pieces = {
            "i": {
                "cords": [[0, 3], [0, 4], [0, 5], [0, 6]],
                "color": (0, 255, 255),
                "rotations": [
                    ((2, 0), (1, 1), (0, 2), (-1, 3)),
                    ((-2, 0), (-1, -1), (0, -2), (1, -3)),
                ],
                "cur_rotation": 0,
            },
            "o": {
                "cords": [[0, 4], [0, 5], [1, 4], [1, 5]],
                "color": (255, 255, 0),
                "rotations": [((0, 0), (0, 0), (0, 0), (0, 0))],
                "cur_rotation": 0,
            },
            "j": {
                "cords": [[2, 4], [2, 5], [1, 5], [0, 5]],
                "color": (0, 0, 255),
                "rotations": [
                    ((0, -2), (-1, -1), (0, 0), (1, 1)),
                    ((2, 0), (1, -1), (0, 0), (-1, 1)),
                    ((0, 2), (1, 1), (0, 0), (-1, -1)),
                    ((-2, 0), (-1, 1), (0, 0), (1, -1)),
                ],
                "cur_rotation": 0,
            },
            "l": {
                "cords": [[0, 4], [1, 4], [2, 4], [2, 5]],
                "color": (255, 127, 0),
                "rotations": [
                    ((1, 1), (0, 0), (-1, -1), (-2, 0)),
                    ((-1, 1), (0, 0), (1, -1), (0, -2)),
                    ((-1, -1), (0, 0), (1, 1), (2, 0)),
                    ((1, -1), (0, 0), (-1, 1), (0, 2)),
                ],
                "cur_rotation": 0,
            },
            "s": {
                "cords": [[1, 3], [1, 4], [0, 4], [0, 5]],
                "color": (0, 255, 0),
                "rotations": [
                    ((1, -1), (0, 0), (1, 1), (0, 2)),
                    ((-1, 1), (0, 0), (-1, -1), (0, -2)),
                ],
                "cur_rotation": 0,
            },
            "z": {
                "cords": [[0, 3], [0, 4], [1, 4], [1, 5]],
                "color": (255, 0, 0),
                "rotations": [
                    ((2, 0), (1, 1), (0, 0), (-1, 1)),
                    ((-2, 0), (-1, -1), (0, 0), (1, -1)),
                ],
                "cur_rotation": 0,
            },
            "t": {
                "cords": [[1, 3], [0, 4], [1, 4], [1, 5]],
                "color": (128, 0, 128),
                "rotations": [
                    ((1, -1), (1, 1), (0, 0), (-1, 1)),
                    ((1, 1), (-1, 1), (0, 0), (-1, -1)),
                    ((-1, 1), (-1, -1), (0, 0), (1, -1)),
                    ((-1, -1), (1, -1), (0, 0), (1, 1)),
                ],
                "cur_rotation": 0,
            },
        }
        self.cur_piece = self.get_next_piece()
        self.next_piece = self.get_next_piece()
        self.held_piece = None
        self.ghost_piece = self.get_ghost_cords()

    def get_next_piece(self):
        return copy.deepcopy(self.pieces[random.choice(list(self.pieces.keys()))])

    def get_ghost_cords(self):
        bottom = False 
        check_ind = 1
        while not bottom:
            if any(cord[0] + check_ind > self.config['rows']-1 for cord in self.cur_piece['cords']):
                break
            if any(self.board[cord[0] + check_ind][cord[1]][1] == 1 for cord in self.cur_piece['cords']):
                break 
            check_ind += 1

        self.ghost_piece = [[cord[0] + check_ind-1, cord[1]] for cord in self.cur_piece['cords']]

            

    def hold_piece(self):
        piece = None

        for key in self.pieces:
            if self.pieces[key]["color"] == self.cur_piece["color"]:
                piece = key

        if self.held_piece and piece:
            self.cur_piece = copy.deepcopy(self.held_piece)
            self.held_piece = copy.deepcopy(self.pieces[piece])

        elif piece:
            self.held_piece = copy.deepcopy(self.pieces[piece])
            self.cur_piece = copy.deepcopy(self.next_piece) 
            self.next_piece = self.get_next_piece()

    def update_board(self):
        self.clear_lines()
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x][1] != 1:
                    self.board[y][x] = [0, 0, (0, 0, 0)]

        for cord in self.cur_piece["cords"]:
            self.board[cord[0]][cord[1]][0] = 1
            self.board[cord[0]][cord[1]][2] = self.cur_piece["color"]

    def clear_lines(self):
        lines_cleared = 0
        ind = self.config['rows']-1
        #for i in range(self.config["rows"] - 1, -1, -1):
        while ind >= 0:
            if any(val[1] != 1 for val in self.board[ind]):
                ind -= 1
                continue
            else:
                lines_cleared += 1
                for z in range(ind, -1, -1):
                    if z == 0:
                        for q in range(len(self.board[z])):
                            self.board[z][q] = [0, 0, (0, 0, 0)]
                    else:
                        self.board[z] = list(self.board[z - 1])
        if lines_cleared == 1:
            self.score += 1
        elif lines_cleared == 2:
            self.score += 4
        elif lines_cleared == 3:
            self.score += 8
        elif lines_cleared == 4:
            self.score += 20

    def rotate_piece(self):
        cords = self.cur_piece["cords"]
        rot = self.cur_piece["rotations"][self.cur_piece["cur_rotation"]]

        if any(cords[i][1] + rot[i][0] < 0 for i in range(len(cords))):
            return False

        if any(
            cords[i][1] + rot[i][0] > self.config["columns"] - 1
            for i in range(len(cords))
        ):
            return False

        for i in range(len(self.cur_piece["cords"])):
            self.cur_piece["cords"][i][0] += rot[i][1]
            self.cur_piece["cords"][i][1] += rot[i][0]

        if self.cur_piece["cur_rotation"] == len(self.cur_piece["rotations"]) - 1:
            self.cur_piece["cur_rotation"] = 0
        else:
            self.cur_piece["cur_rotation"] += 1

    def collision_check(self, dir, new_piece=False):
        
        # check right or left
        if dir == 1:
            if any(
                cord[1] + 1 > self.config["columns"] - 1
                or self.board[cord[0]][cord[1] + 1][1] == 1
                for cord in self.cur_piece["cords"]
            ):
                return False
            return [[cord[0], cord[1] + 1] for cord in self.cur_piece["cords"]]

        if dir == 0:
            if any(
                cord[1] - 1 < 0 or self.board[cord[0]][cord[1] - 1][1] == 1
                for cord in self.cur_piece["cords"]
            ):
                return False
            return [[cord[0], cord[1] - 1] for cord in self.cur_piece["cords"]]

        # check down
        if dir == -1:
            if any(
                cord[0] + 1 > self.config["rows"] - 1
                or self.board[cord[0] + 1][cord[1]][1] == 1
                for cord in self.cur_piece["cords"]
            ):
                for cord in self.cur_piece["cords"]:
                    self.board[cord[0]][cord[1]] = [1, 1, self.cur_piece["color"]]

                self.get_new_piece()
                return False

            return [[cord[0] + 1, cord[1]] for cord in self.cur_piece["cords"]]

    def get_new_piece(self):
        self.cur_piece = self.next_piece
        self.next_piece = self.get_next_piece()

    def move_piece(self, dir, new_piece=False):
        new_cords = self.collision_check(dir)
        if new_cords:
            for i in range(len(new_cords)):
                self.cur_piece["cords"] = [[x[0], x[1]] for x in new_cords]

        return self.collision_check(-1, new_piece)


if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    b = Game(config)
