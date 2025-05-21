import pygame
from pygame.locals import *
import sys
import random
import copy

# 定数
MAX_ROW = 20
MAX_COL = 10
BLOCK_SIZE = 35
BOARD_OFFSET_X = 30
BOARD_OFFSET_Y = 30

class Block:
    def __init__(self, block_type):
        self.shapes = [[], [],  # empty block and wall
                       [[0, -1], [0, 0], [0, 1], [0, 2]],  # I block
                       [[-1, -1], [0, -1], [0, 0], [0, 1]],  # J block
                       [[0, -1], [0, 0], [0, 1], [-1, 1]],  # L block
                       [[0, -1], [0, 0], [-1, 0], [-1, 1]],  # S block
                       [[-1, -1], [-1, 0], [0, 0], [0, 1]],  # Z block
                       [[0, -1], [0, 0], [-1, 0], [0, 1]],  # T block
                       [[0, 0], [-1, 0], [0, 1], [-1, 1]]]  # square

        self.block_type = block_type
        self.shape = copy.deepcopy(self.shapes[block_type])
        self.row = 1  # initial position
        self.col = 5
        self.drop_rate = 60  # 固定の落下速度
        self.count = 0

    def move(self, board, direction):  # direction down:0 left:1 right:2
        if direction == 0 and self.moveable(board, [1, 0]):
            self.row += 1
        elif direction == 1 and self.moveable(board, [0, -1]):
            self.col -= 1
        elif direction == 2 and self.moveable(board, [0, 1]):
            self.col += 1

    def moveable(self, board, direction):
        drow, dcol = direction

        for dx in self.shape:
            row = self.row + dx[0] + drow
            col = self.col + dx[1] + dcol
            if 0 <= row < MAX_ROW + 3 and 0 <= col < MAX_COL + 2 and board[row][col] != 0:
                return False

        return True

    def drop(self, board):
        if self.count < self.drop_rate:
            self.count += 1
            return 0
        elif self.moveable(board, [1, 0]):
            self.count = 0
            self.row += 1
            return 0
        else:
            return 1  # make new block

    def place(self, board):
        for dx in self.shape:
            row = self.row + dx[0]
            col = self.col + dx[1]
            if not (2 <= row < MAX_ROW + 2 and 1 <= col < MAX_COL + 1):
                return 1 # ゲームオーバー
            board[row][col] = self.block_type
        return 0

    '''
    ブロックこうかとん変更プログラム➀
    '''
    def draw(self, screen, block_images):
        for row_offset, col_offset in self.shape:#降ってくるブロック(こうかとん)表示する
            row = self.row + row_offset
            col = self.col + col_offset
            if row > 1:
                screen.blit(block_images[self.block_type],
                        (BOARD_OFFSET_X + BLOCK_SIZE * col,
                         BOARD_OFFSET_Y + BLOCK_SIZE * (row - 2)))
    '''
    ブロックこうかとん変更プログラム➀ここまで
    '''
def initialize_game():
    board = [[0 for _ in range(MAX_COL + 2)] for _ in range(MAX_ROW + 3)]
    for col in range(MAX_COL + 2):
        board[-1][col] = 1
    for row in range(MAX_ROW + 3):
        board[row][0] = 1
        board[row][-1] = 1

    block_type = random.randint(2, 8)
    block = Block(block_type)

    return board, block

'''
ブロックこうかとん変更プログラム➁
'''
def draw_board(screen, board, block_images):#着地後のブロック(こうかとん)を表示
    for row in range(2, MAX_ROW + 3):
        for col in range(MAX_COL + 2):
            pygame.draw.rect(screen, (0, 0, 0),
                             Rect(BOARD_OFFSET_X + BLOCK_SIZE * col,
                                  BOARD_OFFSET_Y + BLOCK_SIZE * (row - 2),
                                  BLOCK_SIZE, BLOCK_SIZE))
            block_type = board[row][col]
            if 2 <= block_type <= 8:
                screen.blit(block_images[block_type],
                            (BOARD_OFFSET_X + BLOCK_SIZE * col,
                             BOARD_OFFSET_Y + BLOCK_SIZE * (row - 2)))
'''
ブロックこうかとん変更プログラム➁ここまで
'''

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 750))
    pygame.display.set_caption("Simple Tetris")

    '''
    ブロックこうかとん追加プログラム➀
    '''
    block_images = [None, None]  # インデックス0,1は使わない

    for i in range(2, 9):#2~8の数字を取得
        image = pygame.image.load(f"ex5/fig/{i}.png").convert_alpha()#ファイルから数字に対応した画像を持ってくる。
        image = pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))
        block_images.append(image)

    '''
    ブロックこうかとん追加プログラム➀ここまで
    '''

    # block_color = [(50, 50, 50), (150, 150, 150), (255, 0, 0), (0, 0, 255), (255, 165, 0),
    #                (255, 0, 255), (0, 255, 0), (0, 255, 255), (255, 255, 0)]

    board, block = initialize_game()
    game_over = False

    while not game_over:
        pygame.time.wait(10)
        screen.fill((0, 0, 0))
        draw_board(screen, board, block_images)#block_imagesに変更

        if block:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[K_DOWN]:
                block.move(board, 0)
            if pressed_key[K_LEFT]:
                block.move(board, 1)
            if pressed_key[K_RIGHT]:
                block.move(board, 2)

            if block.drop(board) == 1:
                if block.place(board) == 1:
                    game_over = True
                else:
                    block_type = random.randint(2, 8)
                    block = Block(block_type)
            block.draw(screen, block_images)#block_imagesに変更

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    print("Game Over")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()