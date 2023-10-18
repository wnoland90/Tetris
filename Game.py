from pygame import Surface, draw, Rect

# The board
class BOARD:

    def __init__(self, block_size=30, width=10, height=25, background_color=tuple([0, 0, 0])):
        self.background_color = background_color
        self.block_size = block_size
        self.width = width * self.block_size
        self.height = height * self.block_size
        self.level = 0
        self.lines_cleared = 0
        self.score = 0
        self.grid = [[0 for _ in range(width)] for p in range(height)]
        self.levels = {
            0: {'FPS': 48, 'lines': 10},
            1: {'FPS': 43, 'lines': 20},
            2: {'FPS': 38, 'lines': 30},
            3: {'FPS': 33, 'lines': 40},
            4: {'FPS': 28, 'lines': 50},
            5: {'FPS': 23, 'lines': 60},
            6: {'FPS': 18, 'lines': 70},
            7: {'FPS': 13, 'lines': 80},
            8: {'FPS': 8, 'lines': 90},
            9: {'FPS': 6, 'lines': 100},
            10: {'FPS': 5, 'lines': 100},
            11: {'FPS': 5, 'lines': 100},
            12: {'FPS': 5, 'lines': 100},
            13: {'FPS': 4, 'lines': 100},
            14: {'FPS': 4, 'lines': 100},
            15: {'FPS': 4, 'lines': 100},
            16: {'FPS': 3, 'lines': 110},
            17: {'FPS': 3, 'lines': 120},
            18: {'FPS': 3, 'lines': 130},
            19: {'FPS': 2, 'lines': 140},
            20: {'FPS': 2, 'lines': 150},
            21: {'FPS': 2, 'lines': 160},
            22: {'FPS': 2, 'lines': 170},
            23: {'FPS': 2, 'lines': 180},
            24: {'FPS': 2, 'lines': 190},
            25: {'FPS': 2, 'lines': 200},
            26: {'FPS': 2, 'lines': 200},
            27: {'FPS': 2, 'lines': 200},
            28: {'FPS': 2, 'lines': 200},
            29: {'FPS': 1}
        }
        self.board = Surface((self.width, self.height))

    def game_is_over(self):
        if self.grid[4][3] != 0 or self.grid[4][4] != 0 or self.grid[4][5] != 0 or self.grid[4][6] != 0:
            return False
        return True

    def make_board(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != 0:
                    draw.rect(
                        surface=self.board,
                        color=self.grid[y][x].color,
                        rect=self.grid[y][x].block
                    )
                elif self.grid[y][x] == 0:
                    draw.rect(
                        surface=self.board,
                        color=self.background_color,
                        rect=Rect((x * self.block_size, y * self.block_size), (self.block_size, self.block_size))
                    )

    def update_score(self):
        clear_count = 0
        row = len(self.grid) - 1
        while row != 0:
            if all(i != 0 for i in self.grid[row]):
                clear_count += 1
                self.grid.pop(row)
                self.grid.insert(0, [0 for _ in range(self.width // self.block_size)])
            else:
                row -= 1

        self.lines_cleared += clear_count
        if self.level == 0:
            if clear_count == 4:
                self.score += (800)
            elif clear_count == 3:
                self.score += (500)
            elif clear_count == 2:
                self.score += (300)
            elif clear_count == 1:
                self.score += (100)
        if clear_count == 4:
            self.score += (800 * self.level)
        elif clear_count == 3:
            self.score += (500 * self.level)
        elif clear_count == 2:
            self.score += (300 * self.level)
        elif clear_count == 1:
            self.score += (100 * self.level)
        if self.lines_cleared == self.levels[self.level]['lines']:
            self.level += 1
        self.board.fill(self.background_color)
        for row in self.grid:
            for tile in row:
                if tile != 0:
                    tile.block.move_ip(0, clear_count * self.block_size)
        return self.levels[self.level]['FPS']


# The tiles
class Tiles:

    def __init__(self, x, y, block=None, name=None, color=None, block_size=30, stop=False, owner=None):
        self.x = x
        self.y = y
        self.block = block
        self.name = name
        self.color = color
        self.block_size = block_size
        self.stop = stop
        self.owner = owner

    def __str__(self):
        return f"{self.owner}"

# The Shape Object
class Shape:

    def __init__(self, name=None, color=None, block_size=30, positions=None, x=None, y=None):
        self.name = name
        self.color = color
        self.block_size = block_size
        self.position = 0
        self.positions = positions
        self.stop = False
        self.x = x
        self.y = y

    def clean_up(self, surface: BOARD):
        for tile in self.tiles:
            if 0 <= tile.x < 10 and tile.y <= surface.height // surface.block_size:
                surface.grid[tile.y][tile.x] = 0

    def spawn(self, surface: BOARD):
        surface.make_board()
        for tile in self.tiles:
            draw.rect(surface=surface.board, color=self.color, rect=tile.block)

    def gravity(self, surface: BOARD):
        can_continue = True
        for tile in self.tiles:
            if tile.y + 1 < len(surface.grid):
                if (tile.y + 1 > (surface.height // surface.block_size)) or (surface.grid[tile.y + 1][tile.x] != 0 and surface.grid[tile.y + 1][tile.x].stop):
                    can_continue = False
                    self.stop = True
                    break
            if tile.y + 1 == len(surface.grid):
                self.stop = True
                can_continue = False
                break
        if can_continue:
            self.clean_up(surface)
            self.y += 1
            for tile in self.tiles:
                tile.y += 1
                surface.grid[tile.y][tile.x] = tile
                tile.block.move_ip((0, self.block_size))
        else:
            for tile in self.tiles:
                tile.stop = True
        self.spawn(surface)

    def left(self, surface: BOARD):
        can_continue = True
        for tile in self.tiles:
            if (tile.x - 1 < 0) or (surface.grid[tile.y][tile.x - 1] != 0 and surface.grid[tile.y][tile.x - 1].stop):
                can_continue = False
                break
        if can_continue:
            self.x -= 1
            self.clean_up(surface)
            for tile in self.tiles:
                tile.x -= 1
                surface.grid[tile.y][tile.x] = tile
                tile.block.move_ip((-1 * self.block_size, 0))
        self.spawn(surface)

    def right(self, surface: BOARD):
        can_continue = True
        for tile in self.tiles:
            if (tile.x + 1 >= 10) or (surface.grid[tile.y][tile.x + 1] != 0 and surface.grid[tile.y][tile.x + 1].stop):
                can_continue = False
                break
        if can_continue:
            self.clean_up(surface)
            self.x += 1
            for tile in self.tiles:
                tile.x += 1
                surface.grid[tile.y][tile.x] = tile
                tile.block.move_ip((self.block_size, 0))
        self.spawn(surface)

    def can_rotate(self, surface: BOARD, new_x, new_y):
        if (len(surface.grid) <= new_y) or len(surface.grid[0]) <= new_x or new_x < 0:
            return False
        if surface.grid[new_y][new_x] != 0:
            if surface.grid[new_y][new_x].stop:
                return False
        return True

    def rotate(self, surface: BOARD, direction: str):
        if direction.lower() == "left":
            if self.position == 0:
                new_position = 3
            else:
                new_position = self.position - 1
        elif direction.lower() == "right":
            if self.position == 3:
                new_position = 0
            else:
                new_position = self.position + 1

        # Check to see if can rotate
        checkpoint1 = False
        for ind, tile in enumerate(self.tiles):
            if not self.can_rotate(surface=surface, new_y=(self.positions[new_position][ind][1] + tile.y), new_x=(self.positions[new_position][ind][0] + tile.x)):
                checkpoint1 = True
                break

        # If not move over the direction it came from
        if checkpoint1:
            if all(self.can_rotate(surface=surface, new_x=(self.positions[new_position][ind][0] + 1 + tile.x),
                                   new_y=(tile.y + self.positions[new_position][ind][1])) for ind, tile in enumerate(self.tiles)):
                self.clean_up(surface)
                for ind, tile in enumerate(self.tiles):
                    tmpx = tile.x
                    tmpy = tile.y
                    tile.x = self.positions[new_position][ind][0] + self.x + 1
                    tile.y = self.positions[new_position][ind][1] + self.y
                    surface.grid[tile.y][tile.x] = tile
                    tile.block.move_ip((tile.x - tmpx) * self.block_size, (tile.y - tmpy) * self.block_size)
                self.position = new_position
            elif all(self.can_rotate(surface=surface, new_x=(self.positions[new_position][ind][0] + -1 + tile.x),
                                   new_y=(tile.y + self.positions[new_position][ind][1])) for ind, tile in enumerate(self.tiles)):
                self.clean_up(surface)
                for ind, tile in enumerate(self.tiles):
                    tmpx = tile.x
                    tmpy = tile.y
                    tile.x = self.positions[new_position][ind][0] + self.x - 1
                    tile.y = self.positions[new_position][ind][1] + self.y
                    surface.grid[tile.y][tile.x] = tile
                    tile.block.move_ip((tile.x - tmpx) * self.block_size, (tile.y - tmpy) * self.block_size)
                self.position = new_position
        else:
            self.clean_up(surface)
            for ind, tile in enumerate(self.tiles):
                tmpx = tile.x
                tmpy = tile.y
                tile.x = self.positions[new_position][ind][0] + self.x
                tile.y = self.positions[new_position][ind][1] + self.y
                if 0 <= tile.x < 10 and tile.y <= surface.height // surface.block_size:
                    surface.grid[tile.y][tile.x] = tile
                tile.block.move_ip(((tile.x - tmpx) * self.block_size, (tile.y - tmpy) * self.block_size))
            while any(i.x < 0 for i in self.tiles):
                self.clean_up(surface)
                for tile in self.tiles:
                    tile.x += 1
                    tile.block.move_ip(self.block_size, 0)
                    surface.grid[tile.y][tile.x] = tile
            while any(i.x >= 10 for i in self.tiles):
                self.clean_up(surface)
                for tile in self.tiles:
                    tile.x -= 1
                    tile.block.move_ip(-1 * self.block_size, 0)
                    surface.grid[tile.y][tile.x] = tile
            self.position = new_position
        self.spawn(surface)


# The Blocks
class S_block(Shape):

    def __init__(self, block_size=30):
        super().__init__(
            name='S_Block',
            color=(255, 0, 0),
            block_size=block_size,
            positions=[
                [
                    (-1, 0), (0, 0), (0, -1), (1, -1)
                ],
                [
                    (0, -1), (0, 0), (1, 0), (1, 1)
                ],
                [
                    (1, 0), (0, 0), (0, 1), (-1, 1)
                ],
                [
                    (0, 1), (0, 0), (-1, 0), (-1, -1)
                ],
            ],
            x=5,
            y=4
        )
        self.tiles = [
            Tiles(
                color=self.color,
                name=0,
                x=(self.positions[self.position][0][0] + self.x),
                y=(self.positions[self.position][0][1] + self.y),
                owner="S",
                block=Rect((
                    (self.positions[0][0][0] + self.x) * block_size, (self.positions[0][0][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=1,
                x=(self.positions[self.position][1][0] + self.x),
                y=(self.positions[self.position][1][1] + self.y),
                owner="S",
                block=Rect(
                    ((self.positions[0][1][0] + self.x) * block_size, (self.positions[0][1][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=2,
                x=(self.positions[self.position][2][0] + self.x),
                y=(self.positions[self.position][2][1] + self.y),
                owner="S",
                block=Rect(
                    ((self.positions[0][2][0] + self.x) * block_size, (self.positions[0][2][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=3,
                x=(self.positions[self.position][3][0] + self.x),
                y=(self.positions[self.position][3][1] + self.y),
                owner="S",
                block=Rect(
                    ((self.positions[0][3][0] + self.x) * block_size, (self.positions[0][3][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
        ]


class I_block(Shape):

    def __init__(self, block_size=30):
        super().__init__(
            name='I_Block',
            color=(0, 255, 255),
            block_size=block_size,
            positions=[
                [
                    (-1, 0), (0, 0), (1, 0), (2, 0)
                ],
                [
                    (1, -2), (1, -1), (1, 0), (1, 1)
                ],
                [
                    (2, 1), (1, 1), (0, 1), (-1, 1)
                ],
                [
                    (-1, 1), (-1, 0), (-1, -1), (-1, -2)
                ],
            ],
            x=3,
            y=4
        )
        self.tiles = [
            Tiles(
                color=self.color,
                name=0,
                x=(self.positions[self.position][0][0] + self.x),
                y=(self.positions[self.position][0][1] + self.y),
                owner="I",
                block=Rect((
                    (self.positions[0][0][0] + self.x) * block_size, (self.positions[0][0][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=1,
                x=(self.positions[self.position][1][0] + self.x),
                y=(self.positions[self.position][1][1] + self.y),
                owner="I",
                block=Rect(
                    ((self.positions[0][1][0] + self.x) * block_size, (self.positions[0][1][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=2,
                x=(self.positions[self.position][2][0] + self.x),
                y=(self.positions[self.position][2][1] + self.y),
                owner="I",
                block=Rect(
                    ((self.positions[0][2][0] + self.x) * block_size, (self.positions[0][2][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=3,
                x=(self.positions[self.position][3][0] + self.x),
                y=(self.positions[self.position][3][1] + self.y),
                owner="I",
                block=Rect(
                    ((self.positions[0][3][0] + self.x) * block_size, (self.positions[0][3][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
        ]


class Z_block(Shape):

    def __init__(self, block_size=30):
        super().__init__(
            name='Z_Block',
            color=(0, 255, 0),
            block_size=block_size,
            positions=[
                [
                    (-1, -1), (0, -1), (0, 0), (1, 0)
                ],
                [
                    (1, -1), (1, 0), (0, 0), (0, 1)
                ],
                [
                    (1, 1), (0, 1), (0, 0), (-1, 0)
                ],
                [
                    (-1, 1), (-1, 0), (0, 0), (0, -1)
                ],
            ],
            x=4,
            y=4
        )
        self.tiles = [
            Tiles(
                color=self.color,
                name=0,
                x=(self.positions[self.position][0][0] + self.x),
                y=(self.positions[self.position][0][1] + self.y),
                owner="Z",
                block=Rect((
                    (self.positions[0][0][0] + self.x) * block_size, (self.positions[0][0][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=1,
                x=(self.positions[self.position][1][0] + self.x),
                y=(self.positions[self.position][1][1] + self.y),
                owner="Z",
                block=Rect(
                    ((self.positions[0][1][0] + self.x) * block_size, (self.positions[0][1][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=2,
                x=(self.positions[self.position][2][0] + self.x),
                y=(self.positions[self.position][2][1] + self.y),
                owner="Z",
                block=Rect(
                    ((self.positions[0][2][0] + self.x) * block_size, (self.positions[0][2][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=3,
                x=(self.positions[self.position][3][0] + self.x),
                y=(self.positions[self.position][3][1] + self.y),
                owner="Z",
                block=Rect(
                    ((self.positions[0][3][0] + self.x) * block_size, (self.positions[0][3][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
        ]


class O_block(Shape):

    def __init__(self, block_size=30):
        super().__init__(
            name='O_Block',
            color=(255, 255, 0),
            block_size=block_size,
            positions=[
                [
                    (0, -1), (1, -1), (0, 0), (1, 0)
                ],
                [
                    (0, 0), (0, -1), (1, 0), (1, -1)
                ],
                [
                    (1, 0), (0, 0), (1, -1), (0, -1)
                ],
                [
                    (1, -1), (1, 0), (0, -1), (0, 0)
                ],
            ],
            x=4,
            y=4
        )
        self.tiles = [
            Tiles(
                color=self.color,
                name=0,
                x=(self.positions[self.position][0][0] + self.x),
                y=(self.positions[self.position][0][1] + self.y),
                owner="o",
                block=Rect((
                    (self.positions[0][0][0] + self.x) * block_size, (self.positions[0][0][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=1,
                x=(self.positions[self.position][1][0] + self.x),
                y=(self.positions[self.position][1][1] + self.y),
                owner="o",
                block=Rect(
                    ((self.positions[0][1][0] + self.x) * block_size, (self.positions[0][1][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=2,
                x=(self.positions[self.position][2][0] + self.x),
                y=(self.positions[self.position][2][1] + self.y),
                owner="o",
                block=Rect(
                    ((self.positions[0][2][0] + self.x) * block_size, (self.positions[0][2][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=3,
                x=(self.positions[self.position][3][0] + self.x),
                y=(self.positions[self.position][3][1] + self.y),
                owner="o",
                block=Rect(
                    ((self.positions[0][3][0] + self.x) * block_size, (self.positions[0][3][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
        ]

    def rotate(self, surface: BOARD, direction: str):
        pass


class T_block(Shape):

    def __init__(self, block_size=30):
        super().__init__(
            name='T_Block',
            color=(75, 0, 130),
            block_size=block_size,
            positions=[
                [
                    (-1, 0), (0, 0), (1, 0), (0, -1)
                ],
                [
                    (0, -1), (0, 0), (0, 1), (1, 0)
                ],
                [
                    (1, 0), (0, 0), (-1, 0), (0, 1)
                ],
                [
                    (0, 1), (0, 0), (0, -1), (-1, 0)
                ],
            ],
            x=4,
            y=4
        )
        self.tiles = [
            Tiles(
                color=self.color,
                name=0,
                x=(self.positions[self.position][0][0] + self.x),
                y=(self.positions[self.position][0][1] + self.y),
                owner="T",
                block=Rect((
                    (self.positions[0][0][0] + self.x) * block_size, (self.positions[0][0][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=1,
                x=(self.positions[self.position][1][0] + self.x),
                y=(self.positions[self.position][1][1] + self.y),
                owner="T",
                block=Rect(
                    ((self.positions[0][1][0] + self.x) * block_size, (self.positions[0][1][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=2,
                x=(self.positions[self.position][2][0] + self.x),
                y=(self.positions[self.position][2][1] + self.y),
                owner="T",
                block=Rect(
                    ((self.positions[0][2][0] + self.x) * block_size, (self.positions[0][2][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=3,
                x=(self.positions[self.position][3][0] + self.x),
                y=(self.positions[self.position][3][1] + self.y),
                owner="T",
                block=Rect(
                    ((self.positions[0][3][0] + self.x) * block_size, (self.positions[0][3][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
        ]


class J_block(Shape):

    def __init__(self, block_size=30):
        super().__init__(
            name='J_Block',
            color=(0, 0, 255),
            block_size=block_size,
            positions=[
                [
                    (-1, -1), (-1, 0), (0, 0), (1, 0)
                ],
                [
                    (1, -1), (0, -1), (0, 0), (0, 1)
                ],
                [
                    (1, 1), (1, 0), (0, 0), (-1, 0)
                ],
                [
                    (-1, 1), (0, 1), (0, 0), (0, -1)
                ],
            ],
            x=5,
            y=4
        )
        self.tiles = [
            Tiles(
                color=self.color,
                name=0,
                x=(self.positions[self.position][0][0] + self.x),
                y=(self.positions[self.position][0][1] + self.y),
                owner="J",
                block=Rect((
                    (self.positions[0][0][0] + self.x) * block_size, (self.positions[0][0][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=1,
                x=(self.positions[self.position][1][0] + self.x),
                y=(self.positions[self.position][1][1] + self.y),
                owner="J",
                block=Rect(
                    ((self.positions[0][1][0] + self.x) * block_size, (self.positions[0][1][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=2,
                x=(self.positions[self.position][2][0] + self.x),
                y=(self.positions[self.position][2][1] + self.y),
                owner="J",
                block=Rect(
                    ((self.positions[0][2][0] + self.x) * block_size, (self.positions[0][2][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=3,
                x=(self.positions[self.position][3][0] + self.x),
                y=(self.positions[self.position][3][1] + self.y),
                owner="J",
                block=Rect(
                    ((self.positions[0][3][0] + self.x) * block_size, (self.positions[0][3][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
        ]


class L_block(Shape):

    def __init__(self, block_size=30):
        super().__init__(
            name='L_Block',
            color=(255, 100, 0),
            block_size=block_size,
            positions=[
                [
                    (-1, 0), (0, 0), (1, 0), (1, -1)
                ],
                [
                    (0, -1), (0, 0), (0, 1), (1, 1)
                ],
                [
                    (1, 0), (0, 0), (-1, 0), (-1, 1)
                ],
                [
                    (0, -1), (0, 0), (0, 1), (-1, 1)
                ],
            ],
            x=4,
            y=4
        )
        self.tiles = [
            Tiles(
                color=self.color,
                name=0,
                x=(self.positions[self.position][0][0] + self.x),
                y=(self.positions[self.position][0][1] + self.y),
                owner="L",
                block=Rect((
                    (self.positions[0][0][0] + self.x) * block_size, (self.positions[0][0][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=1,
                x=(self.positions[self.position][1][0] + self.x),
                y=(self.positions[self.position][1][1] + self.y),
                owner="L",
                block=Rect(
                    ((self.positions[0][1][0] + self.x) * block_size, (self.positions[0][1][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=2,
                x=(self.positions[self.position][2][0] + self.x),
                y=(self.positions[self.position][2][1] + self.y),
                owner="L",
                block=Rect(
                    ((self.positions[0][2][0] + self.x) * block_size, (self.positions[0][2][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
            Tiles(
                color=self.color,
                name=3,
                x=(self.positions[self.position][3][0] + self.x),
                y=(self.positions[self.position][3][1] + self.y),
                owner="L",
                block=Rect(
                    ((self.positions[0][3][0] + self.x) * block_size, (self.positions[0][3][1] + self.y) * block_size),
                    (block_size, block_size))
            ),
        ]