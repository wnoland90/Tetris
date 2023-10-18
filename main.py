import pygame
import time
from random import randint

from Game import Z_block, I_block, S_block, O_block, T_block, L_block, J_block, BOARD


def summon_block():
    blocks = [Z_block(), I_block(), S_block(), O_block(), T_block(), L_block(), J_block()]
    return blocks[randint(0, 6)]


def main():
    pygame.init()

    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    BACKGROUND_COLOR = (201, 130, 81)
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    SCREEN.fill(BACKGROUND_COLOR)
    pygame.display.set_caption("TETRIS")
    SCREEN.fill(BACKGROUND_COLOR)
    pygame.display.flip()

    then = time.time()
    board = BOARD()
    board.make_board()

    FPS = board.levels[board.level]['FPS']
    FRAMES = 0
    newblock = True
    running = True
    block = None
    while running:
        if newblock:
            block = summon_block()
            block.spawn(board)
            newblock = False
            board.make_board()

        SCREEN.blit(board.board, (int((SCREEN_WIDTH - board.width) / 2), -150))

        keys = pygame.key.get_pressed()
        print(keys[81])


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    block.left(board)
                elif event.key == pygame.K_RIGHT:
                    block.right(board)
                elif event.key == pygame.K_DOWN:
                    block.gravity(board)
                elif event.key == pygame.K_q:
                    block.rotate(board, 'left')
                elif event.key == pygame.K_e:
                    block.rotate(board, 'right')
        if block.stop == True:
            newblock = True
            FRAMES = FPS * 30
            for tile in block.tiles:
                board.grid[tile.y][tile.x] = tile
            FPS = board.update_score()
            board.make_board()
            running = board.game_is_over()

        if (FRAMES == FPS * 30) or (int(time.time() - then) >= 1):
            FRAMES = 0
            block.gravity(board)
            then = time.time()
        else:
            FRAMES += 1

        pygame.display.update()

    pygame.quit()
    print(board.score)

main()
